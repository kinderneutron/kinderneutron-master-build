# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import resolve
from django.http import JsonResponse
from django.apps.registry import apps
import psycopg2
import requests
import json
import os
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'data.json'))
# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    detection_json_data = requests.get('http://kinderneutronapicontainer:8001/detectionapi/')
    error_log_json_data = requests.get('http://kinderneutronapicontainer:8001/errorlogapi/')
    device_log_data =requests.get('http://kinderneutronapicontainer:8001/device_detection_api/')
    detection_data= detection_json_data.json()
    error_log_data = error_log_json_data.json()
    device_log_data = device_log_data.json()
    
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        context['detection_data'] = detection_data
        context['error_logs'] = error_log_data
        context['devices'] = device_log_data
        with open(filepath, 'r') as file:
            data = json.load(file)
            context['json_data'] = data['person_detected']
       

        html_template = loader.get_template('home/' + load_template)
        
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

from django.http import JsonResponse

def ajax_update_data(request):
    # Logic to update data dynamically (e.g., read JSON file or fetch data from database)
    # Replace this with your actual logic to update data

    try:
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'data.json'))
        
        with open(filepath, 'r') as file:
            data = json.load(file)
            person_detected = data.get('person_detected', 'no')  # Get 'person_detected' value from JSON data

        return JsonResponse({'person_detected': person_detected})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
