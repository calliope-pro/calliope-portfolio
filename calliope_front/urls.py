from django.urls import path, include

from . import views
app_name = 'calliope_front'
urlpatterns = [
    path('work1/', views.FrontWorkOneView.as_view(), name='work1'),
    
]
