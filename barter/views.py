from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from barter.forms import UserCreateForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'barter/index.html', {})

def user(request):
    return render(request, 'barter/user.html', {"foo": "bar"})

def register(request):
    form = UserCreateForm()
    return render(request, 'registration/register.html', {"form": form})