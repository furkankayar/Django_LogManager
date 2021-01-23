from djongo import models
from pymongo import settings
from django.conf import settings
from django.contrib.auth.models import AbstractUser

log_records = settings.MONGO_DB['logs']

class CustomUser(AbstractUser): 
    can_access_log_manager = models.BooleanField(verbose_name="Log Manager Access Status", help_text="Designates that this user can access log manager page.", default=False)