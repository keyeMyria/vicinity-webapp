# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import ContactView

app_name='contact'

urlpatterns = [
    url(r'^$', ContactView.as_view(), name='contact'),
]
