import re

from calliope_bot.models import LineProfile
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import View

from .forms import UserCreateForm


# Create your views here.
class LoginWebView(LoginView):
    template_name = 'calliope_auth/login.html'
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
            form.add_error('username', 'usernameはuser~~のみ有効です')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutWebView(LogoutView):
    pass


class SignUpView(CreateView):
    template_name = 'calliope_auth/signup.html'
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
        body = render_to_string('calliope_auth/email_body.txt', context)
        user.email_user(sub, body)
        context = {'form': self.get_form_class(), 'done': True}
        return render(self.request, 'calliope_auth/signup.html', context)


class LoginTestuser(View):
    def get(self, request, *args, **kwargs):
        if settings.DEBUG:
            user, _ = get_user_model().objects.get_or_create(
                username='testuser',
                email='shgdxhsnszdbgsgmszvxbdmzsawa@azhjsgbmwanvGzjgkxjd.akwgeyrfjzvcxmdbks',
            )
        else:
            user = get_user_model().objects.get(username='testuser')
        LineProfile.objects.select_related('user').get_or_create(user=user)
        login(request, user)
        return redirect('calliope_web:home')


class SignUpDoneView(TemplateView):
    template_name = "calliope_auth/signup_done.html"

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=60 * SignUpView.timeout_minutes)
        except (SignatureExpired, BadSignature):
            return HttpResponseBadRequest()

        try:
            user = get_user_model().objects.get(pk=user_pk)
        except get_user_model().DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user.is_active = True
            user.save()
            LineProfile.objects.select_related('user').create(user=user)
            return render(request, self.template_name, {'user': user})


class AuthDocsView(TemplateView):
    template_name = 'calliope_auth/auth_docs.html'
