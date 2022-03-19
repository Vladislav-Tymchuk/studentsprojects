from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/<str:groupName>/', views.groupInfo, name='group-info'),
    path('teachers/<int:pk>/', views.teacherInfo, name='teacher-info'),
    path('students/<str:username>/', views.studentInfo, name='student-info'),
    path('join-group/<str:groupName>', views.joinGroup, name='join-group'),
    path('leave-group/<str:groupName>', views.leaveGroup, name='leave-group'),
    path('check-achievement/<int:id>', views.checkAchievement, name='check-achievement'),
    path('delete-achievement/<int:id>', views.deleteAchievement, name='delete-achievement'),
    path('authentication/', include('authentication.urls'))
]