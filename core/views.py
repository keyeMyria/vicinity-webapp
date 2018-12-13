from django.shortcuts import render, redirect
from accounts.models import *
from accounts.forms import *
from core.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.views.decorators.csrf import csrf_exempt

import random
import string
from django.conf import settings

from datetime import datetime
from django.db.models import Q

import braintree, json
from django.utils.text import capfirst

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from dateutil import parser
from core.templatetags.core_extras import *

braintree.Configuration.configure(braintree.Environment.Sandbox,
                              merchant_id=settings.BRAINTREE_MERCHANT_ID,
                              public_key=settings.BRAINTREE_PUBLIC_KEY,
                              private_key=settings.BRAINTREE_PRIVATE_KEY)

from frontend.constant import *

from django.contrib.sitemaps import Sitemap
from django.core.cache import cache

from core.notification import *

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
       return User.objects.all()
 
    def lastmod(self, item): 
       return item.modifiedDate


def home(request):
    if request.user.is_authenticated and not request.session.get('skip_subscription'):
        try:
            subscribe = SubscriptionUser.objects.filter(user_subscribe=request.user).first()
        except SubscriptionUser.DoesNotExist:
            subscribe = None
                
    location = request.session.get('location', None)
    
        
    if request.user.is_authenticated and request.user.type_id == PARTNER:
        return redirect('managerooms:home')
        
    
    if request.user.is_authenticated and request.user.type_id == SPACE_ADMIN:
        return redirect('spaceadmin:dashboard')
    
    
    
    return render(request, 'frontend/core/home.html',{'location':location})

@login_required(login_url='/accounts/register/')
def subscriptions(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        request.session['skip_subscription'] = True
    
    if request.user.is_authenticated and request.session.get('skip_subscription'):
        return HttpResponseRedirect('/')
    try: 
        subscriptions = Subscriptions.objects.all()
    except Subscriptions.DoesNotExist:
        subcriptions = None
    try:
        subscribe = SubscriptionUser.objects.filter(user_subscribe=request.user).first()
    except SubscriptionUser.DoesNotExist:
        subscribe = None
        
    if subscribe:
        return HttpResponseRedirect('/')
        
    if request.method == "POST":
        
        if request.POST.get('skipnow') == '1':
            request.session['skip_subscription'] = True
        
            return HttpResponseRedirect('/')
        
        
    return render(request, 'frontend/core/subscriptions.html',{'subscriptions':subscriptions
                                                               })
    
@login_required(login_url='/accounts/register/')
@csrf_exempt
def subscribecheckout(request):
    rg = request.POST.get

    amount =  request.POST.get('pricevalue')
    pricetitle =  request.POST.get('pricetitle')
    if not amount:
        return HttpResponseRedirect('/')
    user = User.objects.get(pk=request.user.pk)
    a_customer_id = ''
    if not user:
        result = braintree.Customer.create({
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone": request.user.contact_no,
            })
        if result.is_success:
            user.customer_id = result.customer.id
            user.save()
            a_customer_id = user.customer_id
    else:
        a_customer_id = user.customer_id
    if not user.client_token:
        client_token = braintree.ClientToken.generate({
                "customer_id": a_customer_id
            })
        user.client_token = client_token
        user.save()
    else:
        client_token = user.client_token

    varibles ={'amount':amount,
               'pricetitle':pricetitle,
               'client_token':client_token}
    return render(request, 'payment/subscribecheckout.html',varibles)


@login_required(login_url='/accounts/register/')
@csrf_exempt
def subscribepayment(request):
    if request.POST:
        if request.POST.get("payment_method_nonce"):
            nonce_from_the_client =  request.POST.get("payment_method_nonce")
            staff = User.objects.get(id=request.user.id)
            sub = SubscriptionUser()
            sub.user_subscribe = staff
            sub.payment_nonce = nonce_from_the_client
            sub.amount = request.POST.get("amount")
            sub.save()
            result = braintree.Transaction.sale({
            "amount": sub.amount,
            "payment_method_nonce": sub.payment_nonce
            })
            transaction_id =  result.transaction.id
            sub.txnid = transaction_id
            sub.save()
            message = ''
            if result.is_success:
                sub.result = True
                sub.save()
                message =  'Transaction successfully completed'+' : '+ transaction_id
                
                varibles ={'message':message}
                return render(request, 'payment/subscribesuccess.html',varibles)
            else:
                message = 'Error Transaction Failed'

                varibles ={'message':message,}
                return render(request, 'payment/subscribecheckout.html',varibles)
        else:
            message = 'No transaction'

            varibles ={'message':message,}
            return render(request, 'payment/subscribecheckout.html',varibles)
        
    return HttpResponseRedirect('/')

@login_required(login_url='/accounts/register/')
@csrf_exempt
def bookingcheckout(request):
    rg = request.POST.get
    
    if request.POST.get("paymentmethod") == '0':
    
        staff = User.objects.get(id=request.user.id)
        roomdetails = Facility.objects.get(id=request.POST.get("roomId"))
        sub = BookingUser()
        attendnumber = request.POST.get("attendnumber")
        sub.user_subscribe = staff
        sub.attendees = attendnumber
        sub.amount = request.POST.get("pricevalue")
        sub.room_book = roomdetails
        sub.type = "room"
        if roomdetails.availability == False:
            sub.status = QUEUE
            sub.mode = CASH
        else:
            sub.status = CONFIRMED
            sub.mode = CASH
        sub.start_date = datetime.strptime(request.POST.get("start_date"), '%d/%m/%Y - %H:%M')
        sub.start_time = datetime.strptime(request.POST.get("end_date"), '%I:%M %p')
        sub.end_time = datetime.strptime(request.POST.get("end_date"), '%I:%M %p')
        sub.save()
        roomdetails.availability = False
        roomdetails.save()
        
        
        message =  ''
                
        notification = NotificationModel.objects.create(is_read=IS_NOT_READ, state_id=STATE_IS_NOT_SEND,
                                                    model_id=str(sub.user_subscribe.pk),
                                                    description='Booking confirmed for ',
                                                    model_type='booking',
                                                    from_user_id=sub.user_subscribe,
                                                            to_user_id=sub.user_subscribe)
        varibles ={'message':message, 'room_detail': sub}
        return render(request, 'payment/bookingsuccess.html',varibles)
    
    amount =  request.POST.get('pricevalue')
    priority =  request.POST.get('priority')
    TOTAL_FORMS = request.POST.get('date_extend_total_forms')
    next =  request.POST.get('next')
    array_dates = []
    if not amount:
        return HttpResponseRedirect('/')
    if not TOTAL_FORMS:
        return HttpResponseRedirect('/')
    for form_num in range(1,(int(TOTAL_FORMS)+1)):
        array_dates.append({
            'start_date-'+str(form_num): request.POST.get("start_date-"+str(form_num)),
            'start_time-'+str(form_num): request.POST.get("start_time-"+str(form_num)),
            'end_time-'+str(form_num): request.POST.get("end_time-"+str(form_num)),
            })
     
    roomId = request.POST.get("roomId")
    attendnumber = request.POST.get("attendnumber")
    special_request = request.POST.get("special_request")
    user = User.objects.get(pk=request.user.pk)
    roomdetails = Facility.objects.get(id=request.POST.get("roomId"))
    a_customer_id = ''
    try:
        braintree.Customer.find(user.customer_id)
        a_customer_id = user.customer_id
    except:        
        result = braintree.Customer.create({
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone": request.user.contact_no,
            })
        
        if result.is_success:
            user.customer_id = result.customer.id
            user.save()
            a_customer_id = user.customer_id
        
        
    if not user.client_token:
        client_token = braintree.ClientToken.generate({
                "customer_id": a_customer_id
            })
        user.client_token = client_token
        user.save()
    else:
        client_token = user.client_token
        


    varibles ={'amount':amount,
               'client_token':client_token,
               'roomId':roomId,
               'priority':priority,
               'roomdetails':roomdetails,
               'special_request':special_request,
               'array_dates':array_dates,
               'TOTAL_FORMS':TOTAL_FORMS,
               'attendnumber':attendnumber,
               'next':next,}
    return render(request, 'payment/bookingcheckout.html',varibles)


@login_required(login_url='/accounts/register/')
@csrf_exempt
def bookingpayment(request):
    if request.POST:
            nonce_from_the_client =  request.POST.get("payment_method_nonce")
            
            payment_token_nonce = braintree.PaymentMethod.create({
            "customer_id": request.user.client_token,
            "payment_method_nonce": nonce_from_the_client
            })
            staff = User.objects.get(id=request.user.id)
            roomdetails = Facility.objects.get(id=request.POST.get("roomId"))
            TOTAL_FORMS = request.POST.get('date_extend_total_forms')
            booking_dates_list = '' 
                
                
            timeflexibleval = False
            visitscheduleval = False   
            if request.POST.get('timeflexible') == 'on':
                timeflexibleval = True
            if request.POST.get('visitschedule') == 'on':
                visitscheduleval = True
            
            min_char = 8
            max_char = 12
            allchar = string.ascii_letters + string.digits
            key = str(BookingUser.objects.all().count()+1)+"".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
            
            for form_num in range(1,(int(TOTAL_FORMS)+1)):
                booking_dates_list += request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("start_time-"+str(form_num)) +'-' +request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("end_time-"+str(form_num))
                if form_num != (int(TOTAL_FORMS)):
                    booking_dates_list += ','
                    
                sub = BookingUser()
                sub.user_subscribe = staff
                sub.payment_nonce = nonce_from_the_client
                
                startdate = datetime.strptime(request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("start_time-"+str(form_num)), '%d/%m/%Y %I:%M %p')
               
                startdate = datetime.strftime(startdate,'%a %d %B %Y %I:00 %p')
                
                startutc_dt = parser.parse(startdate)
                
                enddate = datetime.strptime(request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("end_time-"+str(form_num)), '%d/%m/%Y %I:%M %p')
                enddate = datetime.strftime(enddate,'%a %d %B %Y %I:00 %p')
                
                endutc_dt = parser.parse(enddate)
                sub.booking_key = key
                sub.amount = int(get_price(roomdetails)) * (round(((endutc_dt-startutc_dt).days*24) + ((endutc_dt-startutc_dt).seconds/3600)))
                sub.room_book = roomdetails
                sub.attendees = request.POST.get("attendnumber")
                sub.special_request = request.POST.get("special_request")
                sub.mode = ONLINE
                sub.type = "room"
                sub.start_date = datetime.strptime(request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("start_time-"+str(form_num)), '%d/%m/%Y %I:%M %p')
                sub.end_date = datetime.strptime(request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("end_time-"+str(form_num)), '%d/%m/%Y %I:%M %p')
                sub.save()
                sub.status = QUEUE
                sub.save()
                
            message =  'Transaction successfully completed'
            
            roomdetails = Facility.objects.get(id=request.POST.get("roomId"))
            
            if not roomdetails.partner_id:
                partnerId = User.objects.filter(type_id=SPACE_ADMIN).first()
            else:
                partnerId = roomdetails.partner
        
            messagedata = HostMessage.objects.create(user_subscribe=request.user,
                                                room_book = roomdetails,
                                                booking_dates = booking_dates_list,
                                                timeflexible = timeflexibleval,
                                                visitschedule = visitscheduleval,
                                                attendees = request.POST.get('attendnumber'),
                                                message_request = request.POST.get('message_request'),
                                                host_user = partnerId)
        
            notification = NotificationModel.objects.create(is_read=IS_NOT_READ, state_id=STATE_IS_NOT_SEND,
                                                        model_id=str(roomdetails.pk),
                                                        description='Booking reserved for ',
                                                        model_type='booking',
                                                        from_user_id=request.user,
                                                        to_user_id=request.user)
            
            
            varibles ={'message':message, 'roomdetails': roomdetails,'booking_dates_list':booking_dates_list}
            return render(request, 'payment/bookingsuccess.html',varibles)
    else:
        
        return HttpResponseRedirect('/')




@login_required(login_url='/accounts/register/')
def client_token():
    client_token = braintree.ClientToken.generate()
    return client_token

@login_required(login_url='/accounts/register/')
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url='/accounts/register/')
def generate_payment_token(token):
    payment_token_nonce = braintree.PaymentMethod.create({
    "customer_id": token,
    "payment_method_nonce": nonce_from_the_client
    })
    
@login_required(login_url='/accounts/register/')
def NotificationUnreadView(request):
    
        notification = NotificationModel.objects.filter(is_read=IS_NOT_READ, to_user_id=request.user)        
        
        response = {
            'count' : notification.count(),
            'data' : [],
            'status' : '400',
            'latest' : {},
        }
        
        
        
        if notification: 
            for notify in notification[:3]:
                response['data'].append({'message' : NotificationDescription().description(model_id=notify.model_id, description=notify.description,model_type= notify.model_type),
                                     'time': notify.created_on,
                                     'modelid': notify.model_id,
                                     'modeltype': notify.model_type,
                                     'to_user_id':str(notify.to_user_id.pk),
                                     })
                    
                response['status'] = '200'
            
            notification_latest = NotificationModel.objects.filter(state_id=STATE_IS_NOT_SEND, to_user_id=request.user)
            
            
            if notification_latest:
                if notification_latest.count() > 1:
                    response['latest'] = {'message' : 'You have '+ str(notification_latest.count()) + ' notifications',
                                     'time': notification_latest.first().created_on,
                                     'modelid': notification_latest.first().model_id,
                                     'modeltype': notification_latest.first().model_type,
                                     'pk': notification_latest.first().from_user_id.pk,
                                     'to_user_id':str(notification_latest.first().to_user_id.pk),
                            }
                    for notify in notification_latest:
                        if request.POST.get('userid') == str(notify.to_user_id.pk):
                            notify.state_id = STATE_IS_SEND
                            notify.save()
                    response['status'] = '200'
                else:    
                    response['latest'] = {'message' : NotificationDescription().description(model_id=notify.model_id, description=notify.description,model_type= notify.model_type),
                                     'time': notification_latest.first().created_on,
                                     'modelid': notification_latest.first().model_id,
                                     'modeltype': notification_latest.first().model_type,
                                     'pk': notification_latest.first().from_user_id.pk,
                                     'to_user_id':str(notification_latest.first().to_user_id.pk),
                            }
                    
                    if request.POST.get('userid') == str(notification_latest.first().to_user_id.pk):
                        notification_latest.first().state_id = STATE_IS_SEND
                        notification_latest.first().save()
                    response['status'] = '200'
                
        return JsonResponse(response)
    
    
@login_required(login_url='/accounts/register/')
def MessageUnreadView(request):
    response = {
            'count' : '',
            'data' : [],
            'status' : '400',
            'latest' : {},
        }
    notification_latest = MessageModel.objects.filter(Q(to_user_id = request.user)|Q(from_user_id = request.user))
    arraynotify = []
    for data in notification_latest:
        if data.to_user_id == request.user and data.is_read_to_user == IS_NOT_READ and data.state_id_to_user == STATE_IS_NOT_SEND:
            arraynotify.append(data.pk)
    notification_latest = MessageModel.objects.filter(pk__in=arraynotify)
    
    
    if notification_latest:        
            try:
                room = NotifRoom.objects.filter(Q(title='chat#' + str(notification_latest.first().from_user_id.pk) + '_' + str(notification_latest.first().to_user_id.pk))| Q(title='chat#' + str(notification_latest.first().to_user_id.pk) + '_' + str(notification_latest.first().from_user_id.pk))).first()
                                                          
            except NotifRoom.DoesNotExist:
                room = none
                
    
    if notification_latest:
        if notification_latest.count() > 1:
            
                    
            if room:
                roomId = str(room.id)
            response['latest'] = {'message' : 'You have '+ str(notification_latest.count()) + ' new messages',
                             'time': notification_latest.first().created_on,
                             'modelid': notification_latest.first().model_id,
                             'modeltype': notification_latest.first().model_type,
                             'pk': notification_latest.first().from_user_id.pk,
                             'roomId': roomId
                    }
            for notify in notification_latest:
                notify.state_id_to_user = STATE_IS_SEND
                notify.save()
            response['status'] = '200'
        else:    
            
                    
            if room:
                roomId = str(room.id)
                
            response['latest'] = {'message' : MessageDescription().description(user=notification_latest.first().from_user_id ,model_id=notification_latest.first().model_id, description=notification_latest.first().description,model_type= notification_latest.first().model_type),
                             'time': notification_latest.first().created_on,
                             'modelid': notification_latest.first().model_id,
                             'modeltype': notification_latest.first().model_type,
                             'pk': notification_latest.first().from_user_id.pk,
                             'roomId': roomId
                    }
            
            notification_latest.first().state_id_to_user = STATE_IS_SEND
            notification_latest.first().save()
            response['status'] = '200'
            
    return JsonResponse(response)

  
@login_required(login_url='/accounts/register/')  
def MessagesListget(request):
        fromId = request.GET.get('fromId')
        start = request.GET.get('start',0)
        end = request.GET.get('end',10)
        
        usersend = ChatModel.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('created_on')
        
        if fromId:
            usersend = usersend.filter(Q(sender_id=fromId) | Q(receiver_id=fromId)).order_by('created_on')
        
        roomId = ''
        
        try:
            sender_user = User.objects.get(pk=fromId)           
        except User.DoesNotExist:
            sender_user = None
        
    
        receiver_user = request.user
    
        try:
            room = NotifRoom.objects.filter(Q(title='chat#' + str(sender_user.pk) + '_' + str(receiver_user.pk))).first()
                                                      
        except NotifRoom.DoesNotExist:
            room = none
            
                
        if room:
            roomId = str(room.id)  
        
    
        try:
            chatmodellist = ChatModel.objects.filter(Q(sender=sender_user) | Q(receiver=sender_user))
        except:
            chatmodellist = None
            
            
            
        notification = MessageModel.objects.filter(model_type='chat').filter(Q(from_user_id=receiver_user) | Q(to_user_id=receiver_user))
        
        
        if notification: 
            for notify in notification:
                if notify.to_user_id==request.user and notify.is_read_to_user == IS_NOT_READ:
                    notify.is_read_to_user = IS_READ
                    notify.save()

        

        response = {
            'data': [],
            'room_id': roomId,
            }
        
        for data in chatmodellist:
            templist = response['data']
            datapush = {'receiver_id' : data.receiver.pk,
                          'receiver_name' : capfirst(data.receiver.get_full_name()),
                          'sender_id' : data.sender.pk,
                          'sender_name' : capfirst(data.sender.get_full_name()),
                          'created_on' : data.created_on,
                          'message' : data.message,
                        }
            
            templist.append(datapush)            
            response['data'] = templist
            
        return JsonResponse(response)
    
@login_required(login_url='/accounts/register/')  
def MessageReadView(request):
        fromId = request.GET.get('fromId')
        
        usersend = ChatModel.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('created_on')
        
        if fromId:
            usersend = usersend.filter(Q(sender_id=fromId) | Q(receiver_id=fromId)).order_by('created_on')
        
        try:
            sender_user = User.objects.get(pk=fromId)           
        except User.DoesNotExist:
            sender_user = None
        
    
        receiver_user = request.user
            
            
        notification = MessageModel.objects.filter(model_type='chat').filter(Q(from_user_id=receiver_user) | Q(to_user_id=receiver_user))
        
        
        if notification: 
            for notify in notification:
                if notify.to_user_id==request.user and notify.is_read_to_user == IS_NOT_READ:
                    notify.is_read_to_user = IS_READ
                    notify.save()

        
            
        return HttpResponse('read')

@login_required(login_url='/accounts/register/')
def MessagesListpost(request):
    if request.method == "POST":
        fromId = request.POST.get('fromId')
        toId = request.POST.get('toId')
        msg = str(request.POST.get('msg', ''))

        sender_user = User.objects.get(pk=toId)
        receiver_user = User.objects.get(pk=fromId)
        
                    
        msg_obj = ChatModel.objects.create(sender=sender_user, receiver=receiver_user, message=msg, msg_state=ADD_STATE)
        
        notification = MessageModel.objects.create(model_id=str(msg_obj.pk),
                                                                    description='Message received from ',
                                                                    model_type='chat',
                                                                    is_read_from_user = IS_READ,
                                                                    state_id_from_user = STATE_IS_SEND,
                                                                    to_user_id=receiver_user,
                                                                    from_user_id=sender_user)

        
        response = {
            'data': 'saved',
        }
        return JsonResponse(response)     
    
@login_required(login_url='/accounts/register/')
def proof_upload(request):
    
    path = request.GET.get('next', '')
    
    if request.method == "POST":
        proof_liability = request.POST.get('proof_liability')
        proof_nonprofit_status = request.POST.get('proof_nonprofit_status')
        user = User.objects.get(pk=request.user.pk)
        user.proof_liability = proof_liability
        user.proof_nonprofit_status = proof_nonprofit_status
        user.save()
    
    
    
    if path:
        return redirect(path)
    else:
        return HttpResponseRedirect('/')
    
@login_required(login_url='/accounts/register/')   
def cancel_booking(request, id):
    
    path = request.GET.get('next', '')
    

    bookings = BookingUser.objects.filter(booking_key=id)
    
    for booking in bookings:
        booking.queue = False
        booking.status = CANCELLED
        booking.save()
        
        
    notify = NotificationCreate().user(user=request.user,
                                            link='',
                                             is_read=IS_NOT_READ,
                                              state_id=STATE_IS_NOT_SEND,
                                               model_id=bookings[0].room_book.pk,
                                                description='Booking Cancelled for ',
                                                model_type='booking',superadmin=True,spaceadmin=True, partner=True)            
          
    
    if path:
        return redirect(path)
    else:
        return redirect('backend:booking_index')
    
@login_required(login_url='/accounts/register/')  
def NotificationReadView(request):
    
        notification = NotificationModel.objects.filter(is_read=IS_NOT_READ, to_user_id=request.user)
        
        if notification: 
            for notify in notification:
                
                notify.is_read = IS_READ
                notify.save()
                
                
            return HttpResponse('read')
        return HttpResponse('')
    

    
@login_required(login_url='/accounts/register/')
def addwishlist(request):
        
    if request.method == "POST":
        path = request.POST.get('next', '') 
        roomID = request.POST.get('roomID')
        
        try:
            room = Facility.objects.get(pk=roomID)
        except Facility.DoestNotExit:
            room = None
        
        
        board_name_input = request.POST.getlist('board_name_input')
        board_data =  Board.objects.filter(user_subscribe = request.user)
        if board_name_input:
            for data in board_name_input:
                try:
                    roomwishlist = Roomwishlist.objects.get(room_book=room, user_subscribe = request.user,board_id=data)#.exclude(board_id__in=board_name_input)                  
                except Roomwishlist.DoesNotExist:
                    roomwishlist = Roomwishlist.objects.create(room_book=room, user_subscribe = request.user,board_id=data)
                    

            roomwishlist = Roomwishlist.objects.filter(room_book=room, user_subscribe = request.user).exclude(board_id__in=board_name_input).delete()
        else:
            roomwishlist = Roomwishlist.objects.filter(room_book=room, user_subscribe = request.user).delete() 
            if request.POST.get('add_board'):
                board = Board.objects.create(user_subscribe = request.user,
                                        board_name = request.POST.get('board_name'),
                                        event_type_id = request.POST.get('event_type'),
                                        location = request.POST.get('location'),
                                        description = request.POST.get('description'))
            

                roomwishlist = Roomwishlist.objects.create(room_book=room, user_subscribe = request.user,board=board)
        response = 'saved' 
                         
    if path:
        return redirect(path)
    else:
        return HttpResponse(response)


@login_required(login_url='/accounts/register/')
def mywishlist(request):
    
    try:
        board_data =  Board.objects.filter(user_subscribe = request.user)
    except Board.DoesNotExist:
        board_data = None
    
    try:
        roomwishlist = Roomwishlist.objects.filter(user_subscribe = request.user)
    except Roomwishlist.DoesNotExist:
        roomwishlist = None
        
            
    return render(request, 'frontend/core/mywhishlist.html',{'roomwishlist':roomwishlist,
                                                             'board_data':board_data})
    

@login_required(login_url='/accounts/register/')  
def getreviews(request):
    id = request.GET.get('Id')
    facility = Facility.objects.get(pk=id)
    count = int(request.GET.get('count'))
    addcount = count + 5
    reviews = ReviewsModel.objects.filter(room_book=facility)[count:addcount]
    
    return render(request, 'frontend/core/reviewsappend.html',{'reviews':reviews,
                                                               'facility':facility})



    
def error_404(request):
        data = {}
        return render(request,'frontend/404.html', data)
    
def error_500(request):
        data = {}
        return render(request,'frontend/500.html', data)
    
@login_required(login_url='/accounts/register/')    
def chatlist(request):
    user = request.GET.get('user')
    getuser = User.objects.get(pk=user)
    return render(request,'frontend/core/chatlist.html',{'getuser':getuser})
    
    
@login_required(login_url='/accounts/register/')  
def userprofile(request):   
    
    form=ProfileUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form=ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            return redirect('core:userprofile')

    return render(request, 'frontend/core/userprofile.html',{'form':form})


@login_required(login_url='/accounts/register/')
def boarddetail(request,id):
    
    try:
        board_data =  Board.objects.get(user_subscribe = request.user, pk=id)
    except Board.DoesNotExist:
        board_data = None
    
    try:
        roomwishlist = Roomwishlist.objects.filter(user_subscribe = request.user,board=board_data)
    except Roomwishlist.DoesNotExist:
        roomwishlist = None
         
    location = board_data.location
        
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "address={lat}&sensor={sen}&key={key}".format(
        lat=location,
        sen='True',
        key=settings.GOOGLE_API_KEY,
    )
    
    req = requests.get(base, params=params)
    res = req.json()
     

    if 'error_message' not in res.keys():
        
       res_latitude = res['results'][0]['geometry']['location']['lat']
       res_longitude = res['results'][0]['geometry']['location']['lng']
    else:
       res_latitude = ''
       res_longitude = ''
            
    return render(request, 'frontend/core/boarddetail.html',{'roomwishlist':roomwishlist,
                                                             'board_data':board_data,
                                                            'res_latitude':res_latitude,
                                                            'res_longitude':res_longitude})
    

@login_required(login_url='/accounts/register/')
def whishlistremove(request, id, pk):
    
    path = request.GET.get('next', '') 
    
    try:
        board_data =  Roomwishlist.objects.filter(user_subscribe = request.user, board_id=id, room_book_id=pk)
    except Roomwishlist.DoesNotExist:
        board_data = None
        
    if board_data:
        board_data.delete()
        
            
    if path:
        return redirect(path)
    else:
        return HttpResponseRedirect('/')
    


@login_required(login_url='/accounts/register/')
def resendemail(request):
        current_site = get_current_site(request)
        request.user.verification_code = '{0:04}'.format(random.randint(1,9999))
        request.user.save()
        context = {
            'user':request.user, 'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
            'token': account_activation_token.make_token(request.user),
            'url':'/accounts/activate/',
            'resendemail':True
        }
        message = render_to_string('frontend/core/acc_active_email.html', context)
        
        mail_subject = 'Activate your account.'
        to_email = request.user.email

            
        email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
        html_email = render_to_string('frontend/core/acc_active_email.html',context)
        email_message.attach_alternative(html_email, 'text/html')
        email_message.send()
        
        messages.add_message(request, messages.INFO, 'Email sent for verification, please activate you account on link sent to your email')
        
            
        return HttpResponse('sent')

@login_required(login_url='/accounts/register/')
def verifyemail(request):
    
    if request.method == 'POST':
        if request.user.verification_code == request.POST.get('verify_input'):
            request.user.verification_code = request.POST.get('verify_input')
            request.user.email_verified = True
            request.user.save()
            messages.add_message(request, messages.INFO, 'Email verification done.')
            
            return HttpResponse('verified')
        else:
            return HttpResponse('error')
    else:
        
        return HttpResponse('error')

@login_required(login_url='/accounts/register/')
def editboard(request, id):
        
    try:
        board_data =  Board.objects.get(user_subscribe = request.user, pk =id)
    except:
        return redirect('core:mywishlist')
        
    if request.method == "POST":
        path = request.POST.get('next', '') 

        board_data.board_name = request.POST.get('board_name')
        board_data.event_type_id = request.POST.get('event_type')
        board_data.location = request.POST.get('location')
        board_data.description = request.POST.get('description')
        board_data.save()
        
        response = 'saved' 
        return redirect('core:mywishlist')
        
    return render(request, 'frontend/core/boardedit.html',{
                                                             'boarddata':board_data})
                         
    
    
@login_required(login_url='/accounts/register/')
def boardremove(request, id):
    
    path = request.GET.get('next', '')
        
     
    if path:
        board_data =  Board.objects.get(user_subscribe = request.user, pk =id)
        board_data.delete()
        
        response = 'delete'  
                         
        if path:
            return redirect(path)
    else:
        return HttpResponseRedirect('/')
    