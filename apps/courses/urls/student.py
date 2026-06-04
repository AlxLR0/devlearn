from django.urls import path
from django.views.generic import RedirectView
from ..views import student

app_name = 'student'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='student:course_list', permanent=True)),
    path("courses/", student.course_list, name="course_list"),
    path("detail/<str:slug>", student.course_detail,
         name="course_detail"),
    path("<str:slug>/lessons/<int:content_id>/",
         student.course_lessons, name="course_lessons"),
    path("<str:slug>/lessons/",
         student.course_lessons, name="course_lessons"),
    path('content/<int:content_id>/complete/',
         student.mark_complete, name="mark_complete")
]