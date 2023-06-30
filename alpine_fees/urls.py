from django.urls import path
from . import views


urlpatterns = [
    path("fees/", views.getFeeDetails, name="FeeDetails"),
    path("receipt/<str:student_id>", views.create_fee_receipt, name="FeeReceipt"),
]
