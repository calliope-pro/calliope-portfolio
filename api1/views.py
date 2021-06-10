from rest_framework import viewsets, mixins, generics
from .serializers import BssSerializer
from calliope_web.models import Bss

class BssViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Bss.objects.order_by('-updated_at').all()
    serializer_class = BssSerializer
# class BssViewSet(generics.ListAPIView):
#     queryset = Bss.objects.order_by('-updated_at').all()
#     serializer_class = BssSerializer
