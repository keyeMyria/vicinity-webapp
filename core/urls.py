from django.conf.urls import url
from . import views

app_name='core'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^subscriptions$', views.subscriptions, name='subscriptions'),
    url(r'^subscribe/checkout$',views.subscribecheckout,name='subscribecheckout'),
    url(r'^subscribe/payment$',views.subscribepayment,name='subscribepayment'),
    url(r'^booking/checkout$',views.bookingcheckout,name='bookingcheckout'),
    url(r'^booking/payment$',views.bookingpayment,name='bookingpayment'),
    url(r'notification/new', views.NotificationUnreadView, name='notification_new'),
    url(r'message/new', views.MessageUnreadView, name='message_new'),
    url(r'notification/all', views.NotificationReadView, name='notification_all'),
    url(r'message/read', views.MessageReadView, name='message_read'),
    url(r'chat/msgslogsget/$', views.MessagesListget, name='msgs_logs_get'),
    url(r'chat/msgslogspost/$', views.MessagesListpost, name='msgs_logs_post'),
    url(r'proof-upload/$', views.proof_upload, name='proof_upload'),
    url(r'booking-cancel/(?P<id>[-\w]+)$', views.cancel_booking, name='cancel_booking'),
    url(r'room-wish-list/$', views.addwishlist, name='addwishlist'),
    url(r'my-boards/$', views.mywishlist, name='mywishlist'),
    url(r'get-reviews/$', views.getreviews, name='getreviews'),
    url(r'user-profile/$', views.userprofile, name="userprofile"),
    url(r'my-boards/board/(?P<id>[-\w]+)$', views.boarddetail, name='boarddetail'),
    url(r'whishlist/remove/(?P<id>[-\w]+)/(?P<pk>[-\w]+)$', views.whishlistremove, name='whishlistremove'),
    url(r'board/remove/(?P<id>[-\w]+)$', views.boardremove, name='boardremove'),
    url(r'editboard/(?P<id>[-\w]+)$', views.editboard, name='editboard'),
    url(r'verifyemail/$', views.verifyemail, name='verifyemail'),
    url(r'resend-email/$', views.resendemail, name="resendemail"),
    url(r'chat-list/$', views.chatlist, name="chatlist"),
]
