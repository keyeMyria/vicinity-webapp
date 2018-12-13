from django.shortcuts import render, redirect
from accounts.models import *
from core.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from django.contrib.auth import authenticate, login as auth_login
import random
import re

import string
from django.conf import settings
from frontend.models import *
from frontend.constant import *
from django.db.models import Q, Avg
from .forms import *
from django.core.mail import send_mail
import MySQLdb

from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.views import View
from django.utils.decorators import method_decorator
import requests
import datetime, json
from datetime import timedelta
from weasyprint import HTML, CSS

from datetime import datetime as datepicker

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.db.models.functions import Concat

from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.http.response import JsonResponse

from dateutil import parser
from email.utils import parsedate_tz, mktime_tz
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.hashers import make_password
import base64

from django.core.files.base import ContentFile

def weighted(nb):
    if nb is None:
        return -float('inf')
    else:
        return nb

def search_filter(request):
    
    page = request.GET.get('page', 1)
    sorttype = request.GET.get('sorttype')
    location = request.GET.get('location')
    zipcode = request.GET.get('zipcode')
    minValue = request.GET.get('minValue')
    maxValue = request.GET.get('maxValue')
    minattendees = 0
    maxattendees = request.GET.get('attendees')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    view = request.GET.get('view')
    getrating = request.GET.get('getrating')
    zoom = request.GET.get('zoom')
    ne_lat = request.GET.get('ne_lat')
    sw_lng = request.GET.get('sw_lng')
    sw_lat = request.GET.get('sw_lat')
    ne_lng = request.GET.get('ne_lng') 
    start_date = datepicker.strptime(start_date, '%d/%m/%Y') if start_date else datepicker.now()
    
    end_date = None
    
    if start_date != None:
        end_date = start_date + timedelta(days=1)

    plantype = request.GET.get('plantype')
        
    amenities = request.GET.get('amenities')
    
    if location:
        request.session['location'] = location
    
    location = request.session.get('location')
    
    url_contains = ''
    
    if location:
        url_contains = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', location)
    
        
    db = MySQLdb.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

    cursor = db.cursor()
    
    plantype_join = []
    amenities_join = []
    getrating_join = []
    
    if plantype:
        plantype = plantype.split(',')
        plantype_join = ','.join(plantype)
    
    if amenities:
        amenities = amenities.split(',')
        amenities_join = ','.join(amenities)
        
        
    if getrating:
        getrating = getrating.split(',')
        getrating_join = ','.join(getrating)
    
    room_query = ""

    _and = False
    
    location_default = False 

    if maxattendees or minValue or maxValue or start_date or end_date:
        room_query = room_query + " WHERE " 
        
    if not location:
        location = 'United States'
        request.session['location'] = location
        location_default = True
        
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "address={lat}&sensor={sen}&key={key}".format(
        lat=location,
        sen='True',
        key=settings.GOOGLE_API_KEY,
    )
    
    req = requests.get(base, params=params)  
    res = req.json()
    
    country = False
    updateall = False
    
    place_length = True
    
    message_update = ''
    
    if 'error_message' in res.keys() and res['status'] != 'ZERO_RESULTS':
        message_update = 'No places found at ' + location
         
        place_length = False
    
    if len(url_contains) > 0:
        message_update = 'There is error in your search with ' + location
    
    if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':

        for data in reversed(res['results'][0]['address_components']):
            
            if 'country' in data['types']:
                if data['short_name'] != 'US':
                    messages.add_message(request, messages.INFO, 'We are not serving outside United States.')
                    return redirect('core:home') 
                
                zoom = 4
                country = True
                updateall = True
                
            if 'administrative_area_level_1' in data['types']:
            
                zoom = 8
                country = True
                
                updateall = False
                
            if 'administrative_area_level_2' in data['types']:
            
                zoom = 10
                country = True
                
                updateall = False
            if 'locality' in data['types']:
            
                zoom = 14
                country = True
                
                updateall = False
                
            if 'neighborhood' in data['types']:
            
                zoom = 17
                country = True
                
                updateall = False
            
    
    
        
        res_latitude = res['results'][0]['geometry']['location']['lat']
        res_longitude = res['results'][0]['geometry']['location']['lng']
        
    else:
        res_latitude = ''
        res_longitude = ''
    
    
        
    if minValue or maxValue:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + 'org_id_id in (select org_type_id from tbl_org) or ((cost_for_profit BETWEEN ' + str(minValue) + ' and ' + str(maxValue) + ') or (cost_for_non_profit BETWEEN ' + str(minValue) + ' and ' + str(maxValue) + '))'
        _and = True
        
    if start_date or end_date:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + 'id NOT IN (select room_book_id from '+ BookingUser._meta.db_table +' WHERE (start_date BETWEEN "'+ str(start_date) +'" AND "'+ str(end_date) +'") OR (end_date BETWEEN "'+ str(start_date) +'" AND "'+ str(end_date) +'"))'
        _and = True
    
        
    if maxattendees:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + '(capacity >= ' +str(maxattendees) + ') '
        _and = True 

    
    room_query = "SELECT * FROM "+ Facility._meta.db_table + " " + room_query
    
    
    
    room_query_table = ''
    room_query_table_area = ''
     
    if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':          
        if not ne_lat and not sw_lng and not sw_lat and not ne_lng:
            if 'bounds' in res['results'][0]['geometry'].keys():
                keyvalue = 'bounds'
            else:
                keyvalue = 'viewport'
            ne_lat = str(res['results'][0]['geometry'][keyvalue]['northeast']['lat'])
            sw_lng = str(res['results'][0]['geometry'][keyvalue]['southwest']['lng'])
            sw_lat = str(res['results'][0]['geometry'][keyvalue]['southwest']['lat'])
            ne_lng = str(res['results'][0]['geometry'][keyvalue]['northeast']['lng'])
            
        if ne_lat and sw_lng and sw_lat and ne_lng:
            room_query_table = 'SELECT * \
    FROM tbl_facility \
    WHERE ST_CONTAINS(ST_GeomFromText("Polygon(('+ sw_lat +' '+ sw_lng +','+ sw_lat +' '+ ne_lng +','+ ne_lat +' '+ ne_lng +','+ ne_lat +' '+ sw_lng +','+ sw_lat +' '+ sw_lng +'))"), point(latitude, longitude));'
    
    
    data_list_table = []
    if  room_query_table:
        cursor.execute(room_query_table)

        desc = cursor.description 
        data_list_table = [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
        ]

        room_query_table_area = 'SELECT\
  *, (\
    3959 * acos (\
      cos ( radians('+ str(res_latitude) +') )\
      * cos( radians( latitude ) )\
      * cos( radians( longitude ) - radians('+ str(res_longitude) +') )\
      + sin ( radians('+ str(res_latitude) +') )\
      * sin( radians( latitude ) )\
    )\
  ) AS distance \
FROM tbl_facility \
HAVING distance < 0.2'
        cursor.execute(room_query_table_area)
        
        desc_area = cursor.description 
        data_list_table_area = [
                    dict(zip([col[0] for col in desc_area], row)) 
                    for row in cursor.fetchall() 
            ]
        for dataarea in data_list_table_area: 
            if dataarea['id'] not in [data['id'] for data in data_list_table]:            
                data_list_table.append(dataarea)
        
    
    cursor.execute(room_query)

    desc = cursor.description 
    data_list = [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
        ]
    
    db.close()
    
    if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':
        facilities_list = Facility.objects.filter(id__in = [data['id'] for data in data_list_table]).order_by('facility_name')
    else:
        facilities_list = Facility.objects.all().order_by('facility_name')
    
    
    facilities_list = facilities_list.filter(id__in = [data['id'] for data in data_list]).order_by('facility_name')
        
        
    if updateall:
        
        facilities_list = Facility.objects.all()
        
    
    facility = []
    facility_cost = []
    amenities_list = []
    plantype_list = []
    
    
    getratinglist = [] 
       
    if getrating:
        for facilities in facilities_list:
            data = ReviewsModel.objects.filter(room_book=facilities).aggregate(Avg('rate')).get('rate__avg')
            if data:
                if str(round(float(data))) in getrating:
                    getratinglist.append((data, facilities.pk))
        
        facilities_list = facilities_list.filter(id__in = [data[1] for data in getratinglist])
        
    if amenities:
        for data in amenities:

            if data_list:
                for facilities in facilities_list:
                    if facilities.fac_amenities:
                        if data in facilities.fac_amenities:
                            
                            amenities_list.append(facilities.pk)
                            
        facilities_list = facilities_list.filter(id__in = [data for data in amenities_list])
    
    if plantype:
        for data in plantype:

            if data_list:
                for facilities in facilities_list:
                    if facilities.event_type:
                        if data in facilities.event_type:
                            
                            plantype_list.append(facilities.pk)
                            
        facilities_list = facilities_list.filter(id__in = [data for data in plantype_list])
    
    if sorttype:
        
        if sorttype == 'availability':
            facilities_list = facilities_list.filter(availability=True)
        elif sorttype == 'rating':
            for facilities in facilities_list:
                data = ReviewsModel.objects.filter(room_book=facilities).aggregate(Avg('rate')).get('rate__avg')
                facility.append((data, facilities.pk))
                
            facility = sorted(facility, key=lambda x:weighted(x[0]), reverse=True)
            ordering = 'FIELD(`id`, %s)' % ','.join(str(id[1]) for id in facility)
            facilities_list = facilities_list.filter(id__in = [data[1] for data in facility]).extra(
           select={'ordering': ordering}, order_by=('ordering',))
        elif sorttype == 'price_asc' or sorttype == 'price_des':
            if sorttype == 'price_des':
                order = 'ordering'
            else:
                order = '-ordering'
            for facilities in facilities_list:
                try:
                    cost_profit = int(facilities.cost_for_profit)
                except:
                    cost_profit = None
                facility_cost.append((cost_profit, facilities.pk))
            
                
            facility_cost_list = sorted(facility_cost, key=lambda x:weighted(x[0]), reverse=True)
            ordering = 'FIELD(`id`, %s)' % ','.join(str(id[1]) for id in facility_cost_list)
            facilities_list = facilities_list.filter(id__in = [data[1] for data in facility_cost_list]).extra(
           select={'ordering': ordering}, order_by=(order,))
        elif sorttype == 'capacity_asc' or sorttype == 'capacity_des':
            if sorttype == 'capacity_des':
                order = '-capacity'
            else:
                order = 'capacity'
            facilities_list = facilities_list.order_by(order)
        else:
            facilities_list = facilities_list.order_by(sorttype)
        
        
    if facilities_list:
        if len(facilities_list) > 8:
            paginator = Paginator(facilities_list, 8)
        else:
            paginator = Paginator(facilities_list, len(facilities_list))
      
        if len(facilities_list) > 8:
            try:
                facilities = paginator.page(page)
            except PageNotAnInteger:
                facilities = paginator.page(1)
            except EmptyPage:
                facilities = paginator.page(paginator.num_pages)
        else:
            facilities = facilities_list
    else:
        facilities = None
    
    
    map_facility = facilities_list

    
    
    return render(request, 'frontend/core/results.html',{'facilities':facilities,
                                                         'count':len(facilities_list),
                                                         'plantype':plantype_join,
                                                         'sorttype':sorttype,
                                                         'minattendees':minattendees,
                                                         'attendees':maxattendees,
                                                         'end_date':end_date,
                                                         'start_date':start_date,
                                                         'location':location,
                                                         'minValue':minValue,
                                                         'maxValue':maxValue,
                                                         'zipcode':zipcode,
                                                         'facilities_list':facilities_list,
                                                         'amenities':amenities_join,
                                                         'res_latitude':res_latitude,
                                                         'res_longitude':res_longitude,
                                                         'view': view,
                                                         'page':page,
                                                         'ne_lat':ne_lat,
                                                        'sw_lng':sw_lng,
                                                        'sw_lat': sw_lat,
                                                        'ne_lng':ne_lng,
                                                        'country':country,
                                                        'zoom':zoom,
                                                        'url_contains':url_contains,
                                                        'message_update':message_update,
                                                        'place_length':place_length,
                                                         'map_facility':map_facility,
                                                         'getrating':getrating_join})

def get_search_filter(request):    
    
    page = request.GET.get('page', 1)
    sorttype = request.GET.get('sorttype')
    location = request.GET.get('location')
    zipcode = request.GET.get('zipcode')
    minValue = request.GET.get('minValue')
    maxValue = request.GET.get('maxValue')
    minattendees = 0
    maxattendees = request.GET.get('attendees')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    view = request.GET.get('view')
    getrating = request.GET.get('getrating')
    zoom = request.GET.get('zoom')
    ne_lat = request.GET.get('ne_lat')
    sw_lng = request.GET.get('sw_lng')
    sw_lat = request.GET.get('sw_lat')
    ne_lng = request.GET.get('ne_lng')
    radius = request.GET.get('radius') if request.GET.get('radius') else '10' 
    start_date = datepicker.strptime(start_date, '%d/%m/%Y') if start_date else None
    
    end_date = None
    
      
    if start_date != None:
        end_date = start_date + timedelta(days=1)

    plantype = request.GET.get('plantype')
        
    amenities = request.GET.get('amenities')
    
    request.session['location'] = location
    
    location = request.session.get('location', None)
    
        
    db = MySQLdb.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

    cursor = db.cursor()
    
    plantype_join = []
    amenities_join = []
    getrating_join = []
    
    if plantype:
        plantype = plantype.split(',')
        plantype_join = ','.join(plantype)
    
    if amenities:
        amenities = amenities.split(',')
        amenities_join = ','.join(amenities)
        
        
    if getrating:
        getrating = getrating.split(',')
        getrating_join = ','.join(getrating)
    
    room_query = ""

    _and = False

    if maxattendees or minValue or maxValue or start_date or end_date:
        room_query = room_query + " WHERE " 
        
       
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "address={lat}&sensor={sen}&key={key}".format(
        lat=location,
        sen='True',
        key=settings.GOOGLE_API_KEY,
    )
    
    req = requests.get(base, params=params)
    res = req.json()
    
    if 'error_message' not in res.keys()  and res['status'] != 'ZERO_RESULTS':
        res_latitude = res['results'][0]['geometry']['location']['lat']
        res_longitude = res['results'][0]['geometry']['location']['lng']
    else:
        res_latitude = ''
        res_longitude = ''
    
     
        
    if minValue or maxValue:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + 'org_id_id in (select org_type_id from tbl_org) or ((cost_for_profit BETWEEN ' + str(minValue) + ' and ' + str(maxValue) + ') or (cost_for_non_profit BETWEEN ' + str(minValue) + ' and ' + str(maxValue) + '))'
        _and = True
        
    if start_date or end_date:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + 'id NOT IN (select room_book_id from '+ BookingUser._meta.db_table +' WHERE (start_date BETWEEN "'+ str(start_date) +'" AND "'+ str(end_date) +'") OR (end_date BETWEEN "'+ str(start_date) +'" AND "'+ str(end_date) +'"))'
        _and = True
    
        
    if maxattendees:
        if _and:
           room_query = room_query + " AND "
        room_query = room_query + '(capacity >= ' +str(maxattendees) + ') '
        _and = True 

    
    room_query = "SELECT * FROM "+ Facility._meta.db_table + " " + room_query
    room_query_table = ''    
    if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':       
        if not ne_lat and not sw_lng and not sw_lat and not ne_lng:
            ne_lat = str(res['results'][0]['geometry']['bounds']['northeast']['lat'])
            sw_lng = str(res['results'][0]['geometry']['bounds']['southwest']['lng'])
            sw_lat = str(res['results'][0]['geometry']['bounds']['southwest']['lat'])
            ne_lng = str(res['results'][0]['geometry']['bounds']['northeast']['lng'])
    
    
        if ne_lat and sw_lng and sw_lat and ne_lng:
            room_query_table = 'SELECT * \
    FROM tbl_facility \
    WHERE ST_CONTAINS(ST_GeomFromText("Polygon(('+ sw_lat +' '+ sw_lng +','+ sw_lat +' '+ ne_lng +','+ ne_lat +' '+ ne_lng +','+ ne_lat +' '+ sw_lng +','+ sw_lat +' '+ sw_lng +'))"), point(latitude, longitude));'

    
    data_list_table = []
    if  room_query_table:
        cursor.execute(room_query_table)

        desc = cursor.description 
        data_list_table = [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
        ]
    
    cursor.execute(room_query)

    desc = cursor.description 
    data_list = [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
        ]
    
    db.close()
    
    if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':
        facilities_list = Facility.objects.filter(id__in = [data['id'] for data in data_list_table]).order_by('facility_name')
    else:
        facilities_list = Facility.objects.all().order_by('facility_name')
    
           
    facilities_list = facilities_list.filter(id__in = [data['id'] for data in data_list]).order_by('facility_name')
    
    
    facility = []
    facility_cost = []
    amenities_list = []
    plantype_list = []
    
    
    getratinglist = [] 
    
    
    if getrating:
        for facilities in facilities_list:
            data = ReviewsModel.objects.filter(room_book=facilities).aggregate(Avg('rate')).get('rate__avg')
            if data:
                if str(round(float(data))) in getrating:
                    getratinglist.append((data, facilities.pk))
        
        facilities_list = facilities_list.filter(id__in = [data[1] for data in getratinglist])
    
       
    if amenities:
        for data in amenities:

            if data_list:
                for facilities in facilities_list:
                    if facilities.fac_amenities:
                        if data in facilities.fac_amenities:
                            
                            amenities_list.append(facilities.pk)
                            
        facilities_list = facilities_list.filter(id__in = [data for data in amenities_list])

    
    if plantype:
        for data in plantype:

            if data_list:
                for facilities in facilities_list:
                    if facilities.event_type:
                        if data in facilities.event_type:
                            
                            plantype_list.append(facilities.pk)
                            
        facilities_list = facilities_list.filter(id__in = [data for data in plantype_list])
        
    
    
    
    if sorttype:
        
        if sorttype == 'availability':
            facilities_list = facilities_list.filter(availability=True)
        elif sorttype == 'rating':
            for facilities in facilities_list:
                data = ReviewsModel.objects.filter(room_book=facilities).aggregate(Avg('rate')).get('rate__avg')
                facility.append((data, facilities.pk))
                
            facility = sorted(facility, key=lambda x:weighted(x[0]), reverse=True)
            ordering = 'FIELD(`id`, %s)' % ','.join(str(id[1]) for id in facility)
            facilities_list = facilities_list.filter(id__in = [data[1] for data in facility]).extra(
           select={'ordering': ordering}, order_by=('ordering',))
        elif sorttype == 'price_asc' or sorttype == 'price_des':
            if sorttype == 'price_des':
                order = 'ordering'
            else:
                order = '-ordering'
            for facilities in facilities_list:
                try:
                    cost_profit = int(facilities.cost_for_profit)
                except:
                    cost_profit = None
                facility_cost.append((cost_profit, facilities.pk))
            
                
            facility_cost_list = sorted(facility_cost, key=lambda x:weighted(x[0]), reverse=True)
            ordering = 'FIELD(`id`, %s)' % ','.join(str(id[1]) for id in facility_cost_list)
            facilities_list = facilities_list.filter(id__in = [data[1] for data in facility_cost_list]).extra(
           select={'ordering': ordering}, order_by=(order,))
        elif sorttype == 'capacity_asc' or sorttype == 'capacity_des':
            if sorttype == 'capacity_des':
                order = '-capacity'
            else:
                order = 'capacity'
            facilities_list = facilities_list.order_by(order)
        else:
            facilities_list = facilities_list.order_by(sorttype)
        
        
    if facilities_list:
        if len(facilities_list) > 8:
            paginator = Paginator(facilities_list, 8)
        else:
            paginator = Paginator(facilities_list, len(facilities_list))
      
        if len(facilities_list) > 8:
            try:
                facilities = paginator.page(page)
            except PageNotAnInteger:
                facilities = paginator.page(1)
            except EmptyPage:
                facilities = paginator.page(paginator.num_pages)
        else:
            facilities = facilities_list
    else:
        facilities = None
    
    if request.GET.get('update') == 'true' and facilities and len(facilities) < 8:
        facilities = None
        
    map_facility = facilities_list
    
    url = '?' + request.GET.copy().urlencode()
    
    marker = []
    if request.GET.get('marker') == 'true':
        for location_list in map_facility:
            pics = ImageSource.objects.filter(facility=location_list)
            pics_data = []
            for count, data in enumerate(pics, 1):
                pics_data.append({""+str(count)+"":"/media/"+str(data.image_file)})
            
            if pics.count() == 0:
                pics_data.append({"1":"/static/images/Detail0.jpg"})
                
            rating = ReviewsModel.objects.filter(room_book=location_list).aggregate(Avg('rate')).get('rate__avg') 
            if rating: 
                rating = round(float(rating))
            else:
                rating = 0
            marker.append({
              "facility":{
              "address": location_list.location_id.street_address_1.strip() + ' ' + location_list.location_id.city.strip() + ' ' + location_list.location_id.state.strip() + ' ' + location_list.location_id.zipcode.zipcode.strip(),
              "name":location_list.facility_name,
              "location_id": location_list.location_id.pk,
              "location_lat": location_list.latitude,
              "location_long": location_list.longitude,
              "price": location_list.cost_for_profit,
              "capacity": location_list.capacity,
                  "id":location_list.pk,
                  "rating": rating,
                  "imagesrc":pics_data
              }
        })
        return JsonResponse(marker, safe=False)
    
    if request.GET.get('update') == 'true':
        
        html = 'frontend/core/update_result.html'
        
    else:
        html = 'frontend/core/get_results.html'
        
            
    return render(request, html ,{'facilities':facilities,
                                                         'count':len(facilities_list),
                                                         'plantype':plantype_join,
                                                         'sorttype':sorttype,
                                                         'minattendees':minattendees,
                                                         'maxattendees':maxattendees,
                                                         'end_date':end_date,
                                                         'start_date':start_date,
                                                         'location':location,
                                                         'minValue':minValue,
                                                         'maxValue':maxValue,
                                                         'zipcode':zipcode,
                                                         'facilities_list':facilities_list,
                                                         'amenities':amenities_join,
                                                         'view': view,
                                                         'map_facility':map_facility,
                                                         'url':str(url),
                                                         'zoom':zoom,
                                                         'page':page,
                                                         'ne_lat':ne_lat,
                                                        'sw_lng':sw_lng,
                                                        'sw_lat': sw_lat,
                                                        'ne_lng':ne_lng,
                                                         'getrating':getrating_join})

def roomview(request, id):
    facility = Facility.objects.get(pk=id)
    
    roomdata = ImageSource.objects.filter(facility=id)
    reviews = ReviewsModel.objects.filter(room_book=facility)   
    
    
    try:
        booking = BookingUser.objects.filter(room_book=facility.pk)
    except BookingUser.DoesNotExist:
        booking = None
    
    date_generated = []
    date_not_available = []

    
    for date in booking:
        start = date.start_date
        end = date.end_date
        if round(((end-start).days*24) + ((end-start).seconds/3600)) > 23:
            date_not_available.append(start + relativedelta(hours=0))
            
        for x in range(0, round(((end-start).days*24) + ((end-start).seconds/3600))):
            date_generated.append(start + relativedelta(hours=+x))
            
    
      
    
    return render(request, 'frontend/core/roomdetail.html',{'facility':facility,
                                                            'roomdata':roomdata,
                                                            'date_generated':date_generated,
                                                            'reviews':reviews[:3],
                                                            'date_not_available':date_not_available,
                                                            'reviews_count':reviews.count()})    
    
    
@login_required(login_url='/accounts/register/')   
def roomviewreviews(request, id):
    if request.method == "POST":
        message=request.POST.get('addComment')
        if not message:
            return redirect('frontend:roomview', id=id)
        rate = request.POST.get('star')
        room_book = Facility.objects.get(pk=id)
        ReviewsModel.objects.create(message=message,room_book=room_book,created_by_id=request.user, rate=rate)
        
        reviews = ReviewsModel.objects.filter(room_book=room_book).aggregate(Avg('rate')).get('rate__avg')
        room_book.rating = reviews
        room_book.save()
    
    return redirect('frontend:roomview', id=id)

@login_required(login_url='/accounts/register/')
def ReportView(request):
    

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        subject = ''.join(data.get('subject').splitlines())
        subject =  '[Report form] ' + subject
        
        send_mail(subject, data.get('message'), settings.EMAIL_HOST_USER, [data.get('email')], fail_silently=False)
        
        ReportModel.objects.create(name=data.get('name'),
                                   email=data.get('email'),
                                   message=data.get('message'),
                                   path=request.POST.get('currenturl'),
                                   model_type='room',
                                   created_by_id=request.user)
    
    return HttpResponseRedirect(request.GET.get('next'))


def locationaddress(request):    
    
    locationaddress = []
    
    citylocations = Location.objects.all().annotate(citydata=Concat('street_address_1','city', 'state', 'zipcode__zipcode')).values('street_address_1','location_name','city','state','zipcode__zipcode','citydata').distinct()
    
    for location in citylocations:
        data = {  
            'data': {
                'type': 'city',
                'value': location['street_address_1'].strip() + ' ' + location['city'].strip() + ' ' + location['state'].strip() + ' ' + location['zipcode__zipcode'].strip()
                },          
            'value' : location['city'].strip() + ' ' + location['state'].strip() + ' ' + location['zipcode__zipcode'].strip(),
            'type' : 'landmark',
            }
        locationaddress.append(data)   
    
    return HttpResponse(json.dumps(locationaddress), content_type="application/json")

@login_required(login_url='/accounts/register/')
def Bookinguser(request):
    
    if request.user.is_superuser:
        return redirect('backend:booking_index')
    
    
    notification_latest = NotificationModel.objects.filter(is_read=IS_NOT_READ, to_user_id=request.user,model_type='booking')
    
    for notify in notification_latest:
        notify.is_read = IS_READ
        notify.save()
        
            
    booking_list_array = []
    bookings = BookingUser.objects.filter(booking_key__isnull=False,user_subscribe=request.user).filter(Q(status=QUEUE)|Q(status=CONFIRMED)).values('booking_key','user_subscribe','status').distinct()
    
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
    
    return render(request, 'frontend/core/bookingdetails.html',{'booking':bookings,'booking_list_array':booking_list_array})

# @method_decorator(login_required, name='dispatch')
class partnerCreateView(FormView):

    model = Proposal
    form_class = ProposalForm
    template_name = 'frontend/core/proposal_form.html'

    def get_success_url(self):
        url = reverse('frontend:newproposal')
        return url
    

    def form_valid(self, form):
        data = form.cleaned_data
        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.digits
        password = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
        user = User.objects.create(email=data.get('CompanyEmail'),
                                            first_name=data.get('CompanyName'),
                                            last_name=' ',
                                            username=data.get('CompanyEmail'),
                                            password=make_password(password),
                                            address=data.get('HQAddress'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            type_id=GUEST)


        form.instance.user = user
        form.save()
        messages.add_message(self.request, messages.INFO, 'Will review your details and contact you shortly.')
        
        
        return super(partnerCreateView, self).form_valid(form)
    


@login_required(login_url='/accounts/register/')
def checkstatus(request):
    proposal_list = Proposal.objects.filter(user = request.user)
    context = {'proposals': proposal_list}
    return render(request, 'frontend/core/checkstatus.html', context)

    
@login_required(login_url='/accounts/register/')
def booking_pdf(request, id):
    try:
        booking = BookingUser.objects.select_related().filter(booking_key=id)
    except BookingUser.DoesNotExist:
        return redirect('frontend:search')
    
    dates = []
    price = 0
        
    for index, data in enumerate(booking):
        dates.append(str(data.start_date.strftime('%a. %d %B %Y, %I:%M %p')) + ' - ' + str(data.end_date.strftime('%a. %d %B %Y, %I:%M %p')))
        price += int(data.amount)
            
    return render(request, 'frontend/core/invoice.html', 
                        {
                         'booking': booking,
                         'dates':dates,
                         'price':price,
                         'gkey':settings.GOOGLE_API_KEY_FRONT
                        })
    
    

    
def viewactivities(request):

    return render(request, 'frontend/core/viewactivities.html')

@login_required(login_url='/accounts/register/')   
def addspace(request):
        
    try:
        spaceadd = AddSpaceModel.objects.get(created_by_id=request.user, complete=False)
    except AddSpaceModel.DoesNotExist:
        spaceadd = None
        
        
    if request.method == "POST":
        spaceadd = AddSpaceModel.objects.get_or_create(created_by_id=request.user, complete=False)
        return redirect('frontend:addspacelocation')
    
        
    return render(request, 'provider/add_space.html')

@login_required(login_url='/accounts/register/')
def addspacelocation(request):
    
    try:
        spaceadd = AddSpaceModel.objects.filter(created_by_id=request.user, complete=False).first()
    except AddSpaceModel.DoesNotExist:
        return redirect('frontend:addspace')
    
    if request.method == "POST":
        spaceadd.street_address_1 = request.POST.get('street_address_1')
        spaceadd.street_address_2 = request.POST.get('street_address_2')
        spaceadd.city = request.POST.get('city')
        spaceadd.state = request.POST.get('state')
        
        zip_code, created = Geolocation.objects.get_or_create(zipcode=request.POST.get('zipcode'))
        
        spaceadd.zipcode = zip_code
        spaceadd.country = request.POST.get('country')
        spaceadd.save()
        
        return redirect('frontend:addspaceabout')

    return render(request, 'provider/addspacelocation.html',{'spaceadd':spaceadd})


def addspacedetail(request):
    
    if request.method == "POST":
        
        data = json.loads(request.POST.get('form'))['0']
        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.digits
        password = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
        user = User.objects.create(email=data.get('CompanyEmail'),
                                            first_name=data.get('CompanyName'),
                                            last_name=' ',
                                            username=data.get('CompanyEmail'),
                                            password=make_password(password),
                                            address=data.get('HQAddress'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            type_id=GUEST)
         
        spaceadd, created = AddSpaceModel.objects.get_or_create(created_by_id=user, complete=False)
        spaceadd.street_address_1 = data.get('HQAddress')
        spaceadd.city = data.get('city')
        spaceadd.state = data.get('state')
         
        zip_code, created = Geolocation.objects.get_or_create(zipcode=data.get('city'))
      
        spaceadd.zipcode = zip_code
        spaceadd.country = 'us'
        spaceadd.save()
        
        
        formabout = AddAboutSpaceForm(data, instance=spaceadd)
        
        if formabout.is_valid:
            formabout.save()
            
        formactivities = AddSpaceForm(data, instance=spaceadd)
        
        if formactivities.is_valid:
            formactivities.save()
            
        spaceadd.complete = True
        spaceadd.save()
             
        return HttpResponse('saved')

    return render(request, 'provider/addspacedetail.html',{})

def addspacedetailmessage(request):
    
    if request.method == "POST":
        messages.add_message(request, messages.INFO, 'Will review your details and contact you shortly.')
            
        return redirect('frontend:addspacedetail')
    
    return redirect('core:home')

@login_required(login_url='/accounts/register/')
def addspaceabout(request):
        
    try:
        spaceadd = AddSpaceModel.objects.filter(created_by_id=request.user, complete=False).first()
    except AddSpaceModel.DoesNotExist:
        return redirect('frontend:addspace')
    
    
    if request.method == "POST":
        
        form = AddAboutSpaceForm(request.POST, instance=spaceadd)
        
        if form.is_valid:
            form.save()
            return redirect('frontend:addspacephotos')
    else:
        form = AddAboutSpaceForm(instance=spaceadd)
        
    return render(request, 'provider/addspaceabout.html',{'form':form})

@login_required(login_url='/accounts/register/')
def addspacephotos(request):
        
    try:
        spaceadd = AddSpaceModel.objects.get(created_by_id=request.user, complete=False)
    except AddSpaceModel.DoesNotExist:
        return redirect('frontend:addspace')
        
    try:
        spaceaddimage = AddSpaceImagesModel.objects.filter(space=spaceadd)
    except AddSpaceModel.DoesNotExist:
        spaceaddimage = None
        
    
    
    if request.method == "POST":
        
        datafiles = request.FILES.getlist('imageadd')
        
        for data in datafiles:
            AddSpaceImagesModel.objects.create(image_file=data,space=spaceadd)
            
        return redirect('frontend:addspaceactivities')

    return render(request, 'provider/addspacephotos.html',{'spaceaddimage':spaceaddimage})

@login_required(login_url='/accounts/register/')
def addspaceactivities(request):
    
    try:
        spaceadd = AddSpaceModel.objects.get(created_by_id=request.user, complete=False)
    except AddSpaceModel.DoesNotExist:
        return redirect('frontend:addspace')
    
    if request.method == 'POST':
        form = AddSpaceForm(request.POST, instance=spaceadd)
                
        if form.is_valid:
            form.save()
            return redirect('frontend:addspaceconfirm')
    else:
        form = AddSpaceForm(instance=spaceadd)

    return render(request, 'provider/addspaceactivities.html',{'form':form})

@login_required(login_url='/accounts/register/')
def addspaceconfirm(request):
    
    try:
        spaceadd = AddSpaceModel.objects.get(created_by_id=request.user, complete=False)
    except AddSpaceModel.DoesNotExist:
        return redirect('frontend:addspace')
        
    try:
        spaceaddimage = AddSpaceImagesModel.objects.filter(space=spaceadd)
    except AddSpaceModel.DoesNotExist:
        spaceaddimage = None
    
    if request.method == 'POST':
        if request.POST.get('agreeconfirm') == 'on':
            spaceadd.complete = True
            spaceadd.save()
            
            messages.add_message(request, messages.INFO, 'your application is in processing will update to you soon.')
            
            return redirect('core:home')

    return render(request, 'provider/addspaceconfirm.html',{'spaceadd':spaceadd,'spaceaddimage':spaceaddimage})



def hostdetail(request,id):
    
    
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        user = None
        
    if user and user.type_id == PARTNER:
        
        Partners.objects.get_or_create(userID_id=id)
    
    try:
        partner = Partners.objects.select_related().get(userID_id=id)
    except Partners.DoesNotExist:
        return redirect('core:home')
       
    try:
        facility = Facility.objects.filter(partner=partner.userID, event_type__isnull=False)
    except Facility.DoesNotExist:
        facility = None
        
    event_list = EventTypeModel.objects.all()
           
    location = 'United States'
        
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "address={lat}&sensor={sen}&key={key}".format(
        lat=location,
        sen='True',
        key=settings.GOOGLE_API_KEY,
    )
    
    req = requests.get(base, params=params)
    res = req.json()   
        
    res_latitude = res['results'][0]['geometry']['location']['lat']
    res_longitude = res['results'][0]['geometry']['location']['lng']
    

    return render(request, 'frontend/core/hostdetail.html',{'partner':partner,
                                                            'facility':facility,
                                                            'res_latitude':res_latitude,
                                                            'res_longitude':res_longitude})
 
@login_required(login_url='/accounts/register/')  
def generatePDF(request, id):
    now = datetime.datetime.now()
    host = request.get_host()
    url = redirect('frontend:booking_pdf', id=id).url
    cookies = request.COOKIES
    
    try:
        booking = BookingUser.objects.select_related().filter(booking_key=id)
    except BookingUser.DoesNotExist:
        return redirect('frontend:search_filter')

    session = requests.Session()
    pdf = session.get('http://{}{}'.format(host, url), cookies=cookies)

    timestamp = now.strftime('%H-%M %d-%m-%Y')
    pdf_name = 'booking_invoice_{}_{}.pdf'.format('_'.join(booking[0].room_book.facility_name.split(' ')), timestamp)
    pdf_file = HTML(string=pdf.text).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename={}.pdf'.format(pdf_name)

    return response

@login_required(login_url='/accounts/register/')
def get_quote_booking(request):


    error = 0
    dateissue = 0
    
    default_msg = 'Make sure your dates do not overlap '
    withmsg = ' with '
    
    dates = ''
    response = ''
    
    datecheck = []
    
    dateoverlapcheck = []
    
    for data in json.loads(request.POST.get('dateArry')):
        startdate = data['start_time_book']
        
        startdate = mktime_tz(parsedate_tz(startdate))
        startdate = datepicker(1970, 1, 1) + timedelta(seconds=startdate)
        startdate = datepicker.strftime(startdate,'%a %d %B %Y %I:00 %p')
        
        startutc_dt = parser.parse(startdate)
        
        
        
        
        enddate = data['end_time_book']
        
        
        
        enddate = mktime_tz(parsedate_tz(enddate))
        enddate = datepicker(1970, 1, 1) + timedelta(seconds=enddate)
        enddate = datepicker.strftime(enddate,'%a %d %B %Y %I:00 %p')
        endutc_dt = parser.parse(enddate)
        
            
            
        for x in range(0, round(((endutc_dt-startutc_dt).days*24) + ((endutc_dt-startutc_dt).seconds/3600))):
            
            if (startutc_dt + relativedelta(hours=+x)) not in dateoverlapcheck:
                
                dateoverlapcheck.append(startutc_dt + relativedelta(hours=+x))
            else:
                dateissue += 1
            
        
        booking = BookingUser.objects.filter(room_book_id= request.POST.get('Id')).filter(Q(start_date__range=[startutc_dt,endutc_dt])|Q( end_date__range=[startutc_dt,endutc_dt]))
      
        
        if booking.count() > 0:
            error += 1
            if error > 1:
                dates = dates + ', '
            dates = dates + datepicker.strftime(startutc_dt,'%a %d %B %Y %I:00 %p') + ' - ' + datepicker.strftime(endutc_dt,'%I:00 %p')
    
    
    if dateissue > 0:
        response = default_msg
        
        
    if error >  0:
        response = default_msg + withmsg + dates
    
    return HttpResponse(response)




@login_required
def passwordreset(request):
    
    if request.method == 'POST':
        request.user.password = make_password(request.POST.get('password'))
        request.user.save()
        
        messages.add_message(request, messages.INFO, 'Changed successfully')
        
        return redirect('core:userprofile')


def profile_save(request):
    
    app_label = request.POST.get('app_label')
    
            
    request.user.profile_file = request.FILES.get('mypicture')
    request.user.save()
    
    return render(request, 'frontend/core/'+ app_label +'/'+ app_label +'.html')
    

@login_required
def contentdetail(request):
    
    model_name = request.GET.get('model')
    
    id = request.GET.get('id')
    
    next = request.GET.get('next')
    
    facility = None
    
    board = request.GET.get('board')
    
    boarddata = None
    
    if board:
        boarddata = Board.objects.get(pk=board)
        app_modal = 'edit_' + model_name
    else:
        app_modal = 'add_' + model_name
    
    if id:
        facility = Facility.objects.get(pk=id)
        if request.GET.get('update') != 'true':
            app_modal =  model_name
        
    return render(request, 'frontend/core/'+ model_name +'/'+ app_modal +'.html',{'facility':facility,'next':next,'boarddata':boarddata})



@login_required(login_url='/accounts/register/')
def messagehost(request):
    
    if request.method == "POST":
        TOTAL_FORMS = request.POST.get('date_extend_total_forms')
        booking_dates_list = '' 
        for form_num in range(1,(int(TOTAL_FORMS)+1)):
            booking_dates_list += request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("start_time-"+str(form_num)) +'-' +request.POST.get("start_date-"+str(form_num)) + ' ' + request.POST.get("end_time-"+str(form_num))
            if form_num != (int(TOTAL_FORMS)):
                booking_dates_list += ','
            
        timeflexibleval = False
        visitscheduleval = False   
        if request.POST.get('timeflexible') == 'on':
            timeflexibleval = True
        if request.POST.get('visitschedule') == 'on':
            visitscheduleval = True
            
        roomdetail = Facility.objects.get(pk=request.POST.get('roomID'))
        
        messagedata = HostMessage.objects.create(user_subscribe=request.user,
                                                room_book = roomdetail,
                                                booking_dates = booking_dates_list,
                                                timeflexible = timeflexibleval,
                                                visitschedule = visitscheduleval,
                                                attendees = request.POST.get('attendnumber'),
                                                message_request = request.POST.get('message_request'),
                                                host_user_id = roomdetail.partner_id,
                                                about_you = request.POST.get('about_you'))
        current_site = get_current_site(request)
        context = {
            'user':request.user, 'domain':current_site.domain,
            'url':'/room/view/',
            'room':roomdetail,
            "messagedata":messagedata,
        }
        message = render_to_string('frontend/core/message_host_email.html', context)
        
        mail_subject = 'Query related to Room #' + roomdetail.pk 
        to_email = roomdetail.partner.email

            
        email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
        html_email = render_to_string('frontend/core/message_host_email.html',context)
        email_message.attach_alternative(html_email, 'text/html')
        email_message.send()
        
        messages.add_message(request, messages.INFO, 'Message sent successfully to Host, '+roomdetail.partner.first_name + ' '+roomdetail.partner.last_name)
        
        
   
        return HttpResponseRedirect(request.POST.get('next'))
        
        
    return HttpResponseRedirect('/')



@csrf_exempt
def feedbackform(request):
    
    try:
        feedbackuser = User.objects.get(email=json.loads(request.POST.get('feedback')).get('feedbackemail'))
    except User.DoesNotExist:
        feedbackuser = None
        
    if not feedbackuser:
        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.digits
        password = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
        feedbackuser = User.objects.create(email=json.loads(request.POST.get('feedback')).get('feedbackemail'),
                                            first_name=json.loads(request.POST.get('feedback')).get('feedbackemail'),
                                            last_name=' ',
                                            username=json.loads(request.POST.get('feedback')).get('feedbackemail'),
                                            password=make_password(password),
                                            type_id=GUEST)
        
    feedback = FeedbackPageForm.objects.create(note=json.loads(request.POST.get('feedback')).get('note'),user_subscribe=feedbackuser,url = json.loads(request.POST.get('feedback')).get('url'))
    format, imgstr = json.loads(request.POST.get('feedback')).get('img').split(';base64,') 
    ext = format.split('/')[-1] 
    
    data = ContentFile(base64.b64decode(imgstr), name= str(feedback.pk) + '.' + ext)
    feedback.feedback_image = data
    feedback.save()
    current_site = get_current_site(request)
    superadmin = User.objects.filter(type_id = SUPER_ADMIN).first() 
    context = {
        'user':request.user, 'domain':current_site.domain,
        "feedback":feedback,'superadmin':superadmin,
    }
    message = render_to_string('frontend/core/feedback_email.html', context)
    
    mail_subject = 'Feed back related to ' + json.loads(request.POST.get('feedback')).get('url')
    to_email = superadmin.email

        
    email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
    html_email = render_to_string('frontend/core/feedback_email.html',context)
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
    
    
    return HttpResponse(status=200)


def validemail(request):
    try:
        user = User.objects.get(email=request.POST.get('email'))
        return HttpResponse('notvalid')
    except User.DoesNotExist:
        return HttpResponse('valid')
    