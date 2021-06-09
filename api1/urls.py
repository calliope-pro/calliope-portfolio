from django.urls.conf import include, path
from rest_framework import routers
from .views import BssViewSet

app_name = 'api1'
router = routers.DefaultRouter()
router.register(r'bss', BssViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
