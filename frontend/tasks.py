from celery import Celery
from frontend.models import *
from frontend.constant import *
from core.models import *
from accounts.models import *
from datetime import datetime
from django.db.models import Q 

app = Celery()

@app.task
def facility_task():
    for book in BookingUser.objects.filter(Q(status=CONFIRMED) | Q(status=QUEUE)):
        if book.end_date.strftime("%Y-%m-%d %H:%M:%S")  <=  datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            if book.status == QUEUE:
                book.status = CANCELLED
            else:
                book.status = DONE
            book.save()
            return 'state changed'
    return 'not modified'