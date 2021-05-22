from django import forms
from django.contrib.auth import get_user_model
from django.db.models import fields
from .models import Bss
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        disabled=True,
        label='ユーザー名',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder':'foo@example.com'
        }),
        label='メールアドレス'
    )
    title = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder':'title'
        }),
        label='件名',
    )
    body = forms.CharField(
        max_length=400,
        widget=forms.Textarea(attrs={
            'placeholder':'content'
        }),
        label='内容',
    )

    
class BssForm(forms.ModelForm):
    
    class Meta:
        model = Bss
        fields = ("body",)
    

class UserCreateForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean(self):
        email = self.cleaned_data['email']
        get_user_model().objects.filter(email=email, is_active=False).delete()
        return super().clean()







