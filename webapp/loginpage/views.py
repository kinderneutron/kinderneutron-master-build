from django.shortcuts import render
import psycopg2
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import resolve
from django.apps.registry import apps
name = ""
password = ""
email = ""
auth_token = ""
def loginpageres(request):
     show_div = request.GET.get('show_div',True)
     print(show_div)
     if not show_div:
          show_div = {'show_div': False} # Get the value of show_div from the query parameters
     context = {'show_div': show_div}
     username = request.GET.get('regusername') if request.GET.get('regusername') else "N/A"
     email = request.GET.get('email') if request.GET.get('regusername') else "N/A"
     auth_token = request.GET.get('authtoken') if request.GET.get('authtoken') else "N/A"
     password = request.GET.get('regpassword') if request.GET.get('regpassword') else "N/A"
     if (username is not None and username != "N/A") and \
   (email is not None and email != "N/A") and \
   (auth_token is not None and auth_token != "N/A") and \
   (password is not None and password != "N/A"):
          conn = psycopg2.connect(dbname="kinderneutron_db", user="postgres",  password="123456",  host="psql-db", port="5432")
          with conn.cursor() as cursor:
        # The SQL INSERT query
               query = """INSERT INTO "user" (username, email, password) VALUES (%s, %s,%s)"""
        
        # Data to insert
               data = (username,email, password)
        
        # Execute the query
               cursor.execute(query, data)
        
        # Commit the transaction
               conn.commit()
          
     return render(request, 'index.html', context)
    

from django.shortcuts import redirect

def redirect_to_another_app(request):
    # You can add any logic here before redirecting if needed
    return redirect('https://www.google.com')  # Replace with the URL you want to redirect to
