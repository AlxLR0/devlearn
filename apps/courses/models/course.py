from django.db import models
from django.conf import settings
from .category import Category

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    overview = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='courses')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    class CourseCategory(models.Model):
        course = models.ForeignKey(Course, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

        class Meta:
            unique_together = ('course', 'category')
        
        def __str__(self):
            return f'{self.course.title} - {self.category.name}'
    
    