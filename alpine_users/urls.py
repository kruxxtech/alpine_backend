from django.urls import path
from . import views


# chaging user model


urlpatterns = [
    path("login/", views.obtain_token, name="obtain_token"),
    path("register/", views.register_user, name="register_user"),
    path("getUsers/", views.get_user_list, name="get_user_list"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
]
