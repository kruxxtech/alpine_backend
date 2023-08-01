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
        # Check if college_id is provided in the request data
        college_id = request.data.get("college_id")
        if college_id:
            try:
                # get the existing college record by college_id
                college = College.objects.get(college_id=college_id)
                serializer = CollegeSerializer(college, data=request.data)
            except College.DoesNotExist:
                # If college_id does not correspond to an existing record, create a new one
                serializer = CollegeSerializer(data=request.data)
        else:
            # If college_id is not provided, create a new record
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
            try:
                course_id = data.get("crsid")
                course = Course.objects.get(crsid=course_id)
                # Update the existing course object
                course.college_id = data["college_id"]
                course.course = data["course"]
                course.duration = data["duration"]
                course.save()
            except Course.DoesNotExist:
                # If no existing Course Object, create a new one
                course = Course.objects.create(
                    college_id=data["college_id"],
                    course=data["course"],
                    duration=data["duration"],
                    crsid=data["crsid"],
                )
            return Response(data, status=status.HTTP_201_CREATED)
        except:
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

            session_title = str(start_date.year) + "-" + str(end_date.year)
            try:
                session_id = data.get("ssnid")
                # get the existing session record by ssnid
                session = Session.objects.get(ssnid=session_id)
                # Update the existing session object
                session.ssntitle = session_title
                session.sdate = data["sdate"]
                session.edate = data["edate"]
                session.iscurrent = data["iscurrent"]
                session.save()
            except Session.DoesNotExist:
                # If no existing ssnid, create a new one
                session = Session.objects.create(
                    ssntitle=session_title,
                    sdate=data["sdate"],
                    edate=data["edate"],
                    iscurrent=data["iscurrent"],
                )
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def getAgents(request):
    if request.method == "GET":
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        try:
            data = request.data
            try:
                agentsid = data.get("agentsid")
                agent = Agent.objects.get(agentsid=agentsid)
                # Update the existing agent object
                agent.agentname = data.get("agentname", agent.agentname)
                agent.email = data.get("email", agent.email)
                agent.contact = data.get("contact", agent.contact)
                agent.save()
            except Agent.DoesNotExist:
                # If no existing Agent object, create a new one
                agent = Agent.objects.create(
                    agentsid=data["agentsid"],
                    agentname=data.get("agentname"),
                    email=data.get("email"),
                    contact=data.get("contact"),
                )
            serializer = AgentSerializer(agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


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
