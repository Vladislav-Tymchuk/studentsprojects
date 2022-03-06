from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/<str:groupName>/', views.groupInfo, name='group-info'),
    path('teachers/<int:pk>/', views.teacherInfo, name='teacher-info'),
    path('students/<str:username>/', views.studentInfo, name='student-info'),
    path('authentication/', include('authentication.urls'))
]