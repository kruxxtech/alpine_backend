from django.urls import path
from . import views


# chaging user model


urlpatterns = [
    path("login/", views.obtain_token, name="obtain_token"),
    path("register/", views.register_user, name="register_user"),
]
