from smtplib import SMTPException

from django import forms
from django.core.mail import EmailMessage

from django.conf import settings

from frontend.models import *
        
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['latitude','longitude']
        widgets= {'location_type': forms.Select(attrs={'class':'selectpicker search-fields','placeholder': 'Location Type', 'required':'required'}),
                  'location_name': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Enter Location name', 'required':'required'}),
    'location_website' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Enter Location website', 'required':'required'}),
    'street_address_1' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Street Address 1', 'required':'required'}),
    'street_address_2' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Street Address 2', 'required':'required'}),
    'city' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'City', 'required':'required'}),
    'state' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'State', 'required':'required'}),
    'zipcode' : forms.Select(attrs={'class':'selectpicker search-fields','placeholder': 'Zipcode', 'required':'required'}),
    'contact_no' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Contact No', 'required':'required'}),
    'hours' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Hours', 'required':'required'}),
    'email': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Email', 'required':'required'}),
    'sun_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Sun Open Time', 'required':'required'}),
    'sun_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Sun Close Time', 'required':'required'}),
    'mon_open_time': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Mon Open Time', 'required':'required'}),
    'mon_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Mon Close Time', 'required':'required'}),
    'tue_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Tue Open Time', 'required':'required'}),
    'tue_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Tue Close Time', 'required':'required'}),
    'wed_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Wed Open Time', 'required':'required'}),
    'wed_close_time': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Wed Close Time', 'required':'required'}),
    'thu_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Thu Open Time', 'required':'required'}),
    'thu_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Thu Close Time', 'required':'required'}),
    'fri_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fri Open Time', 'required':'required'}),
    'fri_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fri Close Time', 'required':'required'}),
    'sat_open_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Sat Open Time', 'required':'required'}),
    'sat_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Sat Close Time', 'required':'required'}),}
        
class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        exclude = ['created_by_id',
                   'assigned_to',
                   'partner',
                   'org_id',
                   'longitude',
                   'latitude',
                   'location_id',
                   'availability',
                   'location_id',                   
                   'updated_on',
                   'created_on']
        widgets= {'facility_name': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Facility name', 'required':'required'}),
                  'facility_information': forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Enter Facility Information', 'required':'required'}),
    'parking_spaces' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Parking spaces', 'required':'required'}),
    'capacity' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Capacity', 'required':'required'}),
    'none_refundable_fee' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'None refundable fee', 'required':'required'}),
    'cost_for_profit' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Cost for profit', 'required':'required'}),
    'cost_for_non_profit' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Cost for non profit', 'required':'required'}),
    'fac_cost_misc_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc alc', 'required':'required'}),
    'fac_cost_misc_rental_clean_dep_no_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc rental clean dep no alc', 'required':'required'}),
    'fac_cost_misc_rental_clean_dep_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc rental clean dep alc', 'required':'required'}),
    'fac_cost_misc_non_ref_hr_mtn': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc non ref hr mtn', 'required':'required'}),
    'fac_cost_misc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc', 'required':'required'}),
    'staff_fee' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Staff fee', 'required':'required'}),
    'fac_amenities': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac amenities', 'required':'required'}),
    'note_1' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 1', 'required':'required'}),
    'note_2' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 2', 'required':'required'}),
    'note_3' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 3', 'required':'required'}),
    'res_1' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 1', 'required':'required'}),
    'res_2': forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 2', 'required':'required'}),
    'res_3' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 3', 'required':'required'}),
    'fac_surf_type' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac surf type', 'required':'required'}),
    'fac_feature' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac feature', 'required':'required'}),
    'fee_based_amenities' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fee based amenities', 'required':'required'}),
    'event_type' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Event type', 'required':'required'}),}
        

                 
