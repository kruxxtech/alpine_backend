from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *

from .serializers import *

# Create your views here.


@api_view(["GET"])
def getFeeDetails(request):
    fees = FeeTable.objects.all()
    serializer = FeeTableSerializer(fees, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_fee_receipt(request, student_id):
    if request.method == "GET":
        try:
            fee_receipt = FeeReceipts.objects.filter(student_id=student_id)
            serializer = FeeReceiptSerializer(fee_receipt, many=True)
            return Response(serializer.data, status=200)
        except FeeReceipts.DoesNotExist:
            return Response({"error": "Fee receipt not found"}, status=404)
    if request.method == "POST":
        admission = Admission.objects.get(student_id=student_id)

        data = request.data.copy()
        data["student"] = student_id
        data["enrol_id"] = admission.enrol_id
        data["stu_name"] = admission.stu_name

        serializer = FeeReceiptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
