from django.urls import path
from .views import SupportView  # Vista de soporte (views.py) 📧

urlpatterns = [
    path('', SupportView.as_view(), name='support'),  # /support/ -> formulario de contacto 💬
]