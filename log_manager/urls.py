from django.urls import path
from .views import index, log_stream


urlpatterns = [
    path('', view=index, name='index'),
    path('log_stream', view=log_stream, name='log_stream')
]