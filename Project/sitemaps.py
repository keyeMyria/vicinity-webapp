from django.contrib.sitemaps import Sitemap
from about.urls import urlpatterns as aboutUrls
from contact.urls import urlpatterns as contactUrls
from frontend.urls import urlpatterns as frontendUrls
from frontend.models import *
from django.shortcuts import reverse
from django.urls import reverse_lazy


class Sitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.5
    

    def items(self):
        return Facility.objects.all()

    def location(self, item):
         return reverse_lazy('frontend:roomview', kwargs={'id': item.id})

class StaticSitemap(Sitemap):
     priority = 0.5
     changefreq = 'weekly'

     def items(self):
        mylist = [ ]
        for url in contactUrls:
            mylist.append('contact:'+url.name)
        for url in aboutUrls:
            mylist.append('about:'+url.name) 
        for url in frontendUrls:
            if url.name=='search_filter':
                mylist.append('frontend:'+url.name)  
        return mylist

     def location(self, item):
         return reverse_lazy(item)
     
sitemaps = {
    'todos': Sitemap,
    'static': StaticSitemap,
}