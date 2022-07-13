from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import CustomUser
from .forms import AchievementForm

from .models import Achievement, Group


def home(request):

    context = {}   
    groups = Group.objects.all()
    context.update({'groups': groups})

    return render(request, 'home.html', context)


def allTeachers(request):

    context = {}
    try:
        teachers = CustomUser.objects.filter(isTeacher = True)
        context.update({'teachers': teachers})

        return render(request, 'teachers.html', context)

    except:

        return render(request, 'teachers.html', context)


def allStudents(request):

    context = {}
    try:
        students = CustomUser.objects.filter(isTeacher = False)
        context.update({'students': students})

        return render(request, 'students.html', context)

    except:

        return render(request, 'students.html', context)


def groupInfo(request, groupName):

    context = {}

    user = request.user

    group = Group.objects.get(groupName = groupName)
    students = CustomUser.objects.filter(userGroup = group.id)
    groupTeacher = Group.objects.get(groupName = groupName).groupTeacher

    context.update({'students': students, 'group': group, 'groupTeacher': groupTeacher})

    try:
        studentCheck = CustomUser.objects.get(id = user.id)
        context.update({'isStudent': True})
        try:
            context.update({'requestGroup': studentCheck.userGroup.groupName})
        except:
            context.update({'requestGroup': 'ошибка'})
    except:
        context.update({'isStudent': False})

    return render(request, 'group-info.html', context)
    


def teacherInfo(request, username):

    context = {'group': False}

    # преподаватель, которому принадлежит страница
    user = CustomUser.objects.get(username = username)

    try:
        achievements = Achievement.objects.filter(person = user)
        context.update({'achievements': achievements})
        context.update({'user': user})

    except:       
        context.update({'user': user, 'teacher': False})

    try:
        group = Group.objects.get(groupTeacher = user.id)
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
                userAchievement.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = AchievementForm()
            context.update({'form': form})

            return render(request, 'teacher-info.html', context)

    return render(request, 'teacher-info.html', context)


def studentInfo(request, username):

    context = {}

    # студент, которому принадлежит страница
    try:
        user = CustomUser.objects.get(username = username)
    except:
        return render(request, 'student-info.html', context)

    try:
        studentGroup = user.userGroup
        groupTeacher = Group.objects.get(id = studentGroup.id).groupTeacher
        achievements = Achievement.objects.filter(person = user).order_by('-id')

        context.update({'achievements': achievements, 'user': user, 'studentGroup': studentGroup, 'groupTeacher': groupTeacher})
    except:
        studentGroup = False
        groupTeacher = False
        achievements = Achievement.objects.filter(person = user).order_by('-id')

        context.update({'achievements': achievements, 'user': user, 'studentGroup': studentGroup, 'groupTeacher': groupTeacher})

    if request.user.id == user.id:
        context.update({'ownProfile': True})

        if request.method == 'POST':
            form = AchievementForm(request.POST, request.FILES)       
            if form.is_valid():
                ancet = form.save(commit=False)
                userAchievement = Achievement.objects.create(person = request.user, achievement = ancet.achievement, name = ancet.name)
                userAchievement.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
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
        user = request.user
        try:
            group = get_object_or_404(Group, groupName = groupName)
            if not user.userGroup.null:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user.userGroup = group
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def leaveGroup(request, groupName):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        user = request.user
        try:
            if not user.userGroup.null:
                user.userGroup = ''
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkAchievement(request, id):

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
