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
from collections import Counter
import requests
import json
from django.contrib.auth.decorators import login_required

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
model  = torch.hub.load('ultralytics/yolov5','custom', path='best.pt',force_reload=False)
load_dotenv(find_dotenv())
llm=OpenAI(model_name="text-davinci-003", openai_api_key =os.getenv("OPENAI_API_KEY"))




def give_recipe(food):
    template="""
You are an world renowned chef . Give the recipe for a simple but tasty {food} """
    prompt =PromptTemplate(
    input_variables=["food"],
    template=template,
    )
    x= llm(prompt.format(food=food))
    
    return x
def give_diet(total_cal):
    template="""
    You are an world renowned dietitian . I have a daily calory limit of of {calory}. recommend a diet for rest of the day along with their calories """
    prompt2 =PromptTemplate(
    input_variables=["calory"],
    template=template,
    )
    x= llm(prompt2.format(calory=total_cal))
    
    return x
def image_converter(imgs):
    result=model(imgs)
    lst=[]
    z=Counter(result.pandas().xyxy[0]["name"])
    for zz in z: 
       lst.append([zz, z[zz]])
    result=result.render()[0]
    im = impill.fromarray(result)
    x=str(uuid.uuid4())+".jpg"
    y="media/"+x
    im.save(y)
    return x,lst

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
            return render(request,'app1/dash.html',{'user':request.user.username,'calory':request.user.calorie_count})
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
            return render(request, "app1/login.html")
        except IntegrityError:
            return render(request, "app1/signup.html", {
                "message": "Username already taken."
            })
        
    else:
        return render (request, "app1/signup.html")
@login_required(login_url='login')
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


@login_required(login_url='login')
def result(request):
    if request.method == "POST":
        img_path = request.POST["img_path"]
        img_path="media/"+img_path
        print(img_path)
        x=image_converter(img_path)
        img_return = x[0]
        query = str(x[1][0][1])+" "+str(x[1][0][0])
        print(query)
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        resp= requests.get(api_url, headers={'X-Api-Key': 'jUxgOQ6Uyyv3X7+hMthrnQ==HroM4odQgevPwzgg'})
        response=resp.json()
        if resp.status_code == requests.codes.ok:
            return render (request, "app1/result.html", {"q":query,"result": img_return,"cal":response[0]["calories"],"fat":response[0]["fat_total_g"], "serve":response[0]["serving_size_g"],"fat_sat":response[0]["fat_saturated_g"], "protein":response[0]["protein_g"], "sodium":response[0]["sodium_mg"],"pottas":response[0]["potassium_mg"],"chole":response[0]["cholesterol_mg"],"carbs":response[0]["carbohydrates_total_g"],"fibre":response[0]["fiber_g"],"sugar":response[0]["sugar_g"]})
        else:
            return render (request , "app1/result.html", {"message": "Invalid Access"})
            
        
        
        
@login_required(login_url='login')  
def camera(request):
    
    return render (request, "app1/camera.html")

@login_required(login_url='login')
def recipe(request):
    
    if request.method == "POST":
        recipe_user = request.POST["recipe_input"]
        recipe_ai = give_recipe(recipe_user)
        return render (request, "app1/recipe.html", {"a":recipe_ai})
    else:
        return render (request, "app1/recipe.html")

@login_required(login_url='login')
def diet(request):
    if request.method == "GET":
        user= request.user
        q = User.objects.get(id=user.id)
        x = give_diet (str(q.calorie_count))
        return render (request, "app1/diet.html", {"a":x})
    else:
        return render (request, "app1/diet.html")