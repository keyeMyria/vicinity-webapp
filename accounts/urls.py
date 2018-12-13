from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views

admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^auth-form/$', views.auth_form, name='auth_form'),
    url(r'^signin/$', views.login_user_auth, name='signin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', views.Register, name='register'),
    url(r'^register-auth/$', views.RegisterAuth, name='register_auth'),
    url(r'^register-business/$', views.RegisterBusiness, name='register_business'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        views.activate, name='activate'),
]