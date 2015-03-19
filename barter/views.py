from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from .models import User, Feedback, Favor, Offer, Agreement
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from barter.admin import UserCreationForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'barter/index.html', {})

class FavorList(ListView):
    queryset = Favor.objects.all()
    template_name = "barter/favor_list.html"
    paginate_by = 10

class FavorDetail(DetailView):
    model = Favor
    template_name = "barter/favor_detail.html"

class UserDetail(DetailView):
    model = User
    template_name = "barter/user.html"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


def post_feedback(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    try:
        m = request.POST['message']
        r = request.POST['rating']
    except (KeyError, Feedback.DoesNotExist):
        return render(request, 'barter/feedback.html', {
            'error_message': 'Some fields are empty.'
        })
    else:
        fb = Feedback(message=m, rating=r, sender=request.user, reciever=u.id)
        fb.save()


def post_favor(request):
    try:
        t = request.POST['title']
        m = request.POST['message']
        c = request.POST['categories']
    except (KeyError, Feedback.DoesNotExist):
        return render(request, 'barter/favor.html', {
            'error_message': 'Some fields are empty.'
        })
    else:
        fv = Favor(title=t, message=m, author=request.user, categories=c)
        fv.save()


def post_offer(request, favor_id):
    f = get_object_or_404(Favor, pk=favor_id)
    try:
        m = request.POST['message']
    except (KeyError, Feedback.DoesNotExist):
        return render(request, 'barter/offer.html', {
            'error_message': 'Some fields are empty.'
        })
    else:
        of = Offer(message=m, favor=f.id, sender=request.user)
        of.save()


def agreement(request, favor_id, user_id):
    f = get_object_or_404(Favor, pk=favor_id)
    u = get_object_or_404(User, pk=user_id)
    try:
        m = request.POST['message']
        c = request.POST['categories']
    except (KeyError, Feedback.DoesNotExist):
        return render(request, 'barter/agreement.html', {
            'error_message': 'Some fields are empty.'
        })
    else:
        ag = Offer(message=m, favor=f.id, sender=request.user, receiver=u.id)
        ag.save()


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request)