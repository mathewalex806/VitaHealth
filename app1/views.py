from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db import IntegrityError
from .forms import *
# Create your views here.


def  index(request):
    return render(request, 'app1/index.html')




def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app1/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app1/login.html")
    


    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))




def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "app1/signup.html", {
                "message": "Username already taken."
            })
        
    else:
        return render (request, "app1/signup.html")
    
def image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            a = Image.objects.last()
            return render (request, "app1/image_upload.html", {'a' : a})
        else:
            form = ImageForm()
            return render (request, 'app1/image_upload.html', {'form': form})
    return render (request, "app1/image_upload.html",  {'form': ImageForm()})



