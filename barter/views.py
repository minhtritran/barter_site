from django.contrib import messages
from django.contrib.auth.views import login
from django.db.models import Max
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import User, Feedback, Favor, Offer, Agreement, Tag
from .forms import UserCreationForm, UserChangeForm, FavorForm, OfferForm


# Create your views here.
@login_required
def home(request):
    return render(request, 'barter/index.html', {})


class FavorList(ListView):
    template_name = "barter/favor_list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        slug_id = Tag.objects.filter(slug=slug)
        if slug_id:
            self.queryset = Favor.objects.filter(tags__pk=slug_id)
        else:
            self.queryset = Favor.objects.all()
        if not self.queryset:
            messages.warning(request, "No favors with this tag.")
        return super(FavorList, self).get(request, *args, **kwargs)


class FavorDetail(DetailView):
    model = Favor
    template_name = "barter/favor_detail.html"

    def get_context_data(self, **kwargs):
        context = super(FavorDetail, self).get_context_data(**kwargs)
        list = []

        #offers = Favor.objects.get(pk=self.kwargs['pk']).offers.values('trader').annotate(max_date=Max('pub_date')).filter(date=F('max_date'))
        offers = Favor.objects.get(pk=self.kwargs['pk']).offers.order_by('trader', '-pub_date').distinct('trader')
        #offers = Favor.objects.raw('SELECT * FROM favor INNER JOIN offer ON(favor_pk = offer_favor) WHERE favor_pk = %s GROUP BY trader HAVING MAX(offer_pub_date)', [self.kwargs['pk']])
        
        list.append(offers)

        context['offer_threads'] = list
        return context

    """
    def post(self, request, *args, **kwargs):
        context = super(FavorDetail, self).get_context_data(**kwargs)
        print(request.POST["trader"])

        return self.render_to_response(context)
    """

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
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


def create_favor(request):
    form = FavorForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        for tag in request.POST['tags'].split(','):
            try:
                t = Tag.objects.get(slug=tag)
            except Tag.DoesNotExist:
                t = Tag(slug=tag)
                t.save()
            obj.tags.add(Tag.objects.get(slug=tag))
        form.save_m2m()
        messages.success(request, 'Favor has been created.')
        return HttpResponseRedirect("/")
    messages.error(request, 'The form is incomplete.')
    return render(request, 'barter/favor_form.html', {"form": form})


def create_offer(request, pk, trader_pk):
    thread = Favor.objects.get(pk=pk).offers.filter(trader=trader_pk).order_by('pub_date')
    form = OfferForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.favor = Favor(pk=pk)
        obj.trader = User(pk=trader_pk)
        if request.user.id is Favor.objects.get(pk=pk).author_id:
            obj.made_by_asker = True
        obj.save()
        messages.success(request, 'Offer has been submitted.')
        return redirect('/favors/' + obj.favor_id + '/')
    return render(request, 'barter/offer_form.html', {"form": form, "thread": thread})


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request)

def accept_offer(request, pk, trader_pk):
    if(request.POST.get('acceptbtn')):
        print(int(request.POST.get('trader')) )
    return render(request, 'barter/favor_detail.html')

