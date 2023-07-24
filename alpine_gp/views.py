from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime


from .models import *

from .serializers import *

# Create your views here.


@api_view(["GET", "POST"])
def getColleges(request):
    if request.method == "GET":
        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = CollegeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  get number of college
@api_view(["GET"])
def college_count(request):
    count = College.objects.count()
    return Response({"count": count})


@api_view(["GET", "POST"])
def getCourses(request):
    if request.method == "GET":
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        try:
            data = request.data

            # Create a new Course object using the provided data
            course = Course.objects.create(
                college_id=data["college_id"],
                course=data["course"],
                duration=data["duration"],
                crsid=data["crsid"],
            )
            return Response(data, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# get course by college_id
@api_view(["GET"])
def course_list_by_college(request, college_id):
    courses = Course.objects.filter(college_id=college_id)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


#  get number of courses
@api_view(["GET"])
def course_count(request):
    count = Course.objects.count()
    return Response({"count": count})


@api_view(["GET", "POST"])
def getSession(request):
    if request.method == "GET":
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        try:
            data = request.data

            # convert string to date
            start_date = datetime.strptime(data["sdate"], "%Y-%m-%d").date()
            end_date = datetime.strptime(data["edate"], "%Y-%m-%d").date()

            #  get year from date

            session = Session.objects.create(
                ssntitle=str(start_date.year) + "-" + str(end_date.year),
                sdate=data["sdate"],
                edate=data["edate"],
                iscurrent=1,
            )
            return Response(data, status=status.HTTP_201_CREATED)
        except Session.DoesNotExist:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getAgents(request):
    agents = Agent.objects.all()
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data)


# get college by id
@api_view(["GET"])
def get_college_name(request, college_id):
    college = College.objects.get(college_id=college_id)
    serializer = CollegeSerializer(college, many=False)
    return JsonResponse(serializer.data)


#  get course by id
@api_view(["GET"])
def get_course_id(request, crsid):
    course = Course.objects.get(crsid=crsid)
    serializer = CourseSerializer(course, many=False)
    return JsonResponse(serializer.data)
