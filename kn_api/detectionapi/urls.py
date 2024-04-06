from detectionapi.views import my_data_view
from django.urls import path

urlpatterns = [
    path('',my_data_view)
]