# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
import psycopg2
global device_id 
device_id = 1
def login_view(request):
    if request.method =="GET":
        name = request.GET.get('username') if request.GET.get('username') else " "
        password = request.GET.get('password') if request.GET.get('password') else " "
        conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.user WHERE username = '"+name+"' AND password ='"+password+"'")
        records = cursor.fetchall()
        if not records:
            return redirect('http://127.0.0.1:8000/login/?show_div=True')
        else:
            with conn.cursor() as cursor:
        # The SQL INSERT query
                query = """INSERT INTO "device" (id, username, device_name) VALUES (%s, %s,%s)"""
            
            # Data to insert
                global device_id
                data = ("DEV-0"+str(device_id),name,"Web Application")
                device_id = device_id+1
                print(data)
            # Execute the query
                cursor.execute(query, data)
            
            # Commit the transaction
                try:
                    conn.commit()
                    
                except Exception as e:
                    query1 = """INSERT INTO "error_log" (id, userid, error_type,message,created_at,updated_at) VALUES (%s, %s,%s,%s)"""
                    data = ("DBERROR-0"+str(error_id),"N/A","Database Error","Error Due to Invalid Post Request")
                    cursor.execute(query1, data)
                    error_id = error_id+1
            f = open('data.txt','w')
            f.write(name)
            return redirect('http://127.0.0.1:8000/landingpage/')



    # if request.method == "GET":
        
    #     if request.method =="GET":
            
    #         name = request.GET.get('username')
    #         password = request.GET.get('password')
    #         print(name+" "+password)

    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")
    #         print(username+" "+password)
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect("/")
    #         else:
    #             msg = 'Invalid credentials'
    #     else:
    #         msg = 'Error validating the form'
    
    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
