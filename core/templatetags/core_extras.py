# -*- coding: utf-8 -*-

from django import template
from frontend.constant import *
from core.models import *
from frontend.models import *

from django.db.models import Q, Avg
from frontend.forms import *
from accounts.forms import *

from datetime import datetime
from core.notification import *

register = template.Library()


@register.filter
def create_pagination_range(page, max_num_buttons):
    max_num_buttons = int(max_num_buttons)
    begin_page = max(1, page.number - int(max_num_buttons / 2))
    end_page = begin_page + max_num_buttons
    if end_page > page.paginator.num_pages:
        end_page = page.paginator.num_pages + 1
        begin_page = max(1, end_page - max_num_buttons)
    return range(begin_page, end_page)



@register.filter(name='get_room_id')
def get_room_id(key): 
        
    try:
        receiver_user = User.objects.get(type_id=SUPER_ADMIN)
    except User.DoesNotExist:
        receiver_user = None
    if receiver_user:        
        if getattr(receiver_user, 'id') != key:
            try:
                room = NotifRoom.objects.get(title='chat#'+str(key)+'_'+str(receiver_user.pk))
            except NotifRoom.DoesNotExist:
                room = NotifRoom.objects.create(title='chat#'+str(key)+'_'+str(receiver_user.pk))
            return room.group_id
        
@register.filter(name='get_room_id_user')
def get_room_id_user(key, user):
        
    if getattr(user, 'id') != key:
        room = NotifRoom.objects.filter(Q(title='chat#'+str(key)+'_'+str(user.pk))|Q(title='chat#'+str(user.pk)+'_'+str(key))).first()
        if not room:
            room = NotifRoom.objects.create(title='chat#'+str(key)+'_'+str(user.pk))
            
        return room.group_id
    
    
@register.filter(name='get_chat_list')
def get_chat_list(key, currentuser): 
        
    userProfile = User.objects.get(pk=key)
         
    chatmodellist = MessageModel.objects.filter(is_read_to_user=IS_NOT_READ, model_type="chat", from_user_id=userProfile, to_user_id=currentuser)    
    
    if chatmodellist.count() > 0:
        return True
    
    
@register.filter(name='filterrange')
def filterrange(start, end):
    if end:
        return range(int(start), round(float(end)))
  
@register.filter(name='get_priority')
def get_priority(key): 
        
    if key == 1:
        return 'High'
    elif key == 0:
        return 'Medium'
    
    
@register.filter(name='roompics')
def roompics(key):
    pics = ImageSource.objects.filter(facility=key)
    if pics:
        return pics
    
@register.filter(name='roompicsall')
def roompicsall(key):
    pics = ImageSource.objects.filter(facility_id=key)
    return pics
    
    
@register.simple_tag
def reportform():
    return ReportForm()

@register.filter(name='getrating')
def getrating(data):
    data = ReviewsModel.objects.filter(room_book=data).aggregate(Avg('rate')).get('rate__avg')
    if data:
        return round(data)
    else:
        return '0'

@register.filter(name='get_price')
def get_price(data):
    if data:
        if data.org_id_id == 1: 
            return data.cost_for_profit
        elif  data.org_id_id == 2:
            return data.cost_for_non_profit
        
        return data.cost_for_profit


@register.filter(name='getsettime')
def getsettime(time):
    try:
        return datetime.strptime(time, '%H:%M:%S')                                  
    except:
        return time
        
@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()  
  
@register.filter(name='getreservation')
def getreservation(data):
    data = BookingUser.objects.filter(booking_key__isnull=False,room_book=data).filter(Q(status=QUEUE)|Q(status=CONFIRMED)).values('booking_key','user_subscribe','status').distinct()
    return data.count()

@register.filter(name='replace_to')
def replace_to(value):
    return value.replace("&amp;","&")

@register.filter(name='filterrangerev')
def filterrangerev(start, end):
    if end:
        return range(round(float(end)), int(start), -1)

@register.filter(name='getwish')
def getwish(data, user):
    if user:
        data = Roomwishlist.objects.filter(room_book=data, user_subscribe=user)
        return data.count()
    else:
        return None

@register.filter(name='getwishcount')
def getwishcount(data):
    if data:
        data = Roomwishlist.objects.filter(user_subscribe=data)
        return data.count()
    else:
        return None
    

@register.filter(name='notification_count')
def notification_count(data):
    notification_latest = NotificationModel.objects.filter(is_read=IS_NOT_READ, to_user_id=data)
            
    return notification_latest.count()


@register.filter(name='getarry')
def getarry(value):
    valuelist = []
    value = value.split(',')
    for data in value:
        valuelist.append(data.strip())
        
    return valuelist

@register.simple_tag
def getvaluedate(value , string, count):
       
    response = value.get(string+'-'+str(count))
    
    return response 


@register.filter(name='geticon')
def geticon(data):
           
    try:
        amenity = AmenityType.objects.get(amenity_type=data)
    except AmenityType.DoesNotExist:
        amenity = None
        
    if amenity:
        if amenity.amenity_icon:
            return amenity.amenity_icon

    return 'fa fa-tags' 

@register.filter(name='gettypepic')
def gettypepic(value):
       
    event = EventTypeModel.objects.get(event_type_id=value)
    
    if event.eventype_image:
        return '/media/'+str(event.eventype_image)
    else:
        return '/static/images/properties/properties-1.jpg'
    
        
@register.filter(name='boardata')
def boardata(user):
    
    board = Board.objects.filter(user_subscribe=user)
    return board



@register.simple_tag
def getwishboard(user, board, room):
    if user:
        try:
            data = Roomwishlist.objects.filter(room_book=room, user_subscribe=user, board=board)
            return data.count()
        except Roomwishlist.DoesNotExist:
            data = None
        
    else:
        return None
    
    
@register.filter(name='getroomboard')
def getroomboard(user, board):
    if user:
        try:
            data = Roomwishlist.objects.filter(user_subscribe=user, board=board).values('room_book')
            
            facility = Facility.objects.filter(id__in = [ id['room_book'] for id in data])
            
            return facility
            
        except Roomwishlist.DoesNotExist:
            data = None
        
    else:
        return None
    
    
@register.filter(name='getsapceboard')
def getsapceboard(user, board):
    if user:
        try:
            data = Roomwishlist.objects.filter(user_subscribe=user, board=board)
            return data.count()
            
        except Roomwishlist.DoesNotExist:
            data = None
        
    else:
        return None

@register.filter(name='roompicsget')
def roompicsget(key):
    data = []
    for value in key:
        pics = ImageSource.objects.filter(facility=value)
        for image in pics:
            data.append(image.image_file)
    return data

@register.filter(name='chat_list_get')
def chat_list_get(currentuser):
    listdata = []        
         
    chatmodellist = ChatModel.objects.all()
    for data in chatmodellist:
        listdata.append(data)
         
    size = len(listdata)
    uniqueNames = [];
    for i in range(0, size, 1):  
        if(listdata[i].sender not in uniqueNames or listdata[i].receiver not in uniqueNames):
            if currentuser != listdata[i].sender or currentuser != listdata[i].receiver:
                uniqueNames.append(listdata[i].sender);
                uniqueNames.append(listdata[i].receiver);
             
    
    userprofiledata = []
    for user in uniqueNames:
        userProfile = User.objects.get(username=str(user))
        if currentuser.type_id == SUPER_ADMIN:  
            if userProfile.type_id != SUPER_ADMIN and userProfile not in userprofiledata:  
                userprofiledata.append(userProfile)
                
        elif currentuser.type_id == SPACE_ADMIN and userProfile not in userprofiledata not in userprofiledata and userProfile != currentuser:     
            userprofiledata.append(userProfile)  
        else:
            if userProfile.type_id == SPACE_ADMIN and userProfile not in userprofiledata and userProfile != currentuser:
                userprofiledata.append(userProfile) 
          
    return userprofiledata


@register.filter(name='user_list_get')
def user_list_get(user):
    if user.is_authenticated:
        userlist = User.objects.filter(~Q(type_id=GUEST) & ~Q(pk = user.pk))
        if user.type_id == USER:
            userlist = userlist.filter(type_id=SPACE_ADMIN)
        if user.type_id == BUSINESS:
            userlist = userlist.filter(type_id=SPACE_ADMIN)
        return userlist
    else:
        return None


@register.filter(name='user_list_space')
def user_list_space(user):
    
    userlist = User.objects.filter(type_id=SPACE_ADMIN).count()
    return userlist

@register.filter(name='list_space')
def list_space(user):
    
    spacelist = Facility.objects.all().count()
    return spacelist

  
@register.simple_tag
def regisform():
    return CreateUserForm()


@register.simple_tag
def businessregisform():
    return CreateBusinessForm()


@register.filter(name='notification_list')
def notification_list(data):
    notifi_arry = []
    notification_latest = NotificationModel.objects.filter(to_user_id=data).filter(Q(is_read=IS_NOT_READ)|Q(is_read=IS_READ))
    
    for notify in notification_latest:
        notifi_arry.append({'message' : NotificationDescription().description(model_id=notify.model_id, description=notify.description,model_type= notify.model_type),
                                     'time': notify.created_on,
                                     'modelid': notify.model_id,
                                     'modeltype': notify.model_type,
                                     'to_user_id':str(notify.to_user_id.pk),
                                     })
            
    return notifi_arry