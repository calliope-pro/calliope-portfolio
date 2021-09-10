from calliope_bot.models import LineProfile
from calliope_web.models import Bss
from django.contrib.auth import authenticate, get_user_model
from django.http.request import HttpRequest, QueryDict
from django.http.response import JsonResponse
from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .serializers import BssSerializer, CustomUserSerializer


class BssListAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = BssSerializer
    queryset = Bss.objects.order_by('-updated_at')
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request:HttpRequest, *args, **kwargs):
        serializer = BssSerializer(data=request.data)
        serializer.is_valid()
        Bss.objects.create(author=request.user, body=serializer.data['body'])
        return JsonResponse(serializer.data, status=201)

class CustomUserListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

class CustomUserAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        queryset = get_user_model().objects.filter(username=self.kwargs['username'])
        return queryset

class CheckAPIView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', )

    def get(self, request):
        user = request.user

        content = {
            'username': str(user),
            'status': 'ok',
        }
        return Response(content)

class PublishTokenAPIView(ObtainAuthToken):
    http_method_names = ('post', )
