from django.conf.urls import url

from Two import views

urlpatterns = [
    # url(r'^students/(\d+)/', views.student),

    url(r'^grades/', views.grades),
    url(r'^students/(\d+)/', views.students, name='get_students'),
    url(r'^gettime/(\d+)/(\d+)/(\d+)/', views.get_time, name='get_time'),
    url(r'^getdate/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/', views.get_date, name='get_date'),
    url(r'^learn/', views.learn, name='learn'),
    url(r'^studentpage/(\d+)/', views.get_studentpage, name='get_studentpage'),
    url(r'^deletestudent/(\d+)/', views.delete_student, name='delete_student'),
    url(r'^addstudent/', views.add_student, name='add_student'),
    url(r'^haverequest/', views.have_request),

    url(r'^test/', views.test),
]