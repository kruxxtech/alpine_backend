from django.urls import path
from . import views


urlpatterns = [
    # colleges
    path("colleges/", views.getColleges, name="colleges"),
    path("colleges/count/", views.college_count, name="colleges count"),
    path("colleges/<int:college_id>", views.get_college_name, name="college by id"),
    # courses
    path("courses/", views.getCourses, name="courses"),
    path("courses/count/", views.course_count, name="course count"),
    path("courses/<str:crsid>", views.get_course_id, name="courses"),
    path(
        "colleges/<int:college_id>/courses/",
        views.course_list_by_college,
        name="course list",
    ),
    # sessions
    path("sessions/", views.getSession, name="sessions"),
    path("agents/", views.getAgents, name="agents"),
    #  get college and course by id


    # Delete Paths
    # colleges delete endpoint
    path("colleges/<str:college_id>/delete/", views.delete_college, name="delete_college"),

    # courses delete endpoint
    path("courses/<str:crsid>/delete/", views.delete_course, name="delete_course"),

    # sessions delete endpoint
    path("sessions/<str:ssnid>/delete/", views.delete_session, name="delete_session"),

    # agents delete endpoint
    path("agents/<str:agentsid>/delete/", views.delete_agent, name="delete_agent"),

]
