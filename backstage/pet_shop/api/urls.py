from django.urls import path, include
from api.views import uLogin, uRegister, aLogin

urlpatterns = [
	# Generic Class Based View
	path("user/register/", uRegister.UserRegister.as_view(), name="user_register"),
	path("user/login/", uLogin.UserLogin.as_view(), name="user_login"),
	path("admin/login/", aLogin.AdminLogin.as_view(), name="admin_login"),

]
