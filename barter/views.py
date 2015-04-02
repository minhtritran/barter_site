from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import User, Feedback, Favor, Offer, Agreement, Tag
from .forms import UserCreationForm, UserChangeForm, FavorForm


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


class FavorCreate(CreateView):
    model = Favor
    template_name = "barter/favor_form.html"
    form_class = FavorForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(FavorCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        # etc...
        return initial


class TagList(ListView):
    queryset = Tag.objects.all()
    template_name = "barter/tag_list.html"
    paginate_by = 10


class UserList(ListView):
    queryset = User.objects.all()
    template_name = "barter/user_list.html"
    paginate_by = 10


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


def create_favor(request):
    if request.method == 'POST':
        form = FavorForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            form.save_m2m()
            return HttpResponseRedirect("/")
    form = FavorForm()
    return render(request, 'barter/favor_form.html', {"form": form})


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request)
