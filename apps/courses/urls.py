# ⚠️ NOTA: Este archivo ya NO se usa activamente.
# Las URLs ahora están divididas en urls/instructor.py y urls/student.py
# Se mantiene por referencia / compatibilidad.
from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("detail/<str:slug>/", views.course_detail, name="course_detail"),
    path("lessons/<str:slug>/", views.course_lessons, name="course_lessons"),
]