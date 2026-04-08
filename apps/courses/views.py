from django.shortcuts import render

# Create your views here.
def course_list(request):
    courses=[
        {
        'id': 1,
        'level': 'Principiante',
        'rating': 4.5,
        'course_title': 'Introduccion a python',
        'instructor': 'Alison Walsh',
        'course_image': 'images/curso_1.jpg',
        'instructor_image': 'https://randomuser.me/api/portraits/women/68.jpg',
        },
        {
            'id': 2,
            'level': 'Principiante',
            'rating': 4.8,
            'course_title': 'Introduccion a Django',
            'instructor': 'Patty Kutch',
            'course_image': 'images/curso_2.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/20.jpg',
        },
        {
            'id': 3,
            'level': 'Avanzado',
            'rating': 4.8,
            'course_title': 'Django avanzado',
            'instructor': 'Alonzo Murray',
            'course_image': 'images/curso_3.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/men/32.jpg',
        },
        {
            'id': 4,
            'level': 'Avanzado',
            'rating': 4.7,
            'course_title': 'Fast api avanzado',
            'instructor': 'Gregory Harris',
            'course_image': 'images/curso_4.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/men/45.jpg',
        }
    ]
    return render(request, "courses/courses.html", {'courses': courses})


def course_detail(request):
    course ={
        'course_title': 'Introduccion a python',
        'course_link': 'course_lessons',
        'course_image': 'images/curso_1.jpg',
        'info_course':{
            'lessons': 79,
            'duration': 8,
            'instructor': 'Alex Lopez',
        },
        'course_content':[
            {
                'id':1,
                'name': 'Introduccion al curso',
                'lessons':[
                    {
                        'id':1,
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'video',
                        'duration': '5:00',
                    },
                    {
                        'id':2,
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                        'duration': '5:00',
                    },
                ]
            },
            {
                'id':2,
                'name': 'Fundamentos necesarios de Python',
                'lessons':[
                    {
                        'id':1,
                        'name': 'Variables y tipos de datos',
                        'type': 'video',
                        'duration': '5:00',
                    },
                    {
                        'id':2,
                        'name': 'Condicionales y bucles',
                        'type': 'video',
                        'duration': '5:00',
                    },
                ]
            }
        ]
    }
    return render(request, 'courses/course_detail.html', {'course': course})

def course_lessons(request):
    lesson ={
        'course_title': 'Introduccion a python',
        'progress': 30,
        'course_content':[
            {
                'id':1,
                'name': 'Introduccion al curso',
                'total_lessons': 6,
                'complete_lessons': 2,
                'lessons':[
                    {
                        'id':1,
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'video',
                        'duration': '5:00',
                    },
                    {
                        'id':2,
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                        'duration': '5:00',
                    },
                ]
            },
            {
                'id':2,
                'name': 'Fundamentos necesarios de Python',
                'total_lessons': 6,
                'complete_lessons': 2,
                'lessons':[
                    {
                        'id':1,
                        'name': 'Variables y tipos de datos',
                        'type': 'video',
                        'duration': '5:00',
                    },
                    {
                        'id':2,
                        'name': 'Condicionales y bucles',
                        'type': 'video',
                        'duration': '5:00',
                    },
                ]
            }
            
        ]
    }
    return render(request, 'courses/course_lessons.html', {'lesson': lesson})



