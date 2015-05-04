from django.contrib import messages
from django.contrib.auth.views import login
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import User, Feedback, Favor, Offer, Agreement, Tag
from postman.models import Message
from .forms import UserCreationForm, UserChangeForm, FavorForm, OfferForm, FeedbackForm, PasswordForm, FavorEditForm
from django.db import connection
from django.template.defaultfilters import slugify
from django.db.models import Count


# Create your views here.
def about(request):
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
        if self.request.user.is_authenticated():
            if not self.request.user.is_confirmed:
                messages.warning(self.request, 'To reply, please verify your email.')

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


class TagList(ListView):
    queryset = Tag.objects.all().annotate(num_favors=Count('favor')).order_by('-num_favors')
    template_name = "barter/tag_list.html"
    paginate_by = 25


class UserList(ListView):
    queryset = User.objects.filter(is_admin=False)
    template_name = "barter/user_list.html"
    paginate_by = 25


class UserDetail(DetailView):
    model = User
    template_name = "barter/user.html"

    def get_context_data(self, **kwargs):
        current_user = self.kwargs['pk']
        context = super(UserDetail, self).get_context_data(**kwargs)
        fb_thread = Feedback.objects.filter(receiver=current_user).order_by('pub_date')
        favor_thread = Favor.objects.filter(author=current_user).order_by('pub_date')

        stars = []
        for i in range(1, 6):
            stars.append(len(Feedback.objects.filter(rating=i, receiver=current_user)))

        context['fb_thread'] = fb_thread
        context['favor_thread'] = favor_thread
        context['currentUser'] = self.request.user
        context['form'] = FeedbackForm(self.request.POST or None)
        context['max'] = max(stars)

        context['stars'] = stars

        return context


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.send_confirmation_email(request)
            messages.success(request, 'Registration successful!  An email has been sent to you for verification.')
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def user_verify(request, pk, key):
    user = User.objects.get(pk=pk)
    user.confirm_email(key)
    messages.success(request, 'Your email has been verified!')
    return HttpResponseRedirect("/")


@login_required
def user_verify_resend(request, pk):
    if int(request.user.pk) is not int(pk):
        messages.error(request, 'You do not have permission to do that.')
        return redirect('/users/' + pk + '/')
    user = User.objects.get(pk=pk)
    user.send_confirmation_email(request)
    messages.success(request, 'An email has been sent to you for verification.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def user_edit(request, pk):
    if int(request.user.pk) is not int(pk):
        messages.error(request, 'You cannot edit another user.')
        return redirect('/users/' + pk + '/')
    user = User.objects.get(pk=pk)
    form = UserChangeForm(request.POST or None, instance=user, initial={'first_name': request.user.first_name,
                                                                        'last_name': request.user.last_name,
                                                                        'date_of_birth': request.user.date_of_birth,
                                                                        'gender': request.user.gender})
    form2 = PasswordForm(request.user, request.POST or None)

    if form.is_valid():
        form.save()
    if form2.is_valid():
        user.set_password(form2.cleaned_data['password1'])
        user.save()
    if form.is_valid() and (not form2.has_changed() or form2.is_valid()):
        messages.success(request, 'User profile successfully updated.')
        return HttpResponseRedirect("/")

    return render(request, 'barter/user_edit.html', {"form": form, "form2": form2})


@login_required
def favor_edit(request, pk):
    favor = Favor.objects.get(pk=pk)
    if int(request.user.pk) is not int(favor.author.pk):
        messages.error(request, 'You are not the author of this favor.')
        return HttpResponseRedirect("/favors/" + pk)
    form = FavorEditForm(request.POST or None, instance=favor,
                         initial={'title': favor.title, 'message': favor.message})
    if form.is_valid():
        form.save()
        messages.success(request, 'Favor successfully updated.')
        return HttpResponseRedirect("/favors/" + pk)
    return render(request, 'barter/favor_edit.html', {"form": form, "favor_pk": pk})


@login_required
def favor_delete(request, pk):
    favor = Favor.objects.get(pk=pk)
    if int(request.user.pk) is not int(favor.author.pk):
        messages.error(request, 'You are not the author of this favor.')
        return HttpResponseRedirect("/favors/" + pk)
    favor.delete()
    messages.success(request, 'Favor deleted.')
    return HttpResponseRedirect("/favors/")


@login_required
def create_favor(request):
    if not request.user.is_confirmed:
        messages.warning(request, 'Please verify your email.')
    form = FavorForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        for tag in request.POST['tags'].split(','):
            if tag is not '':
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
def create_feedback(request, pk, pk2=0):
    if int(request.user.pk) is int(pk):
        messages.error(request, 'You cannot give feedback to yourself.')
        return redirect('/users/' + pk + '/')
    if pk2 != 0:
        try:
            feedback = Feedback.objects.get(pk=int(pk2), sender=request.user.pk)
        except Feedback.DoesNotExist:
            messages.error(request, 'That Feedback does not exist.')
            return redirect('/users/' + pk + '/')
        form = FeedbackForm(request.POST or None, instance=feedback)
    else:
        if request.session.get('user-feedback') != int(pk):
            return redirect('/home/')
        form = FeedbackForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.sender = request.user
        obj.rating = request.POST['rating']
        obj.receiver = User(pk=pk)
        if pk2 != 0:
            obj.last_edit = timezone.now()
        obj.save()
        messages.success(request, 'Feedback has been submitted.')
        request.session['user-feedback'] = None
        return redirect('/users/' + obj.receiver_id + '/')
    return render(request, 'barter/feedback_form.html', {"form": form})


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
