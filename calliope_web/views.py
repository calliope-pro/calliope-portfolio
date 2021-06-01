import os
import re
from django.http import request
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import RedirectView, View

import payjp
from calliope_bot.models import LineProfile
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView)
from payjp.error import PayjpException
from django.template.loader import render_to_string

from .forms import BssForm, ContactForm, UserCreateForm
from .models import Bss


# Create your views here.
class HomeView(TemplateView):
    template_name = "calliope_web/home.html"


class LoginWebView(LoginView):
    template_name = 'calliope_web/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('calliope_web:home')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        request_username = request.POST.get('username')
        for allowed_login_user in settings.ALLOWED_LOGIN_USERS:
            if re.fullmatch(allowed_login_user, request_username):
                break
        else:
            form.add_error('username', 'usernameはuser〇〇のみ有効です')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutWebView(LogoutView):
    pass


class ContactView(FormView):
    template_name = 'calliope_web/contact.html'
    form_class = ContactForm
    
    def get_success_url(self):
        return reverse('calliope_web:contact')
    
    def get_initial(self):
        return {'username':self.request.user.username}
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            title = f"{form.cleaned_data['title']}-by-{self.request.user.username}"
            body = f"{form.cleaned_data['body']}"
            recipient_list = [form.cleaned_data['email'], settings.EMAIL_HOST_USER]
            send_mail(subject=title, message=body, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

class ProfileView(TemplateView):
    template_name = 'calliope_web/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lineprofile, _ = LineProfile.objects.get_or_create(user=self.request.user)
        if lineprofile.line_id:
            context['line_id'] = lineprofile.line_id
        else:
            context['line_id'] = None
        return context


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
    context_object_name = 'form'
    success_url = reverse_lazy('calliope_web:bss')
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
    ordering = ['-created_datetime']
    context_object_name = 'bss_list'


class SignUpView(CreateView):
    template_name = 'calliope_web/signup.html'
    form_class = UserCreateForm
    timeout_minutes = 30
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        current_url = self.request.build_absolute_uri()
        token = dumps(user.pk)
        sub = f'{user.username}さん、仮登録が完了しました。'
        context = {
            'token': token,
            'current_url': current_url,
            'username': user.username,
            'password': len(form.cleaned_data['password2']) * '*',
            'timeout_minutes': self.timeout_minutes,
        }
        if settings.DEBUG:
            context['password'] = form.cleaned_data['password2']
        body = render_to_string('calliope_web/email_body.txt', context)
        user.email_user(sub, body)
        context = {
            'form':self.get_form_class(),
            'done':True
        }
        return render(self.request, 'calliope_web/signup.html', context)


class LoginTestuser(View):    
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(username='testuser')
        login(request, user)
        return redirect('calliope_web:home')

class SignUpDoneView(TemplateView):
    template_name = "calliope_web/signup_done.html"
    
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=60*SignUpView.timeout_minutes)
        except (SignatureExpired, BadSignature):
            return HttpResponseBadRequest()
        
        try:
            user = get_user_model().objects.get(pk=user_pk)
        except get_user_model().DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user.is_active = True
            user.save()
            return render(request, self.template_name, {'user':user})


    

