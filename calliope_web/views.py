import os
from django.urls.base import reverse_lazy

import payjp
from calliope_bot.models import LineProfile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView, CreateView, ListView
from payjp.error import PayjpException

from .forms import ContactForm, BssForm
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
        if request.POST.get('username') in settings.ALLOWED_LOGIN_USERS:
            return super().post(request, *args, **kwargs)
        else:
            return self.form_invalid(self.form_class)


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

    
    

