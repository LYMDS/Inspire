import datetime
from django.utils import timezone
def expire_checker(expire_time):
    return expire_time > timezone.now()
