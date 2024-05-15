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
import datetime
from django.apps.registry import apps
import psycopg2
import requests
import json
import os
import pika
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'admin')
global last_message
last_message='no'

detection_id = 1
error_id = 1
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'data.json'))
# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def consume_rabbitmq_message():
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        
        queue_name = 'webappdet'
        channel.queue_declare(queue=queue_name)

        method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
        if body:
            message = json.loads(body.decode('utf-8'))
            print("Message consumed:", message)
            connection.close()  # Close the connection after consuming
            return message
        else:
            print("No message available")
            connection.close()  # Close the connection even if no message is consumed
            return None
    except Exception as e:
        print(f"Error consuming RabbitMQ message: {e}")
        return None
    

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
    f = open('data.txt','r')
    username = f.read()
    conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT email,auth_token FROM public.user WHERE username = '"+username+"'")
    records = cursor.fetchone()
    email = records[0]
    auth_token = records[1]
    cursor.execute("SELECT * FROM authtoken WHERE auth_token = '"+auth_token+"'")
    records = cursor.fetchone()
    plan_type = records[1]
    print(plan_type)
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        context['detection_data'] = detection_data
        context['error_logs'] = error_log_data
        context['devices'] = device_log_data
        context['json_data'] = last_message
        context['email'] = email
        context['auth_token'] = auth_token
        context['plan_type'] = plan_type
        context
        #print(context['json_data'])
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
    
    global last_message
    try:
        # Check if there's a new message available
        new_message = consume_rabbitmq_message()
        print(new_message)
        print(last_message)
        if new_message:
            if new_message['near']== True or new_message['far']==True:
                last_message='yes'
                
                return JsonResponse({'person_detected': 'yes'})
                # Return the last consumed message as JSON response
            else:
                last_message='no'
                return JsonResponse({'person_detected': 'no'})
        else:
            return JsonResponse({'person_detected': last_message})
    except Exception as e:
        return e
