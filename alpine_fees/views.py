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


#  get fees based on college_id, ssnid and crsid
@api_view(["GET"])
def getFeeDetailsByCourse(request, college_id, ssnid, crsid):
    try:
        fees = FeeTable.objects.filter(college_id=college_id, ssnid=ssnid, crsid=crsid)
        serializer = FeeTableSerializer(fees, many=True)
        return Response(serializer.data)
    except FeeTable.DoesNotExist:
        return Response({"error": "Fee details not found"}, status=404)


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

        for admission in admissions:
            profile = Profile.objects.get(student_id=admission.student_id)
            college = College.objects.get(college_id=admission.college_id)
            course = Course.objects.get(crsid=admission.crsid)
            session = Session.objects.get(ssnid=admission.ssnid)

        data = {
            "student_id": admission.student_id,
            "enrol_id": admission.enrol_id,
            "stu_name": admission.stu_name,
            "father": profile.father_name,
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
