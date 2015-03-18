from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from barter.admin import UserCreationForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'barter/index.html', {})

def user(request):
    return render(request, 'barter/user.html', {"foo": "bar"})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})