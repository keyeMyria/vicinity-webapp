from __future__ import unicode_literals

import re

from django import forms
from django.utils.encoding import force_text
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from accounts.utils import get_user_lookup_kwargs

from accounts.models import User
from core.models import *

alnum_re = re.compile(r"\w+$") 

GENDER = [
    ('0', ''),
    ('1', 'Male'),
    ('2', 'Female'),
]

class DateInput(forms.DateInput):
    input_type = 'date'

class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].input_formats = settings.DATE_INPUT_FORMATS
     
    first_name = forms.CharField(label=_("First name"), max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}), required=True
    )
    last_name = forms.CharField(label=_("Last name"), max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}), required=True
    )

    contact_no = forms.CharField(
        max_length=64, label=_("Contact no"), required=True,  widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.CharField(label=_('Gender'), widget=forms.Select(attrs={'class': 'form-control'},choices = GENDER), required=False)
    about_me=forms.CharField(label=_('About me'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    address=forms.CharField(label=_('Address'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    city=forms.CharField(label=_('City'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    state=forms.CharField(label=_('State'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    country=forms.CharField(label=_('Country'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    zipcode=forms.CharField(label=_('Zipcode'), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    date_of_birth=forms.DateField(label=_('Date of Birth'), widget=DateInput(attrs={'class': 'form-control'}), required=False) 
    profile_file=forms.FileField(label=_('Profile Image'), widget=forms.FileInput(attrs={'class': 'form-control'}), required=False) 
    
    class Meta:
        input_formats = ['%b, %Y']
        model = User
        fields = [
                  'first_name',
                  'last_name',
                  'contact_no',
                  'gender',
                  'about_me',
                  'address',
                  'city',
                  'state',
                  'country',
                  'zipcode',
                  'date_of_birth',
                  'profile_file',
                 ]


    def clean_contact_no(self):
        value = self.cleaned_data["contact_no"]
        qs = User.objects.filter(contact_no__iexact=value)
        if not qs.exists():
            return value
        raise forms.ValidationError(
            _("A user is registered with this Contact no."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(
                    _("You must type the same password each time."))
        return self.cleaned_data
    

    
    