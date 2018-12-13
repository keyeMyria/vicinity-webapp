from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap

from Project.sitemaps import sitemaps
from django.views.static import serve 
from core import views as core_views
from django.conf.urls import handler404, handler500,handler403, handler400

admin.autodiscover()



urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^', include('backend.urls')),
    url(r'^accounts/login/$', RedirectView.as_view(url='/admin/login')),
    url(r'^accounts/logout/$', RedirectView.as_view(url='/admin/logout')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^contact-us/', include('contact.urls', namespace='contact')),
    url(r'^about-us/', include('about.urls', namespace='about')),
    url(r'^', include('core.urls', namespace='core')),
    url(r'^', include('frontend.urls', namespace='frontend')),
    url(r'^accounts/', include('social_django.urls', namespace='social')),
    url(r'^sitemap$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^managerooms/', include('managerooms.urls')),
    url(r'^', include('spaceadmin.urls')),
]

if settings.DEBUG:
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else:
    
    
    urlpatterns += [
         url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
         url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
        ]


handler404 = core_views.error_404
handler500 = core_views.error_500
handler400 = core_views.error_404
handler403 = core_views.error_404
