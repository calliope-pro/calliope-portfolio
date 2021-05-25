from django.urls import path
from . import views

app_name = 'calliope_web'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginWebView.as_view(), name='login'),
    path('logout/', views.LogoutWebView.as_view(), name='logout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('bss/', views.BssListView.as_view(), name='bss'),
    path('bss/new/', views.BssCreateView.as_view(), name='bss_create'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/<token>/', views.SignUpDoneView.as_view(), name='signup_done')
]