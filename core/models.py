from django.db import models
from accounts.models import *
from frontend.models import *

class Subscriptions(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tbl_subscription'
        verbose_name = 'Subscription'
        
    def __str__(self):
        return self.title + ' : $' + str(self.price)

class SubscriptionUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User,related_name='subscription', on_delete=models.CASCADE)
    payment_nonce = models.CharField(max_length=100,null=True,blank=True)
    amount = models.CharField(max_length=100,null=True,blank=True)
    txnid = models.CharField(max_length=25,null=True,blank=True)
    result = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name = 'Subscription User'


    def __str__(self):
        return self.user_subscribe.username + ' : ' + str(self.amount)
    
    
class NotifRoom(models.Model):

    title = models.CharField(max_length=100)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        return "room-%s" % self.id

    @property
    def group_id(self):
        return "%s" % self.id
    

    
class ChatModel(models.Model):
    message = models.CharField(max_length=100)
    receiver = models.ForeignKey(User,related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(User,related_name='sender', on_delete=models.CASCADE)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True) 
    msg_state = models.IntegerField(blank=True, null=True)
    receiver_state = models.IntegerField(blank=True, null=True)
    sender_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_chat'
        verbose_name = 'Chat'
    
    def __str__(self):
        return str(self.id) + ": from " + str(self.sender) + " to " + str(self.receiver)
        
    
class NotificationModel(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    model_id = models.CharField(max_length=100,null=True,blank=True)
    model_type = models.CharField(max_length=100,null=True,blank=True)
    link = models.CharField(max_length=500,null=True,blank=True)
    state_id = models.IntegerField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    to_user_id = models.ForeignKey(User, related_name='to_user_id', on_delete=models.CASCADE, blank=True, null=True)
    from_user_id = models.ForeignKey(User, related_name='from_user_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tbl_notification'
        verbose_name = 'Notification'
        ordering = ['-created_on']
    
    def __str__(self):
        return str(self.title) + ' ' + str(self.description)
    
    
class MessageModel(models.Model):
    description = models.CharField(max_length=100,null=True,blank=True)
    model_id = models.CharField(max_length=100,null=True,blank=True)
    model_type = models.CharField(max_length=100,null=True,blank=True)
    state_id_from_user = models.IntegerField(default=STATE_IS_NOT_SEND)
    state_id_to_user = models.IntegerField(default=STATE_IS_NOT_SEND)
    is_read_from_user = models.IntegerField(default=IS_NOT_READ)
    is_read_to_user = models.IntegerField(default=IS_NOT_READ)
    type_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    to_user_id = models.ForeignKey(User, related_name='message_to_user_id', on_delete=models.CASCADE, blank=True, null=True)
    from_user_id = models.ForeignKey(User, related_name='message_from_user_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tbl_message'
        verbose_name = 'MessageNotif'
        ordering = ['-created_on']
    
    def __str__(self):
        return str(self.description)
        
        
class ReviewsModel(models.Model):
    message = models.TextField(blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    room_book = models.ForeignKey(Facility, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tbl_reviews'
        verbose_name = 'Review'
        ordering = ['-created_on']

STATUS = [
    (DONE,'Done'),
    (QUEUE,'Queue'),
    (CONFIRMED,'Confirmed'),
    (CANCELLED,'Cancelled')
    ]

class BookingUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User,related_name='booking', on_delete=models.CASCADE)
    payment_nonce = models.CharField(max_length=100,null=True,blank=True)
    amount = models.CharField(max_length=100,null=True,blank=True)
    txnid = models.CharField(max_length=25,null=True,blank=True)
    attendees = models.CharField(max_length=25,null=True,blank=True)
    timecheck = models.DateTimeField(blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)
    result = models.BooleanField(default=False)
    room_book = models.ForeignKey(Facility, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    mode = models.IntegerField(default=0)
    status = models.IntegerField(default=0, choices=STATUS)
    type = models.CharField(max_length=25,null=True,blank=True)
    booking_key = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        managed = True
        verbose_name = 'Booking User'
        
        
class Roomwishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Facility, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        
class FeedbackPageForm(models.Model):
    id = models.AutoField(primary_key=True)
    user_subscribe = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    feedback_image = models.ImageField(upload_to="images/feedback/")
    url = models.CharField(max_length=500,null=True,blank=True)
    

    class Meta:
        managed = True
        verbose_name = 'Feedback'