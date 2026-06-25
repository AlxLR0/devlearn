from django.urls import path
from . import views  # Vistas del dashboard (views.py) 🏠

urlpatterns = [
    path('', views.index, name='dashboard'),  # Ruta raíz del dashboard 📊
]