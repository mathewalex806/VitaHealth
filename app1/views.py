from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db import IntegrityError
from .forms import *
from dotenv import load_dotenv,find_dotenv
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import openai
import os
import torch
import numpy
import uuid
import time
from PIL import Image as impill

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
model  = torch.hub.load('ultralytics/yolov5','custom', path='best.pt',force_reload=False)

llm=OpenAI(model_name="text-davinci-003", openai_api_key = "sk-yHOgiFsMAUPoGdqA7yoNT3BlbkFJbANcXH0F9zcDsI")

load_dotenv(find_dotenv())


def give_recipe(food):
    template="""
You are an world renowned chef . Give the recipe for a simple but tasty {food} """
    prompt =PromptTemplate(
    input_variables=["food"],
    template=template,
    )
    x= llm(prompt.format(food=food))
    
    return x

def image_converter(imgs):
    result=model(imgs)
    result=result.render()[0]
    im = impill.fromarray(result)
    x=str(uuid.uuid4())+".jpg"
    y="media/"+x
    im.save(y)
    return x

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
        calorie = request.POST["calorie"]
        allergy = request.POST["allergy"]
        try:
            user = User.objects.create(username = username, password= password, calorie_count = calorie , allergies = allergy)
            user.save()
            return render(request, "app1/login")
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



def result(request):
    if request.method == "POST":
        img_path = request.POST["img_path"]
        img_path="media/"+img_path
        print(img_path)
        img_return = image_converter(img_path)
        
        return render (request, "app1/result.html", {"result": img_return})
    else:
        return render (request , "app1/result.html", {"message": "Invalid Access"})
    
def camera(request):
    
    return render (request, "app1/camera.html")

def recipe(request):
    
    if request.method == "POST":
        recipe_user = request.POST["recipe_input"]
        recipe_ai = give_recipe(recipe_user)
        return render (request, "app1/recipe.html", {"a":recipe_ai})
    else:
        return render (request, "app1/recipe.html")

