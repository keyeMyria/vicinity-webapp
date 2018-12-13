from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q
from frontend.constant import GUEST

UserModel = get_user_model()

from django.contrib.auth.hashers import ( check_password, is_password_usable, make_password, )

class LoginUsingEmailBackend(object):

    def authenticate(self, username=None, password=None):
  
        try:
          # Check if the user exists in Django's database
          user = UserModel.objects.filter(Q(email=username)|Q(username=username)).filter(~Q(type_id=GUEST)).first()
        except UserModel.DoesNotExist:
          return None
        
        if user:
            if not user.is_active == True:
               return None 
        else:
            return None
        # Check password of the user we found
        if check_password(password, user.password):
          return user
        return None
    
    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user