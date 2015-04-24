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
from django.db import connection


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
        listOffers = []

        # offers = Favor.objects.get(pk=self.kwargs['pk']).offers.values('trader').annotate(max_date=Max('pub_date')).filter(date=F('max_date'))
        # offers = Favor.objects.get(pk=self.kwargs['pk']).offers.order_by('trader', '-pub_date').distinct('trader')
        # offers = Favor.objects.raw('SELECT * FROM barter_favor INNER JOIN barter_offer ON (barter_favor.id = barter_offer.favor_id) WHERE barter_favor.id = %s GROUP BY trader_id HAVING MAX(barter_offer.pub_date)', [self.kwargs['pk']])
        cursor = connection.cursor()
        cursor.execute('SELECT trader_id FROM barter_favor INNER JOIN barter_offer ON (barter_favor.id = barter_offer.favor_id) INNER JOIN barter_user ON (barter_offer.trader_id = barter_user.id) WHERE barter_favor.id = 3 GROUP BY trader_id ', [self.kwargs['pk']])
        result = cursor.fetchall()

        for row in result:
            offers = Favor.objects.raw('SELECT * FROM barter_favor INNER JOIN barter_offer ON (barter_favor.id = barter_offer.favor_id) INNER JOIN barter_user ON (barter_offer.trader_id = barter_user.id) WHERE barter_favor.id = %s AND trader_id = %s ORDER BY barter_offer.pub_date DESC', [self.kwargs['pk'], row[0]])[0]
            listOffers.append(offers)
        context['offer_threads'] = listOffers
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
    if(request.POST['acceptbtn']):
        print(int(request.POST['trader']))
    return HttpResponseRedirect("/favors/" + pk)
