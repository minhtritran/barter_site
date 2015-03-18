from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import User, Feedback, Favor, Offer, Agreement


# Create your views here.
def home(request):
    return render(request, 'barter/index.html', {})


def user(request):
    return render(request, 'barter/user.html', {"foo": "bar"})


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
        return render(request, 'barter/favor.html', {
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
        return render(request, 'barter/favor.html', {
            'error_message': 'Some fields are empty.'
        })
    else:
        ag = Offer(message=m, favor=f.id, sender=request.user, receiver=u.id)
        ag.save()
