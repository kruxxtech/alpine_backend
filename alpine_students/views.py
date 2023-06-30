from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Max


from .models import *
from .serializers import *

# Create your views here.


@api_view(["GET"])
def getStudentIds(request):
    student_ids = Admission.objects.all()
    max_id = student_ids.aggregate(Max("student_id"))
    return Response(max_id)


#  get number of students
#  get the largest student id


@api_view(["GET"])
def students_count(request):
    max_id = Admission.objects.aggregate(max_id=Max("student_id"))["max_id"]
    print(max_id)
    return Response({"student_id": max_id})


@api_view(["GET", "POST"])
def getAdmissions(request):
    if request.method == "GET":
        admissions = Admission.objects.all()
        serializer = AdmissionSerializer(admissions, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # admsn_data = JSONParser().parse(request)

        admsn_serializer = AdmissionSerializer(data=request.data)
        if admsn_serializer.is_valid():
            admsn_serializer.save()
            return JsonResponse(admsn_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(admsn_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def student_profile_by_id(request, stu_name):
    try:
        admission = Admission.objects.filter(stu_name=stu_name)
        response_data = []

        for admission in admission:
            profile = Profile.objects.get(student_id=admission.student_id)
            data = {
                "id": admission.enrol_id,
                "stu_name": admission.stu_name,
                "contact_no": admission.contact_no,
                "father_name": profile.father_name,
                "student_id": admission.student_id,
            }
            response_data.append(data)

        return Response(response_data)
    except (Admission.DoesNotExist, Profile.DoesNotExist):
        return Response(status=404)


@api_view(["GET"])
def student_profile_detail_by_filters(request, college_id=None, crsid=None):
    try:
        admissions = Admission.objects.all()

        if college_id:
            admissions = admissions.filter(college_id=college_id)
        if crsid:
            admissions = admissions.filter(crsid=crsid)

        profiles = Profile.objects.filter(
            student_id__in=admissions.values_list("student_id", flat=True)
        )

        response_data = []
        for admission in admissions:
            profile = profiles.filter(student_id=admission.student_id).first()
            data = {
                "id": admission.enrol_id,
                "stu_name": admission.stu_name,
                "father_name": profile.father_name if profile else None,
                "contact_no": admission.contact_no,
                "student_id": admission.student_id,
                "college_id": admission.college_id,
                "crsid": admission.crsid,
            }
            response_data.append(data)

        return Response(response_data)
    except Admission.DoesNotExist:
        return Response(status=404)


@api_view(["GET"])
def student_fee_by_id(request, student_id):
    try:
        admission = Admission.objects.filter(student_id=student_id)
        response_data = []

        for admission in admission:
            profile = Profile.objects.get(student_id=admission.student_id)
            data = {
                "id": admission.enrol_id,
                "stu_name": admission.stu_name,
                "college_id": admission.college_id,
                "crsid": admission.crsid,
            }
            response_data.append(data)

        return Response(response_data)
    except (Admission.DoesNotExist, Profile.DoesNotExist):
        return Response(status=404)


# merge with student_fee_by_id
@api_view(["GET"])
def student_fee_by_year(request, student_id, curr_year):
    try:
        admission = Admission.objects.filter(student_id=student_id)
        response_data = []

        admission_fee = "admsn_yr" + curr_year
        tution_fee = "yr" + curr_year + "_fee"

        for admission in admission:
            data = {
                "reg_fee": admission.__getattribute__(admission_fee),
                "tut_fee": admission.__getattribute__(tution_fee),
                "sec_fee": 0,
                "prev_bal": 0,
                "other_fee": 0,
            }
            response_data.append(data)

        return Response(response_data)
    except (Admission.DoesNotExist, Profile.DoesNotExist):
        return Response(status=404)


@api_view(["GET"])
def name_search(request):
    query_param = request.query_params.get("search", "")
    names = Admission.objects.filter(stu_name__icontains=query_param)
    serializer = StudentNameSerializer(names, many=True)

    return Response(serializer.data)


@api_view(["GET", "POST"])
def promotion_update(request, student_id):
    try:
        if request.method == "GET":
            promotions = Promotion.objects.get(student_id=student_id)
            serializer = PromotionSerializer(promotions, many=False)
            return Response(serializer.data)

    except Promotion.DoesNotExist:
        return Response(status=404)
    # if request.method == "POST":
    #     student_id = request.data.get("student_id")
    #     status = request.data.get("status")
    #     try:
    #         promotion = Promotion.objects.get(student_id=student_id)
    #     except Promotion.DoesNotExist:
    #         return Response({"message": "Student no found."}, status=404)

    #     if status == 'promoted':
    #         promotion.year += 1
    #         promotion.save()
