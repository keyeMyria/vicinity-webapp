from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from backend import views

admin.autodiscover()

app_name= 'backend'

urlpatterns = [
    url(r'^admin/settings$', views.setting_index, name="setting_index"),
    url(r'^admin/chat$', views.chat_index, name="chat_index"),
    url(r'^admin/calendar/view$', views.calendar_view, name="calendar_view"),
    url(r'^admin/booking/details$', views.booking_index, name="booking_index"),
    url(r'^admin/booking/view/(?P<id>[-\w]+)$', views.booking_view, name="booking_view"),
    url(r'^admin/accounts/user/(?P<id>[-\w]+)$', views.user_view, name="user_view"),
    url(r'^admin/dash$', views.displayAdminDash, name='admindash'),
    url(r'^admin/proposals$', views.showProposals, name='showproposals'),
    url(r'^admin/partners$', views.showPartners, name='showpartners'),
    url(r'^admin/partners/(?P<id>[0-9]+)/remove$', views.removePartner, name='removepartner'),
    url(r'^admin/proposals/(?P<id>[0-9]+)/accept$', views.acceptProposals, name='acceptproposal'),
    url(r'^admin/proposals/(?P<id>[0-9]+)/decline$', views.declineProposals, name='declineproposal'),
    url(r'^admin/test_email/$', views.test_email, name="test_email"),
    url(r'^admin/spaceproposals$', views.spaceproposals, name='spaceproposals'),
    url(r'^admin/spaceproposals/(?P<id>[0-9]+)/view$', views.spacereviewProposals, name='spacereviewproposal'),
    url(r'^admin/spaceproposals/(?P<id>[0-9]+)/accept$', views.spaceacceptProposals, name='spaceacceptproposal'),
    url(r'^admin/spaceproposals/(?P<id>[0-9]+)/decline$', views.spacedeclineProposals, name='spacedeclineproposal'),
    
]