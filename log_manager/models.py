from djongo import models
from pymongo import settings
from django.conf import settings

log_records = settings.MONGO_DB['logs']

# Create your models here.
class LogRecord(models.Model):
    client_ip = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100)
    http_method = models.CharField(max_length=40)
    requested_resource = models.CharField(max_length=1000)
    http_version = models.CharField(max_length=50)
    status_code = models.CharField(max_length=50)
    response_size = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=1000)
    time = models.DateTimeField() 

    class Meta: 
        app_label = 'log_manager_db'
        db_table = 'logs'