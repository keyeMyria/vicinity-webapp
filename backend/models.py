from django.db import models
from django.utils import timezone
from accounts.models import *
# Create your models here.


def get_logo_upload_to(instance, filename):
    return "images/site/{}".format(filename)

class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    meta_author = models.TextField()
    analytics_code = models.TextField()
    facebook_page = models.TextField()
    twitter_page = models.TextField()
    google_page = models.TextField()    
    instagram_page = models.TextField()  
    site_logo = models.FileField(upload_to=get_logo_upload_to, blank=True, null=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_setting'
        managed = True
