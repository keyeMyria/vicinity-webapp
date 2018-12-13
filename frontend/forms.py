# -*- coding: utf-8 -*-

from smtplib import SMTPException

from django import forms
from django.core.mail import EmailMessage

from django.conf import settings

from .models import *
from django.utils import html

from django.utils.translation import ugettext_lazy as _

class ReportForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    subject = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )
    
# class UploadButtonWidget(forms.Widget):
#     def render(self, name, value, attrs=None):
#         return '<input type="file" name="%s" id="fileupload" class="hiden" multiple>\
#         <button type="button" class="btn btn-primary js-upload-photos">\
#       <span class="fa fa-cloud-upload"></span> Upload photos\
#     </button>' % (html.escape(name))
#     
# class UploadButtonField(forms.Field):
#     def __init__(self, *args, **kwargs):
#         if not kwargs:
#             kwargs = {}
#         kwargs["widget"] = UploadButtonWidget
# 
#         super(UploadButtonField, self).__init__(*args, **kwargs)
# 
#     def clean(self, value):
#         return value
    
# class RoomsForm(forms.ModelForm):
#     upload_button = UploadButtonField(label="Upload photos", initial=u"uploadpics")
#     
#     class Meta:
#         input_formats = ['%b, %Y']
#         model = RoomsModel
#         fields = '__all__'

class ProposalForm(forms.ModelForm):
     
    class Meta:
        model = Proposal
        fields = ['CompanyName','CompanyEmail','HQAddress', 'city', 'state', 'zipcode']       

        widgets = {
            'CompanyName': forms.TextInput(attrs={'placeholder': 'Name','class': 'form-control input-text'}),
            'CompanyEmail': forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control input-text'}),
            'HQAddress': forms.TextInput(attrs={'placeholder': 'Address','class': 'form-control input-text'}),
            'city': forms.TextInput(attrs={'placeholder': 'City','class': 'form-control input-text'}),
            'state': forms.TextInput(attrs={'placeholder': 'State','class': 'form-control input-text'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'Zip code','class': 'form-control input-text'}),
        }

    def clean_CompanyEmail(self):
        value = self.cleaned_data["CompanyEmail"]
        qs = User.objects.filter(email__iexact=value)
        if not qs.exists():
            return value
        raise forms.ValidationError(
            _("A user is registered with this email address."))
        
class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        exclude = ['updated_on','partner', 'created_by_id']
        


class AddAboutSpaceForm(forms.ModelForm):
     
    class Meta:
        model = AddSpaceModel
        fields = ['facility_name','facility_information','parking_spaces', 'capacity', 'fac_amenities', 'event_type']       

        widgets = {
            'facility_name': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Facility name', 'required':'required'}),
                  'facility_information': forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Enter Facility Information', 'required':'required'}),
    'parking_spaces' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Parking spaces', 'required':'required'}),
    'capacity' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Capacity', 'required':'required'}),
    'fac_amenities': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac amenities', 'required':'required'}),
    'event_type' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Event type', 'required':'required'}),
        }

        
class AddSpaceForm(forms.ModelForm):
    class Meta:
        model = AddSpaceModel
        exclude = ['facility_name','facility_information','parking_spaces', 'capacity', 'fac_amenities', 'event_type','country','created_on','approval','complete', 'created_by_id','event_type','fac_amenities','street_address_1' ,'street_address_2' ,'city' ,'state','zipcode']
        
        widgets = {
            'location_type': forms.Select(attrs={'class':'selectpicker search-fields','placeholder': 'Location Type', 'required':'required'}),
                  'location_name': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Enter Location name', 'required':'required'}),
            'none_refundable_fee' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'None refundable fee', 'required':'required'}),
    'cost_for_profit' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Cost for profit', 'required':'required'}),
    'cost_for_non_profit' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Cost for non profit', 'required':'required'}),
    'fac_cost_misc_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc alc', 'required':'required'}),
    'fac_cost_misc_rental_clean_dep_no_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc rental clean dep no alc', 'required':'required'}),
    'fac_cost_misc_rental_clean_dep_alc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc rental clean dep alc', 'required':'required'}),
    'fac_cost_misc_non_ref_hr_mtn': forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc non ref hr mtn', 'required':'required'}),
    'fac_cost_misc' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac cost misc', 'required':'required'}),
    'staff_fee' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Staff fee', 'required':'required'}),
    'note_1' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 1', 'required':'required'}),
    'note_2' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 2', 'required':'required'}),
    'note_3' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Note 3', 'required':'required'}),
    'res_1' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 1', 'required':'required'}),
    'res_2': forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 2', 'required':'required'}),
    'res_3' : forms.Textarea(attrs={'class':'form-control input-text','placeholder': 'Res 3', 'required':'required'}),
    'fac_surf_type' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac surf type', 'required':'required'}),
    'fac_feature' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fac feature', 'required':'required'}),
    'fee_based_amenities' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Fee based amenities', 'required':'required'}),
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
    'sat_close_time' : forms.TextInput(attrs={'class':'form-control input-text','placeholder': 'Sat Close Time', 'required':'required'}),
        }
        

                 
