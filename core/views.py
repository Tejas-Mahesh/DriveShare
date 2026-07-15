from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def error_403(request, exception):

    return render(
        request,
        "errors/403.html",
        status=403
    )