from django.urls import path
from . import views

app_name = 'calliope_auth'
urlpatterns = [
    path('login/', views.LoginWebView.as_view(), name='login'),
    path('login/testuser/', views.LoginTestuser.as_view(), name='login_testuser'),
    path('logout/', views.LogoutWebView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/<token>/', views.SignUpDoneView.as_view(), name='signup_done'),
    path('auth-docs/', views.AuthDocsView.as_view(), name='auth_docs'),
]