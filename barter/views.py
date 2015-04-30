from django.contrib import messages
from django.contrib.auth.views import login
from django.db.models import Max
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import User, Feedback, Favor, Offer, Agreement, Tag
from postman.models import Message
from .forms import UserCreationForm, UserChangeForm, FavorForm, OfferForm, FeedbackForm, PasswordForm
from django.db import connection
from django.template.defaultfilters import slugify


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
        user_pk = kwargs.get('user_pk')
        if slug_id:
            self.queryset = Favor.objects.filter(tags__pk=slug_id).exclude(status='closed')
        elif user_pk:
            self.queryset = Favor.objects.filter(author=user_pk)
        else:
            self.queryset = Favor.objects.all().exclude(status='closed')
        if not self.queryset and slug_id:
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
        cursor.execute('SELECT trader_id FROM barter_favor INNER JOIN barter_offer ON (barter_favor.id = barter_offer.favor_id) INNER JOIN barter_user ON (barter_offer.trader_id = barter_user.id) WHERE barter_favor.id = %s GROUP BY trader_id ', [self.kwargs['pk']])
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


    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        thread = Feedback.objects.filter(receiver=self.kwargs['pk']).order_by('pub_date')

        context['thread'] = thread
        context['currentUser'] = self.request.user
        context['form'] = FeedbackForm(self.request.POST or None)
        context['ratingSize'] = range(0, 5)

        return context


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def user_edit(request, pk):
    if request.user.pk is not pk:
        messages.error(request, 'You cannot edit another user.')
        return redirect('/users/' + pk + '/')
    form = UserChangeForm(request.POST or None, initial={'email': request.user.email,
                                                         'first_name': request.user.first_name,
                                                         'last_name': request.user.last_name,
                                                         'date_of_birth': request.user.date_of_birth,
                                                         'gender': request.user.gender})
    form2 = PasswordForm(request.POST or None)

    if form.is_valid() or form2.is_valid():
        user = User.objects.get(pk=pk)
        obj = UserCreationForm(request.POST, instance=user)
        if form2.is_valid():
            obj.setPassword(form2.password1)
        obj.save()
        messages.success(request, 'User profile successfully updated.')
        return HttpResponseRedirect("/")

    return render(request, 'barter/user_form.html', {"form": form, "form2": form2})


@login_required
def create_favor(request):
    form = FavorForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        for tag in request.POST['tags'].split(','):
            tag = slugify(tag)
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
    trader = int(trader_pk)
    author = Favor.objects.get(pk=pk).author.pk
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
    return render(request, 'barter/offer_form.html', {"form": form, "thread": thread, "trader": trader, "author": author, "user": request.user})


@login_required
def create_feedback(request, pk):
    if request.user.pk is pk:
        messages.error(request, 'You cannot give feedback to yourself.')
        return redirect('/users/' + pk + '/')
    form = FeedbackForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.sender = request.user
        obj.rating = request.POST['rating']
        obj.receiver = User(pk=pk)
        obj.save()
        messages.success(request, 'Feedback has been submitted.')
        return redirect('/users/' + obj.receiver_id + '/')
    return HttpResponseRedirect("/")


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request)


@login_required
def accept_offer(request, pk, trader_pk):
    if(request.POST['acceptbtn']):
        #Close favor post
        curFavor = Favor.objects.get(pk=pk)
        curFavor.status = 'closed'
        curFavor.save()

        #Create new agreement
        curAgreement = Agreement()
        curAgreement.favor = curFavor
        curAgreement.accepter = User.objects.get(pk=trader_pk)
        curAgreement.save()

        #Create message
        curMessage = Message(subject=curFavor.title, body="Favor agreement has been made. You may now initiate conversation with the other user.", moderation_status='a')
        curMessage.sender = User.objects.get(pk=trader_pk)
        curMessage.recipient = curFavor.author
        curMessage.agreement = curAgreement
        curMessage.save()
        curMessage.thread = curMessage
        curMessage.save()
        otherMessage = Message(subject=curFavor.title, body="Favor agreement has been made. You may now initiate conversation with the other user.", moderation_status='a')
        otherMessage.sender = curFavor.author
        otherMessage.recipient = User.objects.get(pk=trader_pk)
        otherMessage.thread = curMessage
        otherMessage.save()
    return HttpResponseRedirect("/messages/")
