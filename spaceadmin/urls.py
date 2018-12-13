from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from spaceadmin import views

app_name = 'spaceadmin'

# Specifying all the urls for the Manage Hotels app which the partners will see .
# Allows for Creating Hotels , Editing them and photos , and adding rooms etc.
urlpatterns = [
     url(r'^dashboard$', views.dashboard, name='dashboard'),
     url(r'^reservation/detail/(?P<pk>[0-9A-Za-z]+)$', views.reservation_detail, name='reservation_detail'),
     url(r'^location/view$', views.location_view, name='location_view'),
     url(r'^location/detail/(?P<pk>[0-9]+)$', views.location_detail, name='location_detail'),
     url(r'^room/detail/(?P<pk>[0-9]+)$', views.room_detail, name='room_detail'),
     url(r'^location/edit/(?P<pk>[0-9]+)$', views.location_edit, name='location_edit'),
     url(r'^facility/edit/(?P<pk>[0-9]+)$', views.facility_edit, name='facility_edit')


]