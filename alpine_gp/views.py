from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import *

from .serializers import *

# Create your views here.


@api_view(["GET"])
def getColleges(request):
    colleges = College.objects.all()
    serializer = CollegeSerializer(colleges, many=True)
    return Response(serializer.data)


#  get number of college
@api_view(["GET"])
def college_count(request):
    count = College.objects.count()
    return Response({"count": count})


@api_view(["GET"])
def getCourses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


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


@api_view(["GET"])
def getSession(request):
    sessions = Session.objects.all()
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)


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
