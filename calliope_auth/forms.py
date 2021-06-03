import re
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if username[:4] != 'user':
            raise ValidationError('userから始まる20文字以下の名前にしてください。')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data['password1']
        if re.search(r'\s\S', password):
            raise ValidationError('パスワードに空白を含めないでください')
        return password
      
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        
        get_user_model().objects.filter(Q(email=email)|Q(username=username), is_active=False).delete()
        return super().clean()
        