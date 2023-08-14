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
        college_code = request.data.get("college_code")
        if college_id:
            try:
                existing_college = College.objects.get(college_id=college_id)
                if existing_college.college_code != college_code:
                    try:
                        existing_college_with_code = College.objects.get(college_code=college_code)
                        return Response(
                            {"error": "College code already exists."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    except College.DoesNotExist:
                        pass

                serializer = CollegeSerializer(existing_college, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except College.DoesNotExist:
                return Response(
                    {"error": "College with the given ID does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            # If college_id is not provided, check if a college with the given college_code already exists
            try:
                existing_college_with_code = College.objects.get(college_code=college_code)
                return Response(
                    {"error": "College code already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except College.DoesNotExist:

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
        data = request.data

        course_id = data.get("crsid")
        if not course_id:
            return Response(
                {"error": "Course ID (crsid) is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_exists = Course.objects.filter(crsid=course_id).exists()
        update_flag = data.get('update_flag', False)

        # If the course with given course_id exists and update_flag is true
        if course_exists and update_flag:
            course_instance = Course.objects.get(crsid=course_id)

            # Check if the updated course name exists for the given college
            if Course.objects.filter(college_id=data.get("college_id"), course=data["course"]).exclude(crsid=course_id).exists():
                return Response(
                    {"error": "Course name already exists for the given college."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the existing course object
            course_instance.college_id = data["college_id"]
            course_instance.course = data["course"]
            course_instance.duration = data["duration"]
            course_instance.save()

            serializer = CourseSerializer(course_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the course with given course_id doesn't exist but update_flag is true
        elif not course_exists and update_flag:
            return Response(
                {"error": "No Course found with the provided Course ID for updating."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If course doesn't exist and the intention is to create a new one
        elif not course_exists:
            # Check if the given course name exists for the college
            if Course.objects.filter(college_id=data["college_id"], course=data["course"]).exists():
                return Response(
                    {"error": "Course name already exists for the given college."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the new course object
            course = Course.objects.create(
                college_id=data["college_id"],
                course=data["course"],
                duration=data["duration"],
                crsid=data["crsid"],
            )

            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If course exists but the intention was not to update
        else:
            return Response(
                {"error": "Course ID already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    """
    View to handle creation or update of an Agent.
    - The 'agentsid' is used to determine if an agent exists.
    - If 'agentsid' exists and 'update_flag' is true in the request data, the agent is updated.
    - If 'agentsid' exists and 'update_flag' is absent or false, an error is returned.
    - If 'agentsid' doesn't exist, a new agent is created.
    """
    if request.method == "POST":
        data = request.data

        agentsid = data.get("agentsid")
        if not agentsid:
            return Response(
                {"error": "Agent ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        agent_exists = Agent.objects.filter(agentsid=agentsid).exists()
        update_flag = data.get('update_flag', False)

        # If the agent with given agentsid exists and update_flag is true
        if agent_exists and update_flag:
            agent = Agent.objects.get(agentsid=agentsid)

            # Update the existing agent object
            agent.agentname = data.get("agentname", agent.agentname)
            agent.email = data.get("email", agent.email)
            agent.contact = data.get("contact", agent.contact)
            agent.save()

            serializer = AgentSerializer(agent)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the agent with given agentsid doesn't exist but update_flag is true
        elif not agent_exists and update_flag:
            return Response(
                {"error": "No Agent found with the provided agentsid for updating."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If agent doesn't exist and the intention is to create a new one
        elif not agent_exists:
            agent = Agent.objects.create(
                agentsid=data["agentsid"],
                agentname=data.get("agentname"),
                email=data.get("email"),
                contact=data.get("contact"),
            )

            serializer = AgentSerializer(agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If agent exists but the intention was not to update
        else:
            return Response(
                {"error": "Agent ID already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
