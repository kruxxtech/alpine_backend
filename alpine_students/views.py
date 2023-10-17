from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Max, Sum, DecimalField
from alpine_fees.models import FeeBalance
from alpine_fees.serializers import FeeBalanceSerializer
from django.db.models.functions import Coalesce

from .models import *
from .serializers import *
from alpine_gp.models import *

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
            admission = admsn_serializer.save()
            course = Course.objects.get(crsid=request.data["crsid"])
            promotion = Promotion.objects.create(
                curr_year=1,
                status="new_admission",
                _duration=course.duration,
                student=admission,
            )
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
def student_profile_by_name(request, stu_name):
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
                "doj": admission.doj,
            }
            response_data.append(data)

        return Response(response_data)
    except (Admission.DoesNotExist, Profile.DoesNotExist):
        return Response(status=404)


#  get student profile by student_id
@api_view(["GET", "POST"])
def student_profile_by_id(request, student_id):
    try:
        admissions = Admission.objects.get(student_id=student_id)
        if request.method == "GET":
            response_data = [
                {
                    "name": admissions.stu_name,
                    "doj": admissions.doj,
                    "enrol_id": admissions.enrol_id,
                }
            ]

            return Response(response_data)
        elif request.method == "POST":
            admissions = Admission.objects.get(student_id=student_id)

            # Check if a profile exists for the admission
            profile = Profile.objects.filter(student=admissions).first()

            if profile:
                # Update the profile
                serializer = ProfileSerializer(profile, data=request.data, partial=True)
            else:
                # Create a new profile
                new_data = request.data.copy()
                new_data['student'] = admissions.student_id  # Add the student relationship to the data
                serializer = ProfileSerializer(data=new_data)

            if serializer.is_valid():
                serializer.save()

                if profile:
                    return_status = status.HTTP_200_OK
                else:
                    return_status = status.HTTP_201_CREATED

                return Response(serializer.data, status=return_status)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Admission.DoesNotExist:
        return Response({'status': 'error', 'message': 'Student Admission not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#  get student Complete profile by student_id
@api_view(["GET"])
def student_complete_profile_by_id(request, student_id):
    try:
        admission = Admission.objects.get(student_id=student_id)

        profile = admission.profile

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Admission.DoesNotExist:
        return Response({'status': 'error', 'message': 'Admission not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({'status': 'error', 'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def student_profile_detail_by_filters(request):
    try:
        student_name = request.GET.get("stu_name", None)
        college_id = request.GET.get("college_id", None)
        course_id = request.GET.get("crsid", None)
        admissions = Admission.objects.all()

        if student_name is not None:
            admissions = admissions.filter(stu_name__icontains=student_name)

        if college_id is not None:
            admissions = admissions.filter(college_id=college_id)

        if course_id is not None:
            admissions = admissions.filter(crsid=course_id)

        profiles = Profile.objects.filter(
            student_id__in=admissions.values_list("student_id", flat=True)
        )

        response_data = []
        for admission in admissions:
            profile = profiles.filter(student_id=admission.student_id).first()

            try:
                promotion = Promotion.objects.filter(
                    student_id=admission.student_id
                ).first()
                prev_curr_bal = 0
                if promotion is not None:
                    try:
                        fee_balance = FeeBalance.objects.get(
                            student_id=admission.student_id,
                            curr_year=promotion.curr_year,
                        )

                        curr_balance = str(
                            int(
                                fee_balance.reg_fee
                                + fee_balance.tut_fee
                                + fee_balance.sec_fee
                                + fee_balance.other_fee
                            )
                        )

                        prev_curr_bal = (
                            str(int(fee_balance.pre_bal)) + " + " + str(curr_balance)
                        )

                    except FeeBalance.DoesNotExist:
                        prev_curr_bal = 0
                        pass

                data = {
                    "id": admission.enrol_id,
                    "stu_name": admission.stu_name,
                    "father_name": profile.father_name if profile else None,
                    "contact_no": admission.contact_no,
                    "student_id": admission.student_id,
                    "college_id": admission.college_id,
                    "crsid": admission.crsid,
                    "prev_curr_bal": prev_curr_bal,
                }

                response_data.append(data)

            except Promotion.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            #  FeeBalance matching query does not exist, make curr_balance = 0
        return Response(response_data, status=status.HTTP_200_OK)
    except Admission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def student_fee_by_id(request, student_id):
    try:
        admission = Admission.objects.filter(student_id=student_id)
        response_data = []

        for admission in admission:
            # profile = Profile.objects.get(student_id=admission.student_id)
            data = {
                "id": admission.enrol_id,
                "stu_name": admission.stu_name,
                "college_id": admission.college_id,
                "crsid": admission.crsid,
            }
            response_data.append(data)

        return Response(response_data)
    except (Admission.DoesNotExist, Profile.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)


# merge with student_fee_by_id
@api_view(["GET", "POST"])
def update_or_create_fee_balance(request, student_id, curr_year):
    if request.method == "GET":
        try:
            feeBalance = FeeBalance.objects.get(
                student_id=student_id, curr_year=curr_year
            )

            response_data = []

            data = {
                "reg_fee": feeBalance.reg_fee,
                "tut_fee": feeBalance.tut_fee,
                "sec_fee": feeBalance.sec_fee,
                "pre_bal": feeBalance.pre_bal,
                "other_fee": feeBalance.other_fee,
            }
            response_data.append(data)

            return Response(response_data)
        except (Admission.DoesNotExist, Profile.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        try:
            feeBalance = FeeBalance.objects.get(
                student_id=student_id, curr_year=curr_year
            )
            serializer = FeeBalanceSerializer(feeBalance, data=request.data)
            #  pre_bal will be initially
            if serializer.is_valid():
                validated_data = serializer.validated_data
                fee_balance, created = FeeBalance.objects.update_or_create(
                    student_id=validated_data.get("student_id"),
                    curr_year=validated_data.get("curr_year"),
                    defaults={
                        "reg_fee": validated_data.get("reg_fee"),
                        "sec_fee": validated_data.get("sec_fee"),
                        "tut_fee": validated_data.get("tut_fee"),
                        "other_fee": validated_data.get("other_fee"),
                        "pre_bal": validated_data.get("pre_bal"),
                        "rebate": validated_data.get("rebate"),
                    },
                )

                return Response(
                    FeeBalanceSerializer(fee_balance).data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (Admission.DoesNotExist, Profile.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def name_search(request):
    query_param = request.query_params.get("search", "")
    names = Admission.objects.filter(stu_name__icontains=query_param)
    serializer = StudentNameSerializer(names, many=True)

    return Response(serializer.data)


@api_view(["GET", "POST"])
def promotion_update(request, student_id):
    try:
        promotion = Promotion.objects.get(student_id=student_id)
    except Promotion.DoesNotExist:
        return Response(
            {"error": "No entry found for this student"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        if request.method == "GET":
            serializer = PromotionSerializer(promotion, many=False)
            return Response(serializer.data)

    except Promotion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #
    if request.method == "POST":
        serializer = PromotionSerializer(data=request.data)

        promotion_status = request.data.get("status")

        if promotion_status is None:
            return Response(
                {"error": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        duration = promotion.duration
        if promotion_status == "promoted":
            if promotion.curr_year + 1 > duration:
                promotion.status = "passed"
            else:
                promotion.status = "promoted"
                promotion.curr_year += 1
        elif promotion_status == "not_promoted":
            # curr_year remains the same
            pass
        else:
            promotion.status = promotion_status

        promotion.save()

        return Response(
            PromotionSerializer(promotion).data, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def student_guardian_list(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        if student_id:
            guardians = StudentGuardian.objects.filter(student_id=student_id)
        else:
            guardians = StudentGuardian.objects.all()

        serializer = StudentGuardianSerializer(guardians, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentGuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def student_total_details_by_id(request, student_id):
    try:
        admission = Admission.objects.get(student_id=student_id)

        # Fetch associated models
        college = College.objects.get(college_id=admission.college_id)
        course = Course.objects.get(crsid=admission.crsid)
        session = Session.objects.get(ssnid=admission.ssnid)

        # Fetch the profile if it exists, otherwise set it to None
        try:
            profile = Profile.objects.get(student=admission)
            profile_fields = {f.name: getattr(profile, f.name) for f in Profile._meta.fields if f.name not in ["id", "student"]}
        except Profile.DoesNotExist:
            profile = None
            # Set all the profile fields to an empty string
            profile_fields = {f.name: "" for f in Profile._meta.fields if f.name not in ["id", "student"]}

        promotion = Promotion.objects.get(student=admission)
        admission_fields = {f.name: getattr(admission, f.name) for f in Admission._meta.fields if f.name not in ["student_id"]}

        data = {
            "enrol_id": admission.enrol_id,
            "stu_name": admission.stu_name,
            "college_name": college.name,
            "course_name": course.course,
            "course_duration": course.duration,
            "promotion_status": promotion.status,
            "session_current_year": session.sdate,
            **admission_fields,
            **profile_fields
        }

        return Response(data)
    except (Admission.DoesNotExist, College.DoesNotExist, Course.DoesNotExist, Session.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)