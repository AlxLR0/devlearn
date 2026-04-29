from django.db import models

#aqui se importan los modelos que se crearan en la carpeta models
from .models.user import User
from .models.instructor import InstructorProfile

# Create your models here.
#esto es para que cuando hagamos makemigrations se detecten los modelos automaticamente sin tener que importarlos manualmente
