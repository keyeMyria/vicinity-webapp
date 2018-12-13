import datetime
from django.db.models import Sum
from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django import forms
from frontend.models import *
from backend.models import *
from core.models import *
from django.views import generic,View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.template import RequestContext
from frontend.forms import *
from frontend.constant import *
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import requests
import string
import braintree, json

braintree.Configuration.configure(braintree.Environment.Sandbox,
                              merchant_id=settings.BRAINTREE_MERCHANT_ID,
                              public_key=settings.BRAINTREE_PUBLIC_KEY,
                              private_key=settings.BRAINTREE_PRIVATE_KEY)

@login_required(login_url='/accounts/register/')
def home(request):
    
    if request.user.type_id != PARTNER:
        return redirect('core:home')
    
    user = request.user
    provider_room = Facility.objects.filter(partner = user)
    context = {'provider_room':provider_room}
    return render(request,'provider/home.html',context)

@login_required(login_url='/accounts/register/')
def showreservations(request,pk):
    
    if request.user.type_id != PARTNER:
        return redirect('core:home')
    
    theroom = Facility.objects.get(id = pk)
    booking_list_array = []
    bookings = BookingUser.objects.filter(room_book_id= pk, result=False, booking_key__isnull=False).values('booking_key','user_subscribe','status').distinct()
    
    for value in bookings:
        
        bookings = BookingUser.objects.filter(booking_key=value['booking_key'])
        
        dates = []
        price = 0
        user_subscribe = value['user_subscribe']
        user = User.objects.get(pk = user_subscribe)
        
        userfullname = user.get_full_name
        
        for index, data in enumerate(bookings):
            dates.append(str(data.start_date.strftime('%a. %d %B %Y, %I:%M %p')) + ' - ' + str(data.end_date.strftime('%a. %d %B %Y, %I:%M %p')))
            price += int(data.amount)
            
        booking_list_array.append({'dates' : dates,
                                     'price': price,
                                     'userfullname': userfullname,
                                     'booking_key': value['booking_key'],
                                     'status': value['status']
                                     })
        
    context = {'booking_list_array':booking_list_array,'theroom':theroom}
    return render(request,'provider/viewbookings.html',context)

@login_required(login_url='/accounts/register/')
def availability(request,id):
    theroom = Facility.objects.get(id = id)
    if theroom.availability:
        theroom.availability = False
    else:
        theroom.availability = True
        
    theroom.save()
    
    
    return HttpResponse('saved')

@login_required(login_url='/accounts/register/')
def approvebooking(request,pk):
    
    now = datetime.datetime.now()
    
    path = request.GET.get('next', '')
    
    host = request.get_host()
    url = redirect('frontend:booking_pdf', id=pk).url
    cookies = request.COOKIES
     
    try:
        bookings = BookingUser.objects.select_related().filter(booking_key=pk)
    except BookingUser.DoesNotExist:
        return redirect('frontend:search_filter')
 
    price = 0
    
    for index, data in enumerate(bookings):
        price += int(data.amount)
        
        
    result = braintree.Transaction.sale({
    "amount": price,
    "payment_method_nonce": bookings[0].payment_nonce
    })
        
 
    session = requests.Session()
    pdf = session.get('http://{}{}'.format(host, url), cookies=cookies)
 
    timestamp = now.strftime('%H-%M %d-%m-%Y')
    pdf_name = 'booking_invoice_{}_{}.pdf'.format('_'.join(bookings[0].room_book.facility_name.split(' ')), timestamp)
    pdf_file = HTML(string=pdf.text).write_pdf()
    
    if result.is_success:
        for booking in bookings:
            booking.status = CONFIRMED
            booking.txnid =  result.transaction.id            
            booking.result = True
            booking.save()
    
    subject =  'Booking Confirmation for ' + bookings[0].room_book.facility_name
    
    message = render_to_string('frontend/core/booking_mesage_email.html', {
        'user':request.user,
        'booking':bookings[0]
    })
    
    mail = EmailMessage(subject, message , settings.EMAIL_HOST_USER, [bookings[0].user_subscribe.email])
    mail.attach(pdf_name, pdf_file, 'application/pdf')
    mail.send()
    
    notification = NotificationModel.objects.create(is_read=IS_NOT_READ, state_id=STATE_IS_NOT_SEND,
                                                            model_id=str(bookings[0].room_book.pk),
                                                            description='Booking Confirmed for ',
                                                            model_type='booking',
                                                            from_user_id=request.user,
                                                            to_user_id=request.user)
    
    if path:
        return redirect(path)
    else:
        return redirect('managerooms:roomsreservations', pk=bookings[0].room_book.pk)

@method_decorator(login_required, name='dispatch')
class ChartView(View):
    def get(self,request,id):
    
        if request.user.type_id != PARTNER:
            return redirect('core:home')
        
        
        RoomsNames = []
        for data in Facility.objects.filter(partner_id = request.user.id).values_list('facility_name', flat=True):
            RoomsNames.append(data)
            
        PartnerRooms = Facility.objects.filter(partner_id = request.user.pk)
        bookings = []

        for Hotel in PartnerRooms:
            bookings.append(BookingUser.objects.filter(room_book = Hotel).filter(Q(status = CONFIRMED) | Q(status = DONE)).values('booking_key').distinct().count())

        today = datetime.datetime.now()
        money = []

        for Rooms in PartnerRooms:
            value = BookingUser.objects.filter(room_book = Rooms ,end_date__year = today.year,status=DONE).aggregate(sum=Sum('amount'))['sum']
            if value:
                money.append(value)
            else:
                money.append(0)
        data = {"RoomsNames":RoomsNames,"bookings":bookings,"money":money}
        return render(request, 'provider/partnercharts.html',data)


