from django.conf import settings
from django.contrib.admin.sites import site
from django.contrib import messages
from core.models import EventTypeModel
from frontend.models import AmenityType, LocationType
from accounts.models import User
from frontend.constant import *

eventarray = []
event = EventTypeModel.objects.all()
if event:
    for code in event:
        eventarray.append((code.event_type_id, code.eventtype))
        
amenityarray = []
amenity = AmenityType.objects.all()
if amenity:
    for code in amenity:
        amenityarray.append((code.amenity_type_id, code.amenity_type))


spaceadminarray = []
spaceadmin = User.objects.filter(type_id=SPACE_ADMIN)
if spaceadmin:
    for code in spaceadmin:
        spaceadminarray.append((code.id, code.get_full_name))
        
locationtypearray = []
locationtype = LocationType.objects.all()
if locationtype:
    for code in locationtype:
        locationtypearray.append((code.pk, code.loc_type))
        
def base(request):
    
    context = {
        'EVENT_LIST': eventarray,
        'AMENITY_LIST': amenityarray,
        'LOCATION_TYPE': locationtypearray,
        'APP_LIST': site.get_app_list(request),
        'PROJECT_NAME': settings.PROJECT_NAME,
        'PROJECT_ICON': settings.PROJECT_ICON,
        'WEBAPP_NOCACHE_TOKEN': settings.WEBAPP_NOCACHE_TOKEN,
        'DEBUG': settings.DEBUG,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        'GOOGLE_API_KEY_FRONT': settings.GOOGLE_API_KEY_FRONT,
        'SPACE_ADMIN_LIST': spaceadminarray,
    }

    return context
    