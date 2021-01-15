from django.urls import path
from .views import index, log_stream, request_month


urlpatterns = [
    path('', view=index, name='index'),
    path('log_stream', view=log_stream, name='log_stream'),
    path('request_month', view=request_month, name='request_month')
]