from django import forms
from .models import Bss


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








