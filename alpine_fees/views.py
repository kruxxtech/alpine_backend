from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max

from .models import *

from .serializers import *

# Create your views here.


@api_view(["GET"])
def getFeeDetails(request):
    fees = FeeTable.objects.all()
    serializer = FeeTableSerializer(fees, many=True)
    return Response(serializer.data)


# get max fee_receipt_id
@api_view(["GET"])
def getFeeReceiptId(request):
    fee_receipts = FeeReceipts.objects.all()
    max_id = fee_receipts.aggregate(Max("id"))
    return Response({"receipt_id": max_id})


#  get fees based on college_id, ssnid and crsid
@api_view(["GET", "POST"])
def getFeeDetailsByCourse(request, college_id, ssnid, crsid):
    if request.method == "GET":
        try:
            fee = FeeTable.objects.get(college_id=college_id, ssnid=ssnid, crsid=crsid)
            serializer = FeeTableSerializer(fee)
            return Response(serializer.data)
        except FeeTable.DoesNotExist:
            return Response({"error": "Fee details not found"}, status=404)

    if request.method == "POST":
        data = request.data.copy()
        data["college_id"] = college_id
        data["ssnid"] = ssnid
        data["crsid"] = crsid

        fee_id = data.get("fee_id")
        if fee_id:
            try:
                # get the existing fee object by fee_id
                fee = FeeTable.objects.get(pk=fee_id)
                serializer = FeeTableSerializer(fee, data=data)
            except FeeTable.DoesNotExist:
                # If fee_id does not Exist, create a new one
                serializer = FeeTableSerializer(data=data)
        else:
            # If fee_id is not provided, create a new record
            serializer = FeeTableSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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


@api_view(["GET"])
def review_fee_receipt(request, student_id):
    try:
        admissions = Admission.objects.filter(student_id=student_id)

        response_data = []
        # father_name issuw can be solved by creating a entry in profile table when student is admitted
        # temporary solution
        father_name = ""
        for admission in admissions:
            try:
                profile = Profile.objects.get(student_id=admission.student_id)
                father_name = profile.father_name
            except Profile.DoesNotExist:
                father_name = ""

            college = College.objects.get(college_id=admission.college_id)
            course = Course.objects.get(crsid=admission.crsid)
            session = Session.objects.get(ssnid=admission.ssnid)

        data = {
            "student_id": admission.student_id,
            "enrol_id": admission.enrol_id,
            "stu_name": admission.stu_name,
            "father": father_name,
            "course": course.course,
            "session": session.ssntitle,
            # college info
            "college_code": college.college_code,
            "college_name": college.name,
            "college_address": college.address,
            "college_web": college.website,
            "college_email": college.email,
            "college_contact": college.phone_number,
            "college_approved": college.approved_by,
        }

        response_data.append(data)
        return Response(response_data)
    except (
        Admission.DoesNotExist,
        Profile.DoesNotExist,
        College.DoesNotExist,
        Course.DoesNotExist,
        Session.DoesNotExist,
    ):
        return Response(status=404)
