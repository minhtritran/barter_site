from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'barter/index.html', {})
def user(request):
    return render(request, 'barter/user.html', {"foo": "bar"})