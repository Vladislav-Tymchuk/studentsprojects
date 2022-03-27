from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

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


def allTeachers(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        try:
            teachers = Teacher.objects.all()
            context.update({'teachers': teachers})
            return render(request, 'teachers.html', context)
        except:
            return render(request, 'teachers.html', context)


def allStudents(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        try:
            students = Student.objects.all()
            context.update({'students': students})
            return render(request, 'students.html', context)
        except:
            return render(request, 'students.html', context)


def groupInfo(request, groupName):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        student = request.user
        group = Group.objects.get(groupName = groupName)
        students = Student.objects.filter(group = group.id)
        groupTeacher = Group.objects.get(groupName = groupName).groupTeacher
        context.update({'students': students, 'group': group, 'groupTeacher': groupTeacher})

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
    


def teacherInfo(request, username):
    context = {'group': False}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        user = CustomUser.objects.get(username = username)
        try:           
            teacher = Teacher.objects.get(mainProfile = user)
            achievements = Achievement.objects.filter(person = user)
            context.update({'achievements': achievements})
            context.update({'user': user, 'teacher': teacher})
        except:
            context.update({'user': user, 'teacher': False})

        try:
            group = Group.objects.get(groupTeacher = teacher.id)
            context['group'] = group
        except:
            pass

        if request.user.id == user.id:
            context.update({'ownProfile': True})

            if request.method == 'POST':
                form = AchievementForm(request.POST, request.FILES)       
                if form.is_valid():
                    ancet = form.save(commit=False)
                    userAchievement = Achievement.objects.create(person = request.user, achievement = ancet.achievement, name = ancet.name)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    userAchievement.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form = AchievementForm()
                context.update({'form': form})
                return render(request, 'teacher-info.html', context)

        return render(request, 'teacher-info.html', context)


def studentInfo(request, username):
    context = {}
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:

        person = CustomUser.objects.get(username = username)
        student = CustomUser.objects.get(id = person.id)
        try:
            studentGroup = Student.objects.get(student = student).group
            groupTeacher = Student.objects.get(student = student).group
            achievements = Achievement.objects.filter(person = student).order_by('-id')

            context.update({'achievements': achievements, 'student': student, 'studentGroup': studentGroup, 'groupTeacher': groupTeacher})
        except:
            studentGroup = False
            groupTeacher = False
            achievements = Achievement.objects.filter(person = student).order_by('-id')

            context.update({'achievements': achievements, 'student': student, 'studentGroup': studentGroup, 'groupTeacher': groupTeacher})

        if request.user.id == student.id:
            context.update({'ownProfile': True})

            if request.method == 'POST':
                form = AchievementForm(request.POST, request.FILES)       
                if form.is_valid():
                    ancet = form.save(commit=False)
                    userAchievement = Achievement.objects.create(person = request.user, achievement = ancet.achievement, name = ancet.name)
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
        try:
            group = get_object_or_404(Group, groupName = groupName)
            if Student.objects.filter(student = person).exists():
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                Student.objects.create(student = person, group = group)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def leaveGroup(request, groupName):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        person = request.user
        try:
            group = Group.objects.get(groupName = groupName)
            if Student.objects.filter(student = person).exists():
                student = Student.objects.get(student = person, group = group)
                student.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkAchievement(request, id):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        try:
            achievement = Achievement.objects.get(id = id)
            pdf_file = achievement.achievement.path       
            response = FileResponse(open(pdf_file, 'rb'))

            return response
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deleteAchievement(request, id):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        try:
            achievement = get_object_or_404(Achievement, id = id)
            if achievement.person == request.user:
                achievement.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
