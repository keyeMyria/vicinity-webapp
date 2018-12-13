from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from frontend.constant import *


from django.utils.translation import gettext_lazy as _


GENDER = [
    ('0', 'Male'),
    ('1', 'Female')
]

TYPE_ID = [
    ('', '---'),
    (SUPER_ADMIN, 'Superadmin'),
    (SPACE_ADMIN, 'Spaceadmin'),
    (USER, 'User'),
    (BUSINESS, 'Business'),
    (PARTNER, 'Partner'),
    (GUEST, 'Guest'),
    ]


class User(AbstractUser):
    email = models.EmailField(_('email address'))
    date_of_birth = models.DateTimeField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER)
    about_me = models.CharField(max_length=100, blank=True, null=True)
    contact_no = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=25,null=True,blank=True)
    profile_file = models.FileField(upload_to='images/uploads/', blank=True, null=True)
    tos = models.CharField(max_length=100, blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    state_id = models.CharField(max_length=100, blank=True, null=True)
    type_id = models.IntegerField(default=USER, choices=TYPE_ID)
    last_visit_time = models.CharField(max_length=100, blank=True, null=True)
    last_action_time = models.CharField(max_length=100, blank=True, null=True)
    last_password_change = models.CharField(max_length=100, blank=True, null=True)
    login_error_count = models.CharField(max_length=100, blank=True, null=True)
    activation_key = models.CharField(max_length=100, blank=True, null=True)
    access_token = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=100, blank=True, null=True)
    client_token = models.TextField(verbose_name=u'client token', max_length=500)
    payment_once = models.CharField(max_length=100,null=True,blank=True)
    customer_id = models.CharField(max_length=25,null=True,blank=True)
    payment_mode = models.BooleanField(default=False)
    proof_liability = models.FileField(upload_to='proof/uploads/', blank=True, null=True)
    proof_nonprofit_status = models.FileField(upload_to='proof/uploads/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_user'

    def __unicode__(self):
        return self.username
    

