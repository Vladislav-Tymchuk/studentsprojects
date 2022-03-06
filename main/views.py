from django.shortcuts import redirect, render

from authentication.models import CustomUser

from .models import Group, Student, Teacher

def home(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        groups = Group.objects.all()
        context.update({'groups': groups})
        return render(request, 'home.html', context)


def groupInfo(request, groupName):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        group = Group.objects.get(groupName = groupName)
        students = Student.objects.filter(group = group.id)
        context.update({'students': students, 'group': group})
        return render(request, 'group-info.html', context)
    


def teacherInfo(request, pk):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        teacher = Teacher.objects.get(id = pk)
        context.update({'teacher': teacher})
        return render(request, 'teacher-info.html', context)


def studentInfo(request, username):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        person = CustomUser.objects.get(username = username)
        student = Student.objects.get(id = person.id)
        context.update({'student': student})
        return render(request, 'student-info.html', context)
