from django.contrib import admin
from django.urls import path
from views import login_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout")
]