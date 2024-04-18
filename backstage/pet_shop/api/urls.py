from django.urls import path, include
from api import views

urlpatterns = [
    # Generic Class Based View
    path("user/register/", views.UserRegister.as_view(), name="user_register"),
    path("user/login/", views.UserLogin.as_view(), name="user_login"),

]
