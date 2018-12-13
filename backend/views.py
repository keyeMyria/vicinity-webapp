from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import *
from backend.models import *
import configparser

from itertools import chain

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.forms import *

from django.contrib.auth.hashers import make_password

from accounts.forms import *
from core.models import *
from frontend.models import *
from frontend.constant import *
from django.db.models import Q, Count
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

   
@login_required(login_url='/accounts/register/')
def setting_index(request):
    template_name = 'backend/setting/index.html'
        
    user = User.objects.filter(type_id=SUPER_ADMIN).first()
    
    settings_page, created = Setting.objects.get_or_create(created_by_id=user)
    
    if request.POST:
        
        settings_page.meta_title = request.POST.get('meta_title')
        settings_page.meta_description = request.POST.get('meta_description')
        settings_page.meta_keywords = request.POST.get('meta_keywords')
        settings_page.meta_author = request.POST.get('meta_author')
        settings_page.analytics_code = request.POST.get('analytics_code')
        settings_page.facebook_page = request.POST.get('facebook_page')
        settings_page.twitter_page = request.POST.get('twitter_page')
        settings_page.google_page = request.POST.get('google_page')    
        settings_page.instagram_page = request.POST.get('instagram_page')
        settings_page.site_logo = request.FILES.get('site_logo')
        settings_page.save()
        
        
        BASE_DIR_SETTING = settings.BASE_DIR + '/Project/setting_ini/setting.ini'

        config = configparser.ConfigParser()
        config.optionxform = lambda option: option.upper()

        config.read(BASE_DIR_SETTING)
        
        debug_mode = request.POST.get('debug_mode')
        
        if debug_mode == 'on':
            debug_mode = 'True'
        else:
            debug_mode = ''
        
        config.set('email', 'EMAIL_HOST',request.POST.get('mail_server'))
        config.set('email', 'EMAIL_HOST_USER',request.POST.get('email_user'))
        config.set('email', 'EMAIL_HOST_PASSWORD',request.POST.get('email_pwd'))
        config.set('api', 'GOOGLE_API_KEY',request.POST.get('google_maps_api_key'))
        config.set('api', 'GOOGLE_API_KEY_FRONT',request.POST.get('google_maps_api_key_front'))
        config.set('project', 'DEBUG', debug_mode)

        with open(BASE_DIR_SETTING, "w+") as configfile:
            config.write(configfile)
        
        p = subprocess.check_output([settings.BASE_DIR +'/start.sh'])
        
        return redirect('admin:index')
   
    if not request.user.is_superuser:
        return redirect('admin:login')
    else:
        return render(request, template_name, {'settings_page':settings_page,
                                               'email_user':settings.EMAIL_USER,
                                               'email_pwd':settings.EMAIL_PASSWORD,
                                               'google_maps_api_key':settings.GOOGLE_API_KEY,
                                               'google_maps_api_key_front':settings.GOOGLE_API_KEY_FRONT})
    
@login_required(login_url='/accounts/register/')
def calendar_view(request):
    template_name = 'backend/calendar.html'
    
    subscribe = BookingUser.objects.all()
   
    if not request.user.is_superuser:
        return redirect('core:home')
    else:
        return render(request, template_name, {'subscribe':subscribe})
    
@login_required(login_url='/accounts/register/')
def chat_index(request):
    template_name = 'backend/chat_page.html'
    
    listdata = []        
         
    chatmodellist = ChatModel.objects.all()
    for data in chatmodellist:
        listdata.append(data)
         
    size = len(listdata)
    uniqueNames = [];
    for i in range(0, size, 1):  
        if(listdata[i].sender not in uniqueNames or listdata[i].receiver not in uniqueNames):
            if request.user == listdata[i].receiver or request.user == listdata[i].sender:
                uniqueNames.append(listdata[i].sender);
                uniqueNames.append(listdata[i].receiver);
             
    userprofiledata = []
    for user in uniqueNames:
        userProfile = User.objects.get(username=str(user))  
        if userProfile.type_id != SUPER_ADMIN:       
            userprofiledata.append(userProfile)  
          
    userlist = User.objects.filter(~Q(type_id=GUEST) & ~Q(type_id=SUPER_ADMIN))
    
    chats = userprofiledata
    
    
   
    if not request.user.is_superuser:
        return redirect('core:home')
    else:
        return render(request, template_name, {'users':chats,'userlist':userlist})
    


   
@login_required(login_url='/accounts/register/')
def booking_index(request):
    
    template_name = 'backend/bookingdetails.html'    
    
    page = request.GET.get('page', 1)
    
    sorttype = request.GET.get('sorttype')    
    
    
    notification_latest = NotificationModel.objects.filter(is_read=IS_NOT_READ, to_user_id=request.user)
    
    for notify in notification_latest:
        notify.is_read = IS_READ
        notify.save()
    
    if sorttype:
        sort_type = int(sorttype)
    else:
        sort_type = None
    
    booking = BookingUser.objects.all()
    
    if sort_type:
        booking_list = booking.filter(status = sort_type)
    elif sort_type == 0:
        booking_list = booking.filter(status = 0)
    else:
        booking_list = booking
        
        
    if booking_list:
        if booking_list.count() > 9:
            paginator = Paginator(booking_list, 9)
        else:
            paginator = Paginator(booking_list, booking_list.count())
     
        if booking_list.count() > 9:
            try:
                booking = paginator.page(page)
            except PageNotAnInteger:
                booking = paginator.page(1)
            except EmptyPage:
                booking = paginator.page(paginator.num_pages)
        else:
            booking = booking_list
    else:
        booking = None
   
    if not request.user.is_superuser:
        return redirect('accounts:login')
    else:
        return render(request, template_name, {'booking': booking,
                                               'sorttype':sorttype})
    
@login_required(login_url='/accounts/register/')
def booking_view(request, id):
    template_name = 'backend/bookingview.html'
    
    booking = BookingUser.objects.get(pk=id)
        
    roomdata = ImageSource.objects.filter(facility=booking.room_book).first()
   
    if not request.user.is_superuser:
        return redirect('accounts:login')
    else:
        return render(request, template_name, {'booking': booking,
                                               'roomdata':roomdata})
        
@login_required(login_url='/accounts/register/')
def user_view(request, id):
    template_name = 'backend/userdetails.html'
    searchpayment = request.GET.get('searchpayment')
    
    page = request.GET.get('page', 1)
    
    payments_list = BookingUser.objects.filter(user_subscribe_id=id)
    
    if searchpayment:
        payments_list = payments_list.filter(Q(room_book__title__icontains=searchpayment)|Q(amount=searchpayment))
        
    
        
    if payments_list:
        if payments_list.count() > 10:
            paginator = Paginator(payments_list, 10)
        else:
            paginator = Paginator(payments_list, payments_list.count())
     
        if payments_list.count() > 10:
            try:
                payments = paginator.page(page)
            except PageNotAnInteger:
                payments = paginator.page(1)
            except EmptyPage:
                payments = paginator.page(paginator.num_pages)
        else:
            payments = payments_list
    else:
        payments = None
        
    
    user = User.objects.get(pk=id)
   
    if not request.user.is_superuser:
        return redirect('accounts:login')
    else:
        return render(request, template_name, {'user': user,
                                               'payments':payments})
    
@login_required(login_url='/accounts/register/')
def displayAdminDash(request):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    return render(request,'backend/admindash.html')

@login_required(login_url='/accounts/register/')
def showProposals(request):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    proposal_list = Proposal.objects.all()
    context = {'proposals': proposal_list}
    return render(request, 'backend/proposals.html', context)

@login_required(login_url='/accounts/register/')
def showPartners(request):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    distinct = Partners.objects.values(
                'userID'
            ).distinct()
    distinct = Partners.objects.values('userID_id').annotate(name_count= Count('userID_id'))
    distinct_id = []
    for item in Partners.objects.all():
        if item.userID_id not in distinct_id:
            distinct_id.append(item.id)
    partner_list = Partners.objects.filter(id__in=distinct_id)
    context = {'partners': partner_list}
    return render(request, 'backend/partners.html', context)

@login_required(login_url='/accounts/register/')
def removePartner(request,id):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    partner = Partners.objects.filter(id = id)
    userid = partner.userID
    role = partner.userID 
    role.type_id = USER
    role.save()
    for data in partner:
        data.state_id = NOT_ACTIVE
        data.save()
        
    user = User.objects.get(pk=id)
    user.is_staff = False
    user.save()

    return redirect('backend:showpartners')


@login_required(login_url='/accounts/register/')
def acceptProposals(request,id):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    proposal = Proposal.objects.get(id = id)
    user = proposal.user
    newpartner = Partners.objects.create(userID = user,
                                        CompanyName = proposal.CompanyName,
                                        CompanyEmail = proposal.CompanyEmail,
                                        HQAddress = proposal.HQAddress,
                                        )
    updaterole = User.objects.get(pk = user.pk)
    updaterole.type_id = PARTNER
    proposal.state_id = ACCEPT
    updaterole.save()
    proposal.save()
    return redirect('backend:showproposals')

@login_required(login_url='/accounts/register/')
def declineProposals(request,id):
    proposal = Proposal.objects.get(id = id)
    proposal.state_id = DECLINE
    proposal.save()
    return redirect('backend:showproposals')

    
@login_required
def test_email(request):        
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    
    message = 'This is test email'
    mail_subject = 'Test email.'
    to_email = request.GET.get('test_email')

    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)
   
    return HttpResponse('sent')


@login_required(login_url='/accounts/register/')
def spaceproposals(request):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    spaceadd_list = AddSpaceModel.objects.all().order_by('approval')
    context = {'spaceadd_list': spaceadd_list}
    return render(request, 'frontend/core/confirmroom.html', context)


@login_required(login_url='/accounts/register/')
def spacereviewProposals(request,id):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    
    spaceadd = AddSpaceModel.objects.filter(Q(approval=0)&Q(id=id)).first()
    
    if not spaceadd:
        return redirect('admin:index')
    
    try:
        spaceaddimage = AddSpaceImagesModel.objects.filter(space=spaceadd)
    except AddSpaceModel.DoesNotExist:
        spaceaddimage = None
    
    context = {'spaceadd': spaceadd,'spaceaddimage':spaceaddimage}
    
    if request.method == 'POST':
        if request.POST.get('accept') == 'on':
            
            
            zip_code, created = Geolocation.objects.get_or_create(zipcode=spaceadd.zipcode)
            
            location = Location.objects.create(
                location_type = spaceadd.location_type,
                location_name = spaceadd.location_name,
                street_address_1 = spaceadd.street_address_1 ,
                street_address_2 = spaceadd.street_address_2 ,
                city = spaceadd.city ,
                state = spaceadd.state,
                zipcode = zip_code,
                sun_open_time = spaceadd.sun_open_time,
                sun_close_time = spaceadd.sun_close_time,
                mon_open_time = spaceadd.mon_open_time,
                mon_close_time = spaceadd.mon_close_time,
                tue_open_time = spaceadd.tue_open_time,
                tue_close_time = spaceadd.tue_close_time,
                wed_open_time = spaceadd.wed_open_time,
                wed_close_time = spaceadd.wed_close_time,
                thu_open_time = spaceadd.thu_open_time,
                thu_close_time = spaceadd.thu_close_time,
                fri_open_time = spaceadd.fri_open_time,
                fri_close_time = spaceadd.fri_close_time,
                sat_open_time = spaceadd.sat_open_time,
                sat_close_time = spaceadd.sat_close_time,
                )
            facility = Facility.objects.create(
                facility_name = spaceadd.facility_name,
                facility_information = spaceadd.facility_information,
                parking_spaces = spaceadd.parking_spaces,
                capacity = spaceadd.parking_spaces,
                none_refundable_fee = spaceadd.none_refundable_fee,
                cost_for_profit = spaceadd.cost_for_profit,
                cost_for_non_profit = spaceadd.cost_for_non_profit,
                fac_cost_misc_alc = spaceadd.fac_cost_misc_alc,
                fac_cost_misc_rental_clean_dep_no_alc = spaceadd.fac_cost_misc_rental_clean_dep_no_alc,
                fac_cost_misc_rental_clean_dep_alc = spaceadd.fac_cost_misc_rental_clean_dep_alc,
                fac_cost_misc_non_ref_hr_mtn = spaceadd.fac_cost_misc_non_ref_hr_mtn,
                fac_cost_misc = spaceadd.fac_cost_misc,
                staff_fee = spaceadd.staff_fee,
                fac_amenities = spaceadd.fac_amenities,
                note_1 = spaceadd.note_1,
                note_2 = spaceadd.note_2,
                note_3 = spaceadd.note_3,
                res_1 = spaceadd.res_1,
                res_2 = spaceadd.res_2,
                res_3 = spaceadd.res_3,
                fac_surf_type = spaceadd.fac_surf_type,
                location_id = location,
                fac_feature = spaceadd.fac_feature,
                fee_based_amenities = spaceadd.fee_based_amenities,
                event_type = spaceadd.event_type,
                availability = False
                )
            
            
            facility.partner = spaceadd.created_by_id
            facility.assigned_to_id = request.POST.get('assigned_to')
            facility.save()
            
            if spaceaddimage:
                for data in spaceaddimage:
                    imagesource = ImageSource.objects.create(
                        image_file = data.image_file,
                        facility = facility
                        )
                    
            
            to_email = facility.assigned_to.email
        
            current_site = get_current_site(request)
            message_data = 'This is inform you that you space at location at '+  str(location.street_address_1) + ' ' +  str(location.street_address_2) + ' ' +  location.city + ' ' +  location.state +' has been approved.'
            context = {
                'provider':facility.partner,
                'message':message_data,
            }
            message = render_to_string('provider/space_mail.html', context)
    
            mail_subject = 'Information adding space at '+  str(location.street_address_1) + ' ' +  str(location.street_address_2) + ' ' +  location.city + ' ' +  location.state
    
                
            email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            html_email = render_to_string('provider/space_mail.html',context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            
                
            notification = NotificationModel.objects.create(is_read=IS_NOT_READ, state_id=STATE_IS_NOT_SEND,
                                                        model_id=str(facility.partner.pk),
                                                        description=message_data,
                                                        model_type='space',
                                                        from_user_id=facility.partner,
                                                                to_user_id=facility.partner)
            
            return redirect('backend:spaceacceptproposal',id=id)
        
        if request.POST.get('decline') == 'on':
            
            
    
            to_email = spaceadd.created_by_id.email
        
            current_site = get_current_site(request)
            message_data = 'This is inform you that you space at location at '+  str(spaceadd.street_address_1) + ' ' +  str(spaceadd.street_address_2) + ' ' +  spaceadd.city + ' ' +  spaceadd.state +' has been declined.'
            context = {
                'provider':spaceadd.created_by_id,
                'message':message_data,
            }
            message = render_to_string('provider/space_mail.html', context)
    
            mail_subject = 'Information adding space at '+  str(spaceadd.street_address_1) + ' ' +  str(spaceadd.street_address_2) + ' ' +  spaceadd.city + ' ' +  spaceadd.state
    
                
            email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            html_email = render_to_string('provider/space_mail.html',context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            
                
            notification = NotificationModel.objects.create(is_read=IS_NOT_READ, state_id=STATE_IS_NOT_SEND,
                                                        model_id=str(spaceadd.created_by_id.pk),
                                                        description=message_data,
                                                        model_type='space',
                                                        from_user_id=spaceadd.created_by_id,
                                                                to_user_id=spaceadd.created_by_id)
            
            return redirect('backend:spacedeclineproposal',id=id)
            
    return render(request, 'frontend/core/view_proposal.html', context)


@login_required(login_url='/accounts/register/')
def spaceacceptProposals(request,id):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    proposal = AddSpaceModel.objects.get(id = id)
    proposal.approval = ACCEPT
    proposal.save()
    return redirect('backend:spaceproposals')

@login_required(login_url='/accounts/register/')
def spacedeclineProposals(request,id):
    
    if not request.user.is_superuser:
        return redirect('admin:login')
    proposal = AddSpaceModel.objects.get(id = id)
    proposal.approval = DECLINE
    proposal.save()
    return redirect('backend:spaceproposals')