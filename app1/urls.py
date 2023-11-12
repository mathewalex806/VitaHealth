from django.urls import path
from . import views

urlpatterns = [ path("" , views.index, name="index"),
                path("login", views.login_view, name= "login"),
                path("logout", views.logout_view, name= "logout"),
                path("signup", views.signup, name= "signup"),
                path("image_upload", views.image, name= "image"),
                path("result", views.result, name= "result"),
                path("camera", views.camera, name = "camera"),
                path("recipe", views.recipe, name= "recipe"),
                path("diet", views.diet, name = "diet"),
               ]