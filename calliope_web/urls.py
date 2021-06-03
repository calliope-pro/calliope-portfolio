from django.urls import path
from . import views

app_name = 'calliope_web'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/callback/', views.LineLinkView.as_view(), name='linelink'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('bss/', views.BssListView.as_view(), name='bss_list'),
    path('bss/new/', views.BssCreateView.as_view(), name='bss_create'),
    path('bss/<int:pk>/', views.BssDetailView.as_view(), name='bss_detail'),
    path('bss/<int:pk>/update/', views.BssUpdateView.as_view(), name='bss_update'),
    path('bss/<int:pk>/delete/', views.BssDeleteView.as_view(), name='bss_delete'),
    path('support/', views.SupportView.as_view(), name='support'),
]