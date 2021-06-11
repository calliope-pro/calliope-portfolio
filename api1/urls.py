from django.urls.conf import include, path
from rest_framework import routers
from . import views

app_name = 'api1'
router = routers.DefaultRouter()
router.register(r'bss', views.BssAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('users', views.CustomUserAPIView.as_view())
]
