from django.urls import path
from . import views


urlpatterns = [
    path("fees/", views.getFeeDetails, name="FeeDetails"),
    path("fees/receipt_id/", views.getFeeReceiptId, name="FeeReceiptId"),
    path(
        "fees/<str:college_id>/<str:ssnid>/<str:crsid>",
        views.getFeeDetailsByCourse,
        name="FeeDetailsByCourse",
    ),
    path("receipt/<str:student_id>", views.create_fee_receipt, name="FeeReceipt"),
    path(
        "fees/review/<str:student_id>",
        views.review_fee_receipt,
        name="ReviewFeeReceipt",
    ),
]
