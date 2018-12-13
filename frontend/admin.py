from django.contrib import admin

from frontend.models import *
from django import forms
import os
from django.utils.html import format_html

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import *
from django.conf.urls import url
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources

from import_export import widgets

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

# class FileModelForm(forms.ModelForm):
#     class Meta:
#         model = FileModel
#         fields = ['path',]
#         widgets = {
#             'path': forms.FileInput(attrs={'multiple': 'multiple'}),
#         }
    
class LocationWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(location_name = value)[0]

class FacilityResource(resources.ModelResource):
    
    
    location_id = fields.Field(
        column_name='location_name',
        attribute='location_id',
        widget=LocationWidget(Location, 'location_name')) 
    

    class Meta:
        model = Facility
        import_id_fields = ('facility_name',)
        fields = ('facility_name', 
                  'facility_information',
                  'parking_spaces', 
                  'capacity',
                  'location_id',
                  'none_refundable_fee',
                  'cost_for_profit',
    'cost_for_non_profit',
    'fac_cost_misc_alc',
    'fac_cost_misc_rental_clean_dep_no_alc',
    'fac_cost_misc_rental_clean_dep_alc',
    'fac_cost_misc_non_ref_hr_mtn',
    'fac_cost_misc',
    'staff_fee',
    'fac_amenities',
    'note_1',
    'note_2' ,
    'note_3',
    'res_1',
    'res_2',
    'res_3',
    'fac_surf_type',
    'fac_feature',
    'event_type',
    'fee_based_amenities',)
        
@admin.register(Facility)
class FacilityAdmin(ImportExportModelAdmin):
    resource_class = FacilityResource
    
    add_form_template = 'backend/add_pics.html'
    
    list_display = ('facility_name', 'capacity', 'fac_amenities','event_type','assigned_to', 'availability')
    search_fields = ('facility_name', 'capacity', 'cost_for_profit')
    
    def save_model(self, request, obj, form, change):
        file = request.FILES.getlist('upload_button')   
        obj.save()
        if file:
            for filedata in file:
                ImageSource.objects.create(model_id=obj, model_type="room_data",        
                title=filedata._name ,
                extension=filedata._name.split('.')[-1],
                size=filedata._size,
                created_by_id = request.user,
                path = filedata
                )
                
    
class ImageSourceWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(facility_name = value)[0]
                
class ImageSourceResource(resources.ModelResource):
    
    
    facility = fields.Field(
        column_name='facility',
        attribute='facility',
        widget=ImageSourceWidget(Facility, 'facility_name')) 
    

    class Meta:
        model = ImageSource
        import_id_fields = ('facility',)
        fields = ('facility', 
                  'image_url',)
        

@admin.register(ImageSource)
class ImageSourceAdmin(ImportExportModelAdmin):
    resource_class = ImageSourceResource
    
    def image_tag(self, obj):
        return format_html('<img src="/media/{}"  width="150" height="150" />'.format(obj.image_file))

    image_tag.short_description = 'Image'

    list_display = ['image_tag','facility']
    fieldsets = (
        (None, {'fields': ('image_file','image_url', 'facility', 'created_by_id')}),
    )
    
#     form=FileModelForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('image_file','image_url', 'facility', 'created_by_id'),
        }),
    )
    

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(ImageSourceAdmin, self).get_fieldsets(request, obj)
    
        
@admin.register(ReportModel)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message','path') 


class LocationTypeWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(loc_type = value)[0]
    
class GeolocationWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(zipcode = value)[0]
    
class LocationCatergoryWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(category = value)[0]

class LocationResource(resources.ModelResource):
    
    zipcode = fields.Field(
        column_name='zipcode',
        attribute='zipcode',
        widget=GeolocationWidget(Geolocation, 'zipcode')) 
    
    location_category = fields.Field(
        column_name='location_category',
        attribute='location_category',
        widget=LocationCatergoryWidget(LocationCatergory, 'category')) 
        
    
    location_type = fields.Field(
        column_name='location_type',
        attribute='location_type',
        widget=LocationTypeWidget(LocationType, 'loc_type'))
    

    class Meta:
        model = Location
        import_id_fields = ('location_name',)
        fields = ('location_category', 
            'location_type', 
                  'location_name',
                  'location_website', 
                  'street_address_1',
                  'street_address_2',
                  'city',
                  'state',
                  'contact_no',
                  'zipcode',
    'sun_open_time',
    'sun_close_time' ,
    'mon_open_time' ,
    'mon_close_time',
    'tue_open_time' ,
    'tue_close_time',
    'wed_open_time',
    'wed_close_time',
    'thu_open_time' ,
    'thu_close_time',
    'fri_open_time',
    'fri_close_time' ,
    'sat_open_time',
    'sat_close_time', )
    
    
@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ('location_name','location_type','city','state','zipcode') 
    search_fields = ('location_name','city','state')

@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('loc_type',) 
    
@admin.register(LocationCatergory)
class LocationCatergoryAdmin(admin.ModelAdmin):
    list_display = ('category',) 
    
@admin.register(OrgType)
class OrgTypeAdmin(admin.ModelAdmin):
    list_display = ('orgtype',) 

# @admin.register(Partners)
# class PartnersAdmin(admin.ModelAdmin):
#     list_display = ('CompanyName', 'CompanyEmail', 'HQAddress','userID')
    



class GeolocationResource(resources.ModelResource):
        
    
    class Meta:
        model = Geolocation
        import_id_fields = ('zipcode',)
        fields = ('zipcode', 
                  'city',
                  'state', 
                  'state_short',
                  'country',
                  'latitude',
                  'longitude',)


@admin.register(Geolocation)
class GeolocationAdmin(ImportExportModelAdmin):
    resource_class = GeolocationResource
        
class AmenityTypeResource(resources.ModelResource):
        
    
    class Meta:
        model = AmenityType
        import_id_fields = ('amenity_type',)
        fields = ('amenity_type', 
                  'amenity_icon',)
    
@admin.register(AmenityType)
class AmenityTypeAdmin(ImportExportModelAdmin):
    resource_class = AmenityTypeResource
                