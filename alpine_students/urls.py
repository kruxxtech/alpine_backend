from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("admission/", views.getAdmissions, name="admission"),
    path("student_ids/", views.getStudentIds, name="student_ids"),
    # const students
    path("student/count/", views.students_count, name="student count"),
    path(
        "filters/name/<str:stu_name>/",
        views.student_profile_by_id,
        name="college_students_api",
    ),
    path(
        "filters/<str:college_id>/",
        views.student_profile_detail_by_filters,
        name="college_students_api",
    ),
    path(
        "filters/<str:college_id>/<str:crsid>/",
        views.student_profile_detail_by_filters,
        name="college_students_api",
    ),
    #  fees urls
    path(
        "fee/<str:student_id>/",
        views.student_fee_by_id,
        name="college_students_api",
    ),
    path(
        "fee/<str:student_id>/<str:curr_year>/",
        views.student_fee_by_year,
        name="college_students_api",
    ),
    # search names
    path("names/search/", views.name_search, name="name-search"),
    #  promotions urls
    path("promotions/<str:student_id>", views.promotion_update, name="promotions"),
]
