from django.contrib import admin
from django.urls import path, include

# from alpineusers import urls as alpineusers_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("alpine_gp.urls")),
    path("api/", include("alpine_fees.urls")),
    path("api/", include("alpine_students.urls")),
    path("api/", include("alpine_users.urls")),
]
