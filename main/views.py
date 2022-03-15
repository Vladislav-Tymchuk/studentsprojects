from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from authentication.models import CustomUser
from .forms import AchievementForm

from .models import Achievement, Group, Student, Teacher 


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
        student = request.user
        group = Group.objects.get(groupName = groupName)
        students = Student.objects.filter(group = group.id)
        context.update({'students': students, 'group': group})
        try:
            studentCheck = Student.objects.get(student = student)
            context.update({'isStudent': True})
            try:
                context.update({'requestGroup': studentCheck.group.groupName})
            except:
                context.update({'requestGroup': 'ошибка'})
        except:
            context.update({'isStudent': False})
        return render(request, 'group-info.html', context)
    


def teacherInfo(request, pk):
    context = {'group': False}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        teacher = Teacher.objects.get(id = pk)
        context.update({'teacher': teacher})

        try:
            group = Group.objects.get(groupTeacher = teacher.id)
            context['group'] = group
        except:
            pass
        return render(request, 'teacher-info.html', context)


def studentInfo(request, username):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:

        person = CustomUser.objects.get(username = username)
        student = CustomUser.objects.get(id = person.id)
        studentGroup = Student.objects.get(student = student).group
        groupTeacher = Student.objects.get(student = student).group

        achievements = Achievement.objects.filter(student = student)

        context.update({'achievements': achievements, 'student': student, 'studentGroup': studentGroup, 'groupTeacher': groupTeacher})

        if request.user.id == student.id:
            context.update({'ownProfile': True})

            if request.method == 'POST':
                form = AchievementForm(request.POST, request.FILES)       
                if form.is_valid():
                    ancet = form.save(commit=False)
                    userAchievement = Achievement.objects.create(student = request.user, achievement = ancet.achievement, name = ancet.name)
                    if userAchievement.exists():
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        userAchievement.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form = AchievementForm()
                context.update({'form': form})
                return render(request, 'student-info.html', context)
        else:
            return render(request, 'student-info.html', context)


def joinGroup(request, groupName):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        person = request.user
        group = Group.objects.get(groupName = groupName)
        if Student.objects.filter(student = person).exists():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:

            Student.objects.create(student = person, group = group)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def leaveGroup(request, groupName):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        person = request.user
        group = Group.objects.get(groupName = groupName)
        if Student.objects.filter(student = person).exists():
            student = Student.objects.get(student = person, group = group)
            student.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkAchievement(request, id):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        achievement = Achievement.objects.get(id = id)
        pdf_file = achievement.achievement.path

        
        response = FileResponse(open(pdf_file, 'rb'))

        return response

