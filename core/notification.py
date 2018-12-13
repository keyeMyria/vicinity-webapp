from accounts.models import *
from core.models import *
from frontend.constant import *


class NotificationCreate():
    
    def createnotify(self, userdata, link, is_read, state_id, model_id, description, model_type):
        
        
        NotificationModel.objects.create(link=link, is_read=is_read, state_id=state_id,
                                                    model_id=str(model_id),
                                                    description=description,
                                                    model_type=model_type,
                                                    from_user_id=userdata,
                                                            to_user_id=userdata)
        
    
    
    def user(self, user, link, is_read, state_id, model_id, description, model_type, spaceadmin=False, superadmin=False, partner=False):
        
        if model_type == 'booking':
            room = Facility.objects.get(pk=model_id) 
        
        userdata = user
        if userdata.type_id != SPACE_ADMIN and userdata.type_id != SUPER_ADMIN and userdata.type_id != PARTNER:   
            self.createnotify(userdata=userdata, 
                              link=link, 
                              is_read=is_read, 
                              state_id=state_id, 
                              model_id=model_id, 
                              description=description, 
                              model_type=model_type)
        
        if superadmin:
            userdata = User.objects.filter(type_id=SUPER_ADMIN).first()
            self.createnotify(userdata=userdata, 
                              link=link, 
                              is_read=is_read, 
                              state_id=state_id, 
                              model_id=model_id, 
                              description=description, 
                              model_type=model_type)
            
        if spaceadmin and model_type == 'booking':   
            userdata = room.assigned_to
            self.createnotify(userdata=userdata, 
                              link=link, 
                              is_read=is_read, 
                              state_id=state_id, 
                              model_id=model_id, 
                              description=description, 
                              model_type=model_type)
            
        if partner and model_type == 'booking':
            userdata = room.partner
            self.createnotify(userdata=userdata, 
                              link=link, 
                              is_read=is_read, 
                              state_id=state_id, 
                              model_id=model_id, 
                              description=description, 
                              model_type=model_type)
            
class NotificationDescription():
        
    def description(self, model_id, description, model_type):
        
        if model_type == 'booking':
            room = Facility.objects.get(pk=model_id)
            description += room.facility_name
        return description
    
class MessageDescription():
        
    def description(self, model_id, user, description, model_type):
        
        if model_type == 'chat':
            description += user.get_full_name()
        return description
    