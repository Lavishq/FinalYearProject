
from django.urls import path
from accounts import views

urlpatterns = [
    path('register', views.register, name="register.html"),
    path('login', views.login, name="login.html"),
    path('logout', views.logout, name="logout.html")
]