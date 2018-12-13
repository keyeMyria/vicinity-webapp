from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login as auth_login

from accounts.models import *
from accounts.forms import *
from django.contrib.auth.hashers import make_password

from django.db.models import Q
from django.conf import settings

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from accounts import forms

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect

import random

@csrf_exempt
def login_user(request, template_name=None, extra_context=None):
    template_name = 'frontend/accounts/login.html'
    response = auth_views.login(request, template_name)
    
    if request.POST.get('remember_me'):
        request.session.set_expiry(1209600)
    else:
        request.session.set_expiry(0)
        
    
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')
    
    try:
        user = User.objects.get(Q(email=request.POST.get('username'))|Q(username=request.POST.get('username')))
    except:
        user = None  
        
    
        
    if user:
        if user.email_verified == False:
            if '_auth_user_id' not in request.session.keys():
                messages.add_message(request, messages.INFO, 'Email not verified, please activate you account on link sent to your email')
     
        
    return response

@csrf_exempt
def login_user_auth(request, template_name=None, extra_context=None):
    template_name = 'frontend/accounts/login.html'
    response = auth_views.login(request, template_name)
    
    if request.POST.get('remember_me'):
        request.session.set_expiry(1209600)
    else:
        request.session.set_expiry(0)
    
    try:
        user = User.objects.get(Q(email=request.POST.get('username'))|Q(username=request.POST.get('username')))
    except:
        user = None  
        
    
        
#     if user:
#         if user.email_verified == False:
#             if '_auth_user_id' not in request.session.keys():
#                 messages.add_message(request, messages.INFO, 'Email not verified, please activate you account on link sent to your email')
     
    if request.user.is_authenticated:
        
        return render(request, 'frontend/includes/_header.html', {'response':response}, status=202)
    else:

        return render(request, 'frontend/core/login/login-update.html', {'response':response}, status=201)


def password_reset(request):
    response = auth_views.password_reset(request, post_reset_redirect='done/',html_email_template_name='registration/password_reset_email.html')
        
    return response



def logout(request):
    response = auth_views.logout(request, next_page='/')
        
    return response



def password_reset_done(request):
    response = auth_views.password_reset_done(request)
        
    return response



def password_reset_confirm(request, uidb64=None, token=None):
    template_name = 'frontend/accounts/login.html'
    response = auth_views.password_reset_confirm(request, uidb64=uidb64, token=token, post_reset_redirect="/")
        
    return response



def password_reset_complete(request):
    response = auth_views.password_reset_complete(request)
        
    return response


def auth_form(request):
    
    if request.GET.get('type_form') == 'login':
        
        return render(request, 'frontend/core/login/login-update.html', status=200)
    
    if request.GET.get('type_form') == 'register':
        
        
        form = CreateUserForm()
        registerform = CreateBusinessForm()
        
        return render(request, 'frontend/core/register/register-update.html',  {'form':form,'registerform':registerform}, status=200)
    
    return HttpResponse(status=400)

def Register(request):
         
    typeuser = '4' 
    orgtype = ''
    orgname = ''
    orgcount = ''
    
    if request.method == 'POST':           
        form = CreateUserForm(request.POST)
        typeuser = request.POST.get('type_id')
        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.get(email=data.get('email'),type_id=GUEST).delete()
            except:
                None
            user = User.objects.create(email=data.get('email'),
                                            first_name=data.get('first_name'),
                                            last_name=data.get('last_name'),
                                            username=data.get('username'),
                                            password=make_password(data.get('password')),
                                            date_of_birth=data.get('date_of_birth'),
                                            gender=data.get('gender'),
                                            about_me=data.get('about_me'),
                                            address=data.get('address'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            type_id=request.POST.get('type_id'),
                                            zipcode=data.get('zipcode'),
                                            language=data.get('language'),
                                            contact_no=request.POST.get('contact_no'))
            
            user.verification_code = '{0:04}'.format(random.randint(1,9999))
            user.save()
            current_site = get_current_site(request)
            context = {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                'url':'/accounts/activate/',
            }
            message = render_to_string('frontend/core/acc_active_email.html', context)
            
            mail_subject = 'Activate your account.'
            to_email = data.get('email')

                
            email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            html_email = render_to_string('frontend/core/acc_active_email.html',context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            
            messages.add_message(request, messages.INFO, 'Email sent for verfication, please activate you account on link sent to your email')
            
                
            return redirect('accounts:login')
        

        orgtype = request.POST.get('orgtype')
        orgname = request.POST.get('orgname')
        orgcount = request.POST.get('orgcount')
    else:
        form = CreateUserForm()
    registerform = CreateBusinessForm() 

    return render(request, 'frontend/accounts/registration.html', {'form':form,'registerform':registerform, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype})

def RegisterBusiness(request):
         
    typeuser = '3' 
    orgtype = ''
    orgname = ''
    orgcount = ''
    
    if request.method == 'POST':           
        registerform = CreateBusinessForm(request.POST)
        typeuser = request.POST.get('type_id')
        if registerform.is_valid():
            data = registerform.cleaned_data
            try:
                User.objects.get(email=data.get('email'),type_id=GUEST).delete()
            except:
                None
            user = User.objects.create(email=data.get('email'),
                                            first_name=data.get('first_name'),
                                            last_name=data.get('last_name'),
                                            username=data.get('username_buisness'),
                                            password=make_password(data.get('password')),
                                            date_of_birth=data.get('date_of_birth'),
                                            gender=data.get('gender'),
                                            about_me=data.get('about_me'),
                                            address=data.get('address'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            type_id=request.POST.get('type_id'),
                                            zipcode=data.get('zipcode'),
                                            language=data.get('language'),
                                            contact_no=request.POST.get('contact_no'))
            
            if user.type_id == BUSINESS:
                OrgType.objects.create(orgtype = data.get('orgtype'),
                    orgname = data.get('orgname'),
                    orgcount = data.get('orgcount'),
                    created_by_id = user)
            user.verification_code = '{0:04}'.format(random.randint(1,9999))
            user.save()
            current_site = get_current_site(request)
            context = {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                'url':'/accounts/activate/',
            }
            message = render_to_string('frontend/core/acc_active_email.html', context)
            
            mail_subject = 'Activate your account.'
            to_email = data.get('email')

                
            email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            html_email = render_to_string('frontend/core/acc_active_email.html',context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            
            messages.add_message(request, messages.INFO, 'Email sent for verfication, please activate you account on link sent to your email')
            
                
            return redirect('accounts:login')
        

        orgtype = request.POST.get('orgtype')
        orgname = request.POST.get('orgname')
        orgcount = request.POST.get('orgcount')
    else:
        registerform = CreateUserForm() 
        
    form = CreateUserForm()

    return render(request, 'frontend/accounts/registration.html', {'form':form,'registerform':registerform, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype})

def RegisterAuth(request):
         
    typeuser = '' 
    orgtype = ''
    orgname = ''
    orgcount = ''
    
    if request.method == 'POST':           
        form = CreateUserForm(request.POST)
        registerform = CreateBusinessForm(request.POST)
        typeuser = request.POST.get('type_id')
        if typeuser == str(BUSINESS):
            form = registerform
        if form.is_valid():
            data = form.cleaned_data
            
            email=data.get('email')
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            username=data.get('username_user')
            password=make_password(data.get('password'))
            
            if typeuser == str(BUSINESS):
                email = data.get('email_business')
                first_name=data.get('first_name_business')
                last_name=data.get('last_name_business')
                username=data.get('username_business')
                password=make_password(data.get('password_business'))
            
            
            
            try:
                User.objects.get(email=data.get('email'),type_id=GUEST).delete()
            except:
                None
            user = User.objects.create(email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            username=username,
                                            password=password,
                                            date_of_birth=data.get('date_of_birth'),
                                            gender=data.get('gender'),
                                            about_me=data.get('about_me'),
                                            address=data.get('address'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            type_id=request.POST.get('type_id'),
                                            zipcode=data.get('zipcode'),
                                            language=data.get('language'),
                                            contact_no=request.POST.get('contact_no'))
            
            if user.type_id == BUSINESS:
                OrgType.objects.create(orgtype = data.get('orgtype'),
                    orgname = data.get('orgname'),
                    orgcount = data.get('orgcount'),
                    created_by_id = user)
            user.verification_code = '{0:04}'.format(random.randint(1,9999))
            user.save()
            current_site = get_current_site(request)
            context = {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                'url':'/accounts/activate/',
            }
            message = render_to_string('frontend/core/acc_active_email.html', context)
            
            mail_subject = 'Activate your account.'
            to_email = data.get('email')
            email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            html_email = render_to_string('frontend/core/acc_active_email.html',context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            
            messages.add_message(request, messages.INFO, 'Email sent for verfication, please activate you account on link sent to your email')
            
                
            return render(request, 'frontend/includes/_alerts.html', {'registerform':form, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype},status='200')
        
        orgtype = request.POST.get('orgtype')
        orgname = request.POST.get('orgname')
        orgcount = request.POST.get('orgcount')
        if typeuser == str(USER):
            return render(request, 'frontend/core/register/register-user.html', {'registerform':form, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype},status='201')            
        if typeuser == str(BUSINESS):
            return render(request, 'frontend/core/register/register-buisness.html', {'registerform':form, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype},status='202')
    else:
        form = CreateUserForm()
        registerform = CreateBusinessForm()

    return render(request, 'frontend/accounts/registration.html', {'form':form, 'registerform':registerform, 'typeuser':typeuser, 'orgcount':orgcount, 'orgname':orgname, 'orgtype':orgtype})


def activate(request, uidb64, token):
        
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    validlink = True
    
    if user is not None and account_activation_token.check_token(user, token):
        if user.email_verified:
            validlink = False
            
    if not user or not account_activation_token.check_token(user, token):
        validlink = False
    
    
    if request.method == "POST":

        if user is not None and account_activation_token.check_token(user, token):
            if user.verification_code == request.POST.get('verify_input'): 
                user.is_active = True
                user.email_verified = True
                user.save()
                messages.add_message(request, messages.INFO, 'Email is verified, you can login now.')
            else:
                messages.add_message(request, messages.INFO, 'Email is not verified, please enter correct verification code.')
                return redirect('accounts:activate',uidb64=uidb64,token=token)
            
            return redirect('/')
        
        messages.add_message(request, messages.INFO, 'The activation link is invalid, possibly because it has already been used.')
        return redirect('/')
        
    return render(request, 'frontend/core/acc_active_pass.html', {
                                                               'uidb64':uidb64,
                                                               'token':token,
                                                               'validlink':validlink})
    

