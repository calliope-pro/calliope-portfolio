from django.urls import path

from . import views
app_name = 'calliope_front'
urlpatterns = [
    path('work1/', views.FrontWorkOneView.as_view(), name='work1'),
    path('work2/', views.FrontWorkTwoView.as_view(), name='work2'),
]
