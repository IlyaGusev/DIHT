from django.shortcuts import render


def custom_400(request):
    values_for_template = {}
    return render(request, 'errors/400.html', values_for_template, status=400)


def custom_403(request):
    values_for_template = {}
    return render(request, 'errors/403.html', values_for_template, status=403)


def custom_404(request):
    values_for_template = {}
    return render(request, 'errors/404.html', values_for_template, status=404)


def custom_405(request):
    values_for_template = {}
    return render(request, 'errors/405.html', values_for_template, status=405)


def custom_500(request):
    values_for_template = {}
    return render(request, 'errors/500.html', values_for_template, status=500)


def custom_501(request):
    values_for_template = {}
    return render(request, 'errors/501.html', values_for_template, status=501)


def custom_502(request):
    values_for_template = {}
    return render(request, 'errors/502.html', values_for_template, status=502)


def custom_503(request):
    values_for_template = {}
    return render(request, 'errors/503.html', values_for_template, status=503)
