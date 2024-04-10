# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from landingpage.home import views
from .views import ajax_update_data

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('ajax/update_data/', ajax_update_data, name='ajax_update_data'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    

]
