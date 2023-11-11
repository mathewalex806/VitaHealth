from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
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