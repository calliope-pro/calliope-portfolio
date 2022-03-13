import os
import uuid

import jwt
import payjp
import requests
from bs4 import BeautifulSoup
from calliope_bot.models import LineProfile
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from django.views.generic.edit import DeleteView
from payjp.error import PayjpException

from .forms import BssForm, ContactForm
from .models import Bss


class HomeView(TemplateView):
    template_name = "calliope_web/home.html"
    atcoder_rate = -1

    def get_atcoder_rate(self):
        """
        自作(Atcoderのレート取得)
        """
        response = requests.get('https://atcoder.jp/users/calliope')
        soup = BeautifulSoup(response.content, features='html5lib')
        atcoder_rate_string = soup.select_one(
            '#main-container > div.row > div.col-md-9.col-sm-12 > table > tbody > tr:nth-child(2) > td > span'
        ).decode_contents()

        self.atcoder_rate = int(atcoder_rate_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_atcoder_rate()
        context['atcoder_rate'] = self.atcoder_rate
        return context


class ContactView(FormView):
    template_name = 'calliope_web/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('calliope_web:contact')

    def get_initial(self):
        return {'username': self.request.user.username}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            title = (
                f"{form.cleaned_data['title']}-by-{self.request.user.username}"
            )
            body = f"{form.cleaned_data['body']}"
            recipient_list = [
                form.cleaned_data['email'],
                settings.EMAIL_HOST_USER,
            ]
            send_mail(
                subject=title,
                message=body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


LINE_REDIRECT_URL = settings.LINE_REDIRECT_URL
LINE_CHANNEL_ID = settings.LINE_CHANNEL_ID
LINE_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET


class ProfileView(TemplateView):
    template_name = 'calliope_web/profile.html'
    LINE_RANDOM_STATE = str(uuid.uuid1())
    LINE_NONCE = str(uuid.uuid4())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channel_id'] = LINE_CHANNEL_ID
        context['redirect_url'] = LINE_REDIRECT_URL
        context['random_state'] = self.LINE_RANDOM_STATE
        context['nonce'] = self.LINE_NONCE
        self.request.session['nonce'] = self.LINE_NONCE
        lineprofile, _ = LineProfile.objects.get_or_create(
            user=self.request.user
        )
        if lineprofile.line_id:
            context['lineprofile'] = lineprofile
        else:
            context['line_id'] = None
        return context


class LineLinkView(View):
    URI_ACCESS_TOKEN = 'https://api.line.me/oauth2/v2.1/token'
    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    def get(self, request, *args, **kwargs):
        request_code = request.GET.get("code")
        data_params = {
            "grant_type": "authorization_code",
            "code": request_code,
            "redirect_uri": LINE_REDIRECT_URL,
            "client_id": LINE_CHANNEL_ID,
            "client_secret": LINE_CHANNEL_SECRET,
        }

        response_post = requests.post(
            self.URI_ACCESS_TOKEN, headers=self.HEADERS, data=data_params
        )

        json_loads = response_post.json()
        line_id_token = json_loads["id_token"]
        line_profile = jwt.decode(
            line_id_token,
            LINE_CHANNEL_SECRET,
            audience=LINE_CHANNEL_ID,
            issuer='https://access.line.me',
            algorithms=['HS256'],
        )

        if request.session.pop('nonce') != line_profile.get('nonce'):
            return HttpResponseBadRequest()

        user = request.user
        user_line_profile = LineProfile.objects.get(user=user)
        user_line_profile.line_id = line_profile['sub']
        user_line_profile.line_icon_url = line_profile['picture']
        user_line_profile.line_name = line_profile['name']
        user_line_profile.save()

        return redirect('calliope_web:profile')


class SupportView(TemplateView):
    template_name = 'calliope_web/support.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['public_key'] = os.environ['PUBLIC_KEY_PAYJP']
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            # print(request.POST)
            amount = request.POST.get('amount')
            payjp_token = request.POST.get('payjp-token')
            # customer = payjp.Customer.
            charge = payjp.Charge.create(
                amount=amount,
                currency='jpy',
                # customer=customer.id,
                card=payjp_token,
                description='django test',
            )
            context['amount'] = amount
            return render(request, self.template_name, context)
        except (PayjpException, Exception):
            return redirect('calliope_web:support')


class BssCreateView(CreateView):
    model = Bss
    template_name = "calliope_web/bss_create.html"
    success_url = reverse_lazy('calliope_web:bss_list')
    form_class = BssForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.author = request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BssListView(ListView):
    model = Bss
    template_name = "calliope_web/bss_list.html"
    ordering = ['-updated_at']
    context_object_name = 'bss_list'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            queryset = self.model.objects.filter(
                Q(author__username__icontains=query) | Q(body__icontains=query)
            )
        else:
            queryset = self.model.objects.all()
        if self.ordering:
            queryset = queryset.order_by(*self.ordering)
        return queryset


class BssDetailView(DetailView):
    model = Bss
    template_name = "calliope_web/bss_detail.html"
    context_object_name = 'bss'


class BssUpdateView(UserPassesTestMixin, UpdateView):
    model = Bss
    template_name = "calliope_web/bss_update.html"
    fields = ['body']

    def get_success_url(self):
        return reverse('calliope_web:bss_list')

    def test_func(self):
        user = self.request.user
        return (
            user
            == self.model.objects.select_related('author')
            .get(pk=self.kwargs['pk'])
            .author
        )


class BssDeleteView(UserPassesTestMixin, DeleteView):
    model = Bss
    template_name = "calliope_web/bss_delete.html"
    success_url = reverse_lazy('calliope_web:bss_list')

    def get(self, request, *args, **kwargs):
        super().delete(request)
        return redirect('calliope_web:bss_list')

    def test_func(self):
        user = self.request.user
        return (
            user
            == self.model.objects.select_related('author')
            .get(pk=self.kwargs['pk'])
            .author
        )
