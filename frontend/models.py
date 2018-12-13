from django.db import models

from accounts.models import *
import uuid
from frontend.constant import *
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import requests
from urllib import parse
import random 
from django.conf import settings

STATE = [
    (INACTIVE,'InActive'),
    (ACTIVE,'Active')
    ]

        
ORG_TYPE = [
    ('for_profit','Profit'),
    ('non_profit','Non profit')
    
    ]



def get_default_user():
    user = User.objects.filter(type_id=SUPER_ADMIN).first()
    return user.pk

class Geolocation(models.Model):
    geo_id = models.AutoField(primary_key=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
         return str(self.zipcode)
        
class LocationType(models.Model):
    loc_type_id = models.AutoField(primary_key=True)
    loc_cat_id = models.IntegerField(blank=True, null=True)
    loc_type = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
         return self.loc_type
        
class LocationCatergory(models.Model):
    loc_cat_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        managed = True 
        db_table = 'tbl_location_category'  

    def __str__(self):
         return self.category    
        
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL,null=True,blank=True)
    location_name = models.CharField(max_length=500,null=True,blank=True)
    location_website = models.CharField(max_length=500,null=True,blank=True)
    street_address_1 = models.CharField(max_length=256,null=True,blank=True)
    street_address_2 = models.CharField(max_length=256,null=True,blank=True)
    city = models.CharField(max_length=256,null=True,blank=True)
    state = models.CharField(max_length=256,null=True,blank=True)
    zipcode = models.ForeignKey(Geolocation, on_delete=models.SET_NULL,null=True,blank=True)
    contact_no = models.CharField(max_length=100,null=True,blank=True)
    hours = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    sun_open_time = models.CharField(max_length=100,null=True,blank=True)
    sun_close_time = models.CharField(max_length=100,null=True,blank=True)
    mon_open_time = models.CharField(max_length=100,null=True,blank=True)
    mon_close_time = models.CharField(max_length=100,null=True,blank=True)
    tue_open_time = models.CharField(max_length=100,null=True,blank=True)
    tue_close_time = models.CharField(max_length=100,null=True,blank=True)
    wed_open_time = models.CharField(max_length=100,null=True,blank=True)
    wed_close_time = models.CharField(max_length=100,null=True,blank=True)
    thu_open_time = models.CharField(max_length=100,null=True,blank=True)
    thu_close_time = models.CharField(max_length=100,null=True,blank=True)
    fri_open_time = models.CharField(max_length=100,null=True,blank=True)
    fri_close_time = models.CharField(max_length=100,null=True,blank=True)
    sat_open_time = models.CharField(max_length=100,null=True,blank=True)
    sat_close_time = models.CharField(max_length=100,null=True,blank=True)
    

    class Meta:
        managed = True 
        db_table = 'tbl_location' 

    def __str__(self):
         return self.location_name  
        

class Partners(models.Model):
    userID = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length  = 255)
    CompanyEmail = models.EmailField(max_length  = 254)
    HQAddress = models.CharField(max_length  = 255)
    state_id = models.IntegerField(choices=STATE, default= INACTIVE)
    org_type = models.IntegerField(blank=True, null=True, choices=ORG_TYPE)
    
    class Meta:
        verbose_name_plural = 'Partners'

    def __str__(self):
         return self.CompanyName  
     
class OrgType(models.Model):
    org_type_id = models.IntegerField()
    orgtype = models.IntegerField(blank=True, null=True, choices=ORG_TYPE)
    orgname = models.CharField(max_length=500,blank=True, null=True)
    orgcount = models.CharField(max_length=100,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tbl_org'
        
    def __str__(self):
        return self.orgtype

    
class EventTypeModel(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    eventtype = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    eventype_image = models.ImageField(upload_to="images/event/")
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    class Meta:
        managed = True
        db_table = 'tbl_event'
        verbose_name = 'Event Type'
        
    def __str__(self):
        return self.eventtype
  
class Facility(models.Model):
    id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=100, blank=True, null=True)
    facility_information = models.TextField(blank=True, null=True)
    parking_spaces = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.CharField(max_length=100, blank=True, null=True)
    none_refundable_fee = models.CharField(max_length=100, blank=True, null=True)
    cost_for_profit = models.CharField(max_length=100, blank=True, null=True)
    cost_for_non_profit = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_rental_clean_dep_no_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_rental_clean_dep_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_non_ref_hr_mtn = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc = models.CharField(max_length=100, blank=True, null=True)
    staff_fee = models.CharField(max_length=100, blank=True, null=True)
    fac_amenities = models.CharField(max_length=500, blank=True, null=True)
    note_1 = models.TextField(blank=True, null=True)
    note_2 = models.TextField(blank=True, null=True)
    note_3 = models.TextField(blank=True, null=True)
    res_1 = models.TextField(blank=True, null=True)
    res_2 = models.TextField(blank=True, null=True)
    res_3 = models.TextField(blank=True, null=True)
    fac_surf_type = models.CharField(max_length=100, blank=True, null=True)
    fac_feature = models.CharField(max_length=100, blank=True, null=True)
    fee_based_amenities = models.CharField(max_length=100, blank=True, null=True)
    event_type = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    availability = models.BooleanField(default="True")
    location_id = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    org_id = models.ForeignKey(OrgType, on_delete=models.SET_NULL, blank=True, null=True)  
    partner = models.ForeignKey(User, blank=True, null=True,related_name="partner",on_delete=models.SET_NULL,limit_choices_to={'type_id': PARTNER})
    assigned_to = models.ForeignKey(User, blank=True, null=True,related_name="assigned_to",on_delete=models.SET_NULL,limit_choices_to={'type_id': SPACE_ADMIN})
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    class Meta:
        managed = True
        db_table = 'tbl_facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
         return str(self.facility_name)  
     
    def save(self, *args, **kwargs):

        if self.location_id.street_address_1 and self.location_id.city and self.location_id.state and self.location_id.zipcode:
            
            location = self.location_id.street_address_1 + ' ' + self.location_id.city + ' ' + self.location_id.state + ' ' + self.location_id.zipcode.zipcode
            sensor = 'true'
            
            base = "https://maps.googleapis.com/maps/api/geocode/json?"
            params = "address={lat}&sensor={sen}&key={key}".format(
                lat=location,
                sen=sensor,
                key=settings.GOOGLE_API_KEY,
            )
            
            req = requests.get(base, params=params)
            res = req.json()
            
            if 'error_message' not in res.keys() and res['status'] != 'ZERO_RESULTS':
                min = .999998
                max = 1.000002
                self.latitude = res['results'][0]['geometry']['location']['lat']
                self.longitude = res['results'][0]['geometry']['location']['lng']
                
                latupdate = 0
                lngupdate = 0
                
                for data in Facility.objects.all():
                    if data.latitude and float(data.latitude) == self.latitude:
                        latupdate += 1
                        if latupdate == 1:
                            self.latitude = self.latitude * ((random.random() * (max - min)) + min)
                            latupdate = 0

                    if  data.longitude and float(data.longitude) == self.longitude:
                        lngupdate += 1
                        if lngupdate == 1:
                            self.longitude = self.longitude * ((random.random() * (max - min)) + min)
                            lngupdate = 0
                        
        super(Facility, self).save(*args, **kwargs)

def get_member_upload_to(instance, filename):
    new_filename = '{}'.format(filename)
    return "images/rooms/{}/{}".format(instance.facility.id, new_filename)



    
class ImageSource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(upload_to=get_member_upload_to)
    image_url = models.URLField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    extension = models.CharField(max_length=100, blank=True, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user) 

    class Meta:
        managed = True
        
    def save(self, *args, **kwargs):

        if self.image_url and not self.image_file:
            r = requests.get(self.image_url)

            if r.status_code == requests.codes.ok:
    
                img_temp = NamedTemporaryFile(delete = True)
                img_temp.write(r.content)
                img_temp.flush()
        
                img_filename = parse.urlsplit(self.image_url).path[1:]
                image_name = img_filename.split('/')
                self.image_file.save(image_name[-1], File(img_temp), save = True)
            
        super(ImageSource, self).save(*args, **kwargs)
    
    
class ReportModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=200, blank=True, null=True)
    model_type = models.CharField(max_length=100, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        managed = True
        verbose_name = 'Report'
        

PROPOSAL_TYPE = [
    (ACCEPT,'Active'),
    (DECLINE,'Decline')
    
    ]  
        
class AddSpaceModel(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    approval =  models.IntegerField(default=0, choices=PROPOSAL_TYPE)
    facility_name = models.CharField(max_length=100, blank=True, null=True)
    facility_information = models.TextField(blank=True, null=True)
    parking_spaces = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.CharField(max_length=100, blank=True, null=True)
    none_refundable_fee = models.CharField(max_length=100, blank=True, null=True)
    cost_for_profit = models.CharField(max_length=100, blank=True, null=True)
    cost_for_non_profit = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_rental_clean_dep_no_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_rental_clean_dep_alc = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc_non_ref_hr_mtn = models.CharField(max_length=100, blank=True, null=True)
    fac_cost_misc = models.CharField(max_length=100, blank=True, null=True)
    staff_fee = models.CharField(max_length=100, blank=True, null=True)
    note_1 = models.TextField(blank=True, null=True)
    note_2 = models.TextField(blank=True, null=True)
    note_3 = models.TextField(blank=True, null=True)
    res_1 = models.TextField(blank=True, null=True)
    res_2 = models.TextField(blank=True, null=True)
    res_3 = models.TextField(blank=True, null=True)
    fac_surf_type = models.CharField(max_length=100, blank=True, null=True)
    fac_feature = models.CharField(max_length=100, blank=True, null=True)
    fee_based_amenities = models.CharField(max_length=100, blank=True, null=True)
    sun_open_time = models.CharField(max_length=100,null=True,blank=True)
    sun_close_time = models.CharField(max_length=100,null=True,blank=True)
    mon_open_time = models.CharField(max_length=100,null=True,blank=True)
    mon_close_time = models.CharField(max_length=100,null=True,blank=True)
    tue_open_time = models.CharField(max_length=100,null=True,blank=True)
    tue_close_time = models.CharField(max_length=100,null=True,blank=True)
    wed_open_time = models.CharField(max_length=100,null=True,blank=True)
    wed_close_time = models.CharField(max_length=100,null=True,blank=True)
    thu_open_time = models.CharField(max_length=100,null=True,blank=True)
    thu_close_time = models.CharField(max_length=100,null=True,blank=True)
    fri_open_time = models.CharField(max_length=100,null=True,blank=True)
    fri_close_time = models.CharField(max_length=100,null=True,blank=True)
    sat_open_time = models.CharField(max_length=100,null=True,blank=True)
    sat_close_time = models.CharField(max_length=100,null=True,blank=True)
    fac_amenities = models.CharField(max_length=500, blank=True, null=True)
    event_type = models.CharField(max_length=500, blank=True, null=True)
    location_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL,null=True,blank=True)
    location_name = models.CharField(max_length=500,null=True,blank=True)
    street_address_1 = models.CharField(max_length=256,null=True,blank=True)
    street_address_2 = models.CharField(max_length=256,null=True,blank=True)
    city = models.CharField(max_length=256,null=True,blank=True)
    state = models.CharField(max_length=256,null=True,blank=True)
    zipcode = models.ForeignKey(Geolocation, on_delete=models.SET_NULL,null=True,blank=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        managed = True
        verbose_name = 'Space'
      

class Proposal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length  = 255)
    CompanyEmail = models.EmailField(max_length  = 254)
    HQAddress = models.CharField(max_length  = 255)
    city = models.CharField(max_length  = 255)
    state = models.CharField(max_length  = 255)
    zipcode = models.CharField(max_length  = 255)
    Vision = models.TextField(max_length  = 400)
    state_id = models.IntegerField(default=0, choices=PROPOSAL_TYPE)
    
    class Meta:
        verbose_name_plural = 'Proposal'

    def __str__(self):
         return self.CompanyName 
     
     

        
class AmenityType(models.Model):
    amenity_type_id = models.AutoField(primary_key=True)
    amenity_type = models.CharField(max_length=100,null=True,blank=True)
    amenity_icon = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
         return self.amenity_type
     
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User, on_delete=models.CASCADE)
    board_name = models.CharField(max_length = 255)
    event_type = models.ForeignKey(EventTypeModel, blank=True, null=True,on_delete=models.SET_NULL)
    location = models.CharField(max_length = 255)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
         return self.board_name
     
class HostMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Facility, on_delete=models.CASCADE)    
    booking_dates = models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    attendees = models.CharField(max_length=25,null=True,blank=True)
    timeflexible = models.BooleanField(default=False)
    visitschedule = models.BooleanField(default=False)
    message_request = models.TextField(blank=True, null=True)
    about_you = models.TextField(null=True,blank=True)
    host_user = models.ForeignKey(User,related_name='host_user', on_delete=models.CASCADE)

    class Meta:
        managed = True
        


def get_space_upload_to(instance, filename):
    new_filename = '{}'.format(filename)
    return "images/space/{}/{}".format(instance.space.id, new_filename)


class AddSpaceImagesModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(upload_to=get_space_upload_to)
    image_url = models.URLField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    extension = models.CharField(max_length=100, blank=True, null=True)
    space = models.ForeignKey(AddSpaceModel, on_delete=models.CASCADE)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user) 

    class Meta:
        managed = True
        verbose_name = 'Space Images'
        
    def save(self, *args, **kwargs):

        if self.image_url and not self.image_file:
            r = requests.get(self.image_url)

            if r.status_code == requests.codes.ok:
    
                img_temp = NamedTemporaryFile(delete = True)
                img_temp.write(r.content)
                img_temp.flush()
        
                img_filename = parse.urlsplit(self.image_url).path[1:]
                image_name = img_filename.split('/')
                self.image_file.save(image_name[-1], File(img_temp), save = True)
            
        super(AddSpaceImagesModel, self).save(*args, **kwargs)