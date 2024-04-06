from video_stream.views import video_feed
from django.urls import path

urlpatterns = [
    path('',video_feed)
]