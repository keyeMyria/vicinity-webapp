from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django import forms
from frontend.models import *
from backend.models import *
from core.models import *
from django.views import generic,View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.template import RequestContext
from frontend.forms import *
from spaceadmin.forms import *
from frontend.constant import *
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

@login_required(login_url='/accounts/register/')
def dashboard(request):
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    booking_list_array = []
    book_list = BookingUser.objects.prefetch_related('room_book').filter(booking_key__isnull=False,
                                                                           room_book__assigned_to = request.user).values(
                                                                               'booking_key','user_subscribe','status',
                                                                               'attendees','special_request').distinct()
    
    for value in book_list:
        
        bookings = BookingUser.objects.filter(booking_key=value['booking_key'])
        
        dates = []
        user_subscribe = value['user_subscribe']
        user = User.objects.get(pk = user_subscribe)
        
        userfullname = user.get_full_name
        
        for index, data in enumerate(bookings):
            dates.append(str(data.start_date.strftime('%a. %d %B %Y, %I:%M %p')) + ' - ' + str(data.end_date.strftime('%a. %d %B %Y, %I:%M %p')))
          
            
        booking_list_array.append({'dates' : dates,
                                     'userfullname': userfullname,
                                     'booking_key': value['booking_key'],
                                     'status': value['status'],
                                     'attendees': value['attendees'],
                                     'special_request': value['special_request'],
                                     'room_book':bookings[0].room_book
                                     })    
        
    
    
    room_list = Facility.objects.filter(assigned_to=request.user)
    
    context = {
               'booking_list_array':booking_list_array,
               'room_list':room_list,
               }
    
    return render(request,'space_admin/dashboard.html',context)

@login_required(login_url='/accounts/register/')
def reservation_detail(request, pk):
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    user = request.user
    booking_list_array = []
    book_list = BookingUser.objects.prefetch_related('room_book').filter(booking_key__isnull=False,
                                                                           room_book__assigned_to = user, booking_key=pk).values(
                                                                               'booking_key','user_subscribe','status',
                                                                               'attendees','special_request').distinct()
    for value in book_list:
        
        bookings = BookingUser.objects.filter(booking_key=value['booking_key'])
        
        dates = []
        user_subscribe = value['user_subscribe']
        user = User.objects.get(pk = user_subscribe)
        
        userfullname = user.get_full_name
        
        for index, data in enumerate(bookings):
            dates.append(str(data.start_date.strftime('%a. %d %B %Y, %I:%M %p')) + ' - ' + str(data.end_date.strftime('%a. %d %B %Y, %I:%M %p')))
          
            
        booking_list_array.append({'dates' : dates,
                                     'userfullname': userfullname,
                                     'booking_key': value['booking_key'],
                                     'status': value['status'],
                                     'attendees': value['attendees'],
                                     'special_request': value['special_request'],
                                     'room_book':bookings[0].room_book
                                     })

    if booking_list_array:
        try:
            facility_room = Facility.objects.get(assigned_to=user, pk=booking_list_array[0]['room_book'].pk)
        
        except Facility.DoesNotExist:
            facility_room = None
    else:
        facility_room = None
    
            
    try:
        user_data = User.objects.get(pk=user.pk)
    except Partners.DoesNotExist:
        user_data = None
    
    context = {'booking_list_array':booking_list_array,
               'facility_room':booking_list_array[0]['room_book'],
               'user_data': user_data,
               }
    
    return render(request,'space_admin/reservation_detail.html',context)

@login_required(login_url='/accounts/register/')
def location_view(request):
    user = request.user
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    location_id = []
    
    try:
        location = Facility.objects.filter(assigned_to=user)
    except Facility.DoesNotExist:
        location = None
        
    for data in location:
        if data.location_id.pk not in location_id:
            location_id.append(data.location_id.pk)
            
    try:
        location = Location.objects.filter(pk__in=location_id)
    except Location.DoesNotExist:
        location = None
    
    context = {'location': location,
               }
    
    return render(request,'space_admin/location_view.html',context)

@login_required(login_url='/accounts/register/')
def location_detail(request, pk):
    user = request.user
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        location = None
    
    if location:
        try:
            facility_room = Facility.objects.filter(assigned_to=user, location_id_id=location.pk)
        
        except Facility.DoesNotExist:
            facility_room = None
    else:
        facility_room = None
        
    if not facility_room:
        return redirect('spaceadmin:location_view')
    
    
    context = {'location': location,
               'facility_room':facility_room,
               }
    
    return render(request,'space_admin/location_detail.html',context)

@login_required(login_url='/accounts/register/')
def room_detail(request, pk):
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    user = request.user
    try:
        facility_room = Facility.objects.get(assigned_to=user, pk=pk)
    
    except Facility.DoesNotExist:
        facility_room = None
    
    if facility_room:
        try:
            booking = BookingUser.objects.filter(status = CONFIRMED, room_book__assigned_to = user, room_book=facility_room)
        except BookingUser.DoesNotExist:
            booking = None
    else:
        booking = None
            
    try:
        partner = Partners.objects.get(userID=user)
    except Partners.DoesNotExist:
        partner = None
    
    context = {'booking': booking,
               'facility_room':facility_room,
               'partner': partner,
               }
    
    return render(request,'space_admin/room_view.html',context)



@login_required(login_url='/accounts/register/')
def location_edit(request, pk):
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        location = None
    
    if request.method =="POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
        return redirect('spaceadmin:location_detail', pk=pk)
    else:
        form = LocationForm(instance=location)
    
    context = {'form': form,
               }
    
    return render(request,'space_admin/location_edit.html',context)

@login_required(login_url='/accounts/register/')
def facility_edit(request, pk):
    
    if request.user.type_id != SPACE_ADMIN:
        return redirect('core:home')
    
    
    try:
        facility = Facility.objects.get(pk=pk)
    except Facility.DoesNotExist:
        facility = None
    
    if request.method =="POST":
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            
        return redirect('spaceadmin:room_detail', pk=pk)
    else:
        form = FacilityForm(instance=facility)
    
    context = {'form': form,
               }
    
    return render(request,'space_admin/facility_edit.html',context)