from django.conf.urls import url
from . import views
from django.contrib import admin

app_name='frontend'

admin.autodiscover()

urlpatterns = [
    url(r'^search$', views.search_filter, name='search_filter'),
    url(r'^search/filter$', views.get_search_filter, name='get_search_filter'),
    url(r'^room/view/(?P<id>[-\w]+)$', views.roomview, name='roomview'),
    url(r'^room/view/(?P<id>[-\w]+)/reviews$', views.roomviewreviews, name='roomviewreviews'),
    url(r'^report/$', views.ReportView, name='report'),
    url(r'^booking/user/$', views.Bookinguser, name='bookinguser'),
    url(r'^recommend/space$', views.partnerCreateView.as_view(), name='newproposal'),
    url(r'^partner/checkstatus$', views.checkstatus, name='checkproposal'),
    url(r'^viewactivities/$', views.viewactivities, name='viewactivities'),
    url(r'^hostdetail/(?P<id>[0-9]+)/$', views.hostdetail, name='hostdetail'),
    url(r'booking-pdf/(?P<id>[0-9A-Za-z]+)/$', views.booking_pdf, name="booking_pdf"),
    url(r'^booking-pdf/(?P<id>[0-9A-Za-z]+)/pdf$', views.generatePDF, name='generatepdf'),
    url(r'^rental/get-location-address-list/$', views.locationaddress, name='locationaddress'),
    url(r'^get-quote-booking/$', views.get_quote_booking, name='get_quote_booking'),
    url(r'^password-reset-user/$', views.passwordreset, name='passwordreset'),
    url(r'^profile/save$', views.profile_save, name='profile_save'),
    url(r'^contentdetail/$', views.contentdetail, name='contentdetail'),
    
    url(r'^message/host$',views.messagehost,name='messagehost'),
    url(r'^add-space/$', views.addspace, name='addspace'),
    url(r'^recommend-space$', views.addspacedetail, name='addspacedetail'),
    url(r'^add-space-detail-confirm$', views.addspacedetailmessage, name='addspacedetailmessage'),
    url(r'^valid/email$', views.validemail, name='validemail'),
    url(r'^add-space/location$', views.addspacelocation, name='addspacelocation'),
    url(r'^add-space/about$', views.addspaceabout, name='addspaceabout'),
    url(r'^add-space/photos$', views.addspacephotos, name='addspacephotos'),
    url(r'^add-space/activities$', views.addspaceactivities, name='addspaceactivities'),
    url(r'^add-space/confirm$', views.addspaceconfirm, name='addspaceconfirm'),
    url(r'^feedback-form$', views.feedbackform, name='feedbackform'),
]