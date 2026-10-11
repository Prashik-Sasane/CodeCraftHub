from django.contrib import admin
from django.urls import path
from views import home, login_user, logout_user

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout")
]