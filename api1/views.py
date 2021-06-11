from calliope_bot.models import LineProfile
from django.contrib.auth import authenticate, get_user_model
from django.db.models import query
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from calliope_web.models import Bss
from rest_framework import generics, mixins, viewsets, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import BssSerializer, CustomUserSerializer

class BssListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = BssSerializer
    queryset = Bss.objects.order_by('-updated_at')
    
    def post(self, request):
        post_bss = Bss.objects.create(author=request.user, body=request.POST['body'])
        post_bss_data = self.get_serializer(post_bss)
        return Response({'post': post_bss_data.data})

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

class PublishTokenAPIView(generics.GenericAPIView):
    http_method_names = ('post', )
    
    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        token, _ = Token.objects.get_or_create(user=user)
        update_flag = request.POST.get('update', False)
        if update_flag:
            token.delete()
            token.save()
        return Response({'token': str(token)})
