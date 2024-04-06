# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
import psycopg2

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
