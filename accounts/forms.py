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
from django.contrib.auth.forms import AuthenticationForm
from frontend.constant import *

from django.db.models import Q

alnum_re = re.compile(r"\w+$") 

GENDER = [
    ('0', ''),
    ('1', 'Male'),
    ('2', 'Female'),
]

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(forms.Form):     
    email = forms.EmailField(
        label=_("Email"), widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control input-text'}), required=True)
    first_name = forms.CharField(label=_("First name"), max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name','class': 'form-control input-text'}), required=True
    )
    last_name = forms.CharField(label=_("Last name"), max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name','class': 'form-control input-text'}), required=True
    )   
        
    username_user = forms.CharField(
        label=_("Username"),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control input-text'}),
        required=True
    )
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control input-text'}), required=True
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"), widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)','class': 'form-control input-text'}), required=True
    )

    contact_no = forms.CharField(
        max_length=64, label=_("Contact no"), required=True,  widget=forms.TextInput(attrs={'placeholder': 'Contact no','class': 'form-control input-text'})
    )

    def clean_username_user(self):
        if not alnum_re.search(self.cleaned_data["username_user"]):
            raise forms.ValidationError(
                _("Usernames can only contain letters, numbers and underscores."))
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username_user"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username_user"]
        raise forms.ValidationError(
            _("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = User.objects.filter(email__iexact=value).filter(~Q(type_id=GUEST))
        if not qs.exists():
            return value
        raise forms.ValidationError(
            _("A user is registered with this email address."))
        
    

    def clean_contact_no(self):
        value = self.cleaned_data["contact_no"]        
        try:
            int(value)
        except:
            raise forms.ValidationError(
            _("Contact no. should be integer value"))
            
        if len(value) < 5:
            raise forms.ValidationError(
            _("Contact no. should not be smaller than 5"))
        
        if  len(value) > 15:
            raise forms.ValidationError(
            _("Contact no. should not be greater than 15")) 

    def clean(self):
        
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
        
            if len(self.cleaned_data["password"]) < 8:
                raise forms.ValidationError("Password is too short.")
            
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(
                    _("You must type the same password each time."))
        return self.cleaned_data
    
class CreateBusinessForm(forms.Form):    
    email_business = forms.EmailField(
        label=_("Email"), widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control input-text'}), required=True)
    first_name_business = forms.CharField(label=_("First name"), max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name','class': 'form-control input-text'}), required=True
    )
    last_name_business = forms.CharField(label=_("Last name"), max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name','class': 'form-control input-text'}), required=True
    )    
        
    username_business = forms.CharField(
        label=_("Username"),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control input-text'}),
        required=True
    )
    password_business = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control input-text'}), required=True
    )
    password_confirm_business = forms.CharField(
        label=_("Password (again)"), widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)','class': 'form-control input-text'}), required=True
    )

    contact_no_business = forms.CharField(
        max_length=64, label=_("Contact no"), required=True,  widget=forms.TextInput(attrs={'placeholder': 'Contact no','class': 'form-control input-text'})
    )

    def clean_username_business(self):
        if not alnum_re.search(self.cleaned_data["username_business"]):
            raise forms.ValidationError(
                _("Usernames can only contain letters, numbers and underscores."))
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username_business"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username_business"]
        raise forms.ValidationError(
            _("This username is already taken. Please choose another."))

    def clean_email_business(self):
        value = self.cleaned_data["email_business"]
        qs = User.objects.filter(email__iexact=value).filter(~Q(type_id=GUEST))
        if not qs.exists():
            return value
        raise forms.ValidationError(
            _("A user is registered with this email address."))
        
    

    def clean_contact_no_business(self):
        value = self.cleaned_data["contact_no_business"]        
        try:
            int(value)
        except:
            raise forms.ValidationError(
            _("Contact no. should be integer value"))
            
        if len(value) < 5:
            raise forms.ValidationError(
            _("Contact no. should not be smaller than 5"))
        
        if  len(value) > 15:
            raise forms.ValidationError(
            _("Contact no. should not be greater than 15")) 

    def clean(self):
        
        if "password_business" in self.cleaned_data and "password_confirm_business" in self.cleaned_data:
        
            if len(self.cleaned_data["password_business"]) < 8:
                raise forms.ValidationError("Password is too short.")
            
            if self.cleaned_data["password_business"] != self.cleaned_data["password_confirm_business"]:
                raise forms.ValidationError(
                    _("You must type the same password each time."))
        return self.cleaned_data

class CheckoutForm(forms.Form):
    payment_method_nonce = forms.CharField(max_length=1000, widget=forms.widgets.HiddenInput, required=False)
    
    def clean(self):
        self.cleaned_data = super(CheckoutForm, self).clean()
        # Braintree nonce is missing
        if not self.cleaned_data.get('payment_method_nonce'):
            raise forms.ValidationError(_(
                'We couldn\'t verify your payment. Please try again.'))
        return self.cleaned_data
       
    
class ProfileUpdateForm(forms.ModelForm):        
        
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].input_formats=settings.DATE_INPUT_FORMATS 

    date_of_birth = forms.DateField(
        label=_("date of birth"), widget=forms.DateInput(attrs={'class':'form-control', 'autocomplete':'off','placeholder': 'D.O.B'}, format='%d/%m/%Y'), required=True
    )
    gender = forms.ChoiceField(
        label=_("Gender"), required=True, choices=GENDER,  widget=forms.Select(attrs={'class':'form-control', 'autocomplete':'off','placeholder': 'Gender'})
    )
    
    class Meta:
        model = User
        fields = ['first_name','last_name','gender','date_of_birth', 'contact_no',
                  'address','city','country','state','zipcode']               
    