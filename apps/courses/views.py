from django.shortcuts import render

# Create your views here.
def course_list(request):
    courses=[{
        
    }]
    return render(request, "courses/courses.html")


def course_detail(request):
    pass

def course_lessons(request):
    pass



