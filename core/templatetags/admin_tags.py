from django import template
from frontend.constant import *


from django.db.models import Q

from django.contrib import messages

from django.contrib.contenttypes.models import ContentType

from django.db.models import Sum
from frontend.models import *
from backend.models import *
from core.models import *
import datetime
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.filter(name='get_roomname')
def get_roomname(data):
            
        bookings = []

        for Hotel in Facility.objects.all():
            facility_name = Hotel.facility_name
            count = BookingUser.objects.filter(room_book = Hotel).filter(Q(status = CONFIRMED) | Q(status = DONE)).values('booking_key').distinct().count()
            if count > 0:
                bookings.append({
                    'facility_name':facility_name,
                    'count':count
                    })
        return bookings[:10]
    
@register.filter(name='get_money')
def get_money(data):
    
        PartnerRooms = Facility.objects.all()
        today = datetime.datetime.now()
        money = []

        for Rooms in PartnerRooms:
            facility_name = Rooms.facility_name
            value = BookingUser.objects.filter(room_book = Rooms ,end_date__year = today.year,status=DONE).aggregate(sum=Sum('amount'))['sum']
            if value:
        
                money.append(({
                    'facility_name':facility_name,
                    'value':value
                    }))
    
                
        return money[:10]
    
@register.filter(name='get_usermonth')
def get_usermonth(data):
        month = []
        
        usermonth = []
        start_date = datetime.datetime.today()
        month.append(start_date)
        for i in range(9):
            start_date += relativedelta(months = -1)
            month.append(start_date)
            
            
        for data in month:
            last_month = data + relativedelta(months = -1)
            usermonth.append(({
                    'month': data.strftime("%Y-%m"),
                    'value': User.objects.filter(created_on__lte=data,created_on__gt=last_month).count()
                    }))
        
        return usermonth
    
@register.filter(name='get_useractive')
def get_useractive(data):
    
        useractive = []
            
        useractive.append(({
                'state': 'Active',
                'value': User.objects.filter(is_active = True).count()
                }))
        
        useractive.append(({
                'state': 'InActive',
                'value': User.objects.filter(is_active = False).count()
                }))
        
        return useractive
    
@register.filter(name='get_count')
def get_count(model):
    
    try:
        model = ContentType.objects.get(model=model['object_name'])
    except:
        model = None
    if model:
        get_model= model.model_class()

        return get_model.objects.all().count()
    else:
        return '0' 
