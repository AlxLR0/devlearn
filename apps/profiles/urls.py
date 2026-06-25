from django.urls import path
from .views import ProfileUpdateView  # Vista para editar perfil (viene de views.py) ✏️

urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile'),  # /profile/ -> editar mi perfil 👤
]
