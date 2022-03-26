from django.shortcuts import render

def page404(request, exception):
    return render(request, '404.html', status=404)


def page500(request):
    return render(request, '500.html', status=500)

