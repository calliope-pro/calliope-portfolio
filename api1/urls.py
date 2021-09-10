from django.urls.conf import path
from . import views

app_name = 'api1'
urlpatterns = [
    path('bss', views.BssListAPIView.as_view()),
    path('users', views.CustomUserListAPIView.as_view()),
    path('users/<str:username>', views.CustomUserAPIView.as_view()),
    path('check', views.CheckAPIView.as_view()),
    path('token', views.PublishTokenAPIView.as_view()),
]
