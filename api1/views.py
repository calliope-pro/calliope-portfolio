from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.http.response import Http404
from calliope_web.models import Bss
from rest_framework import generics, mixins, viewsets

from .serializers import BssSerializer, CustomUserSerializer

class BssAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Bss.objects.order_by('-updated_at').all()
    serializer_class = BssSerializer

class CustomUserAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    # queryset = get_user_model().objects.all()

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        username = self.request.GET.get('username')
        print(self.kwargs)
        if username is not None:
            queryset = get_user_model().objects.filter(username=username)
        return queryset
