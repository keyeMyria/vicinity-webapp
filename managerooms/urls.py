from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from managerooms import views
from managerooms.views import ChartView

app_name = 'managerooms'

# Specifying all the urls for the Manage Hotels app which the partners will see .
# Allows for Creating Hotels , Editing them and photos , and adding rooms etc.
urlpatterns = [
     url(r'^$', views.home, name='home'),
     url(r'^yourrooms/(?P<pk>[0-9]+)/bookings$', views.showreservations, name='roomsreservations'),
     url(r'^yourrooms/bookings/(?P<pk>[0-9A-Za-z]+)/approve$', views.approvebooking, name='approvebooking'),
     url(r'^yourrooms/(?P<id>[0-9]+)/charts$', ChartView.as_view(), name = 'partnercharts'),
     url(r'^yourrooms/(?P<id>[0-9]+)/availability$', views.availability, name = 'availability'),


]
