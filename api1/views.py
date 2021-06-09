from rest_framework import viewsets
from .serializers import BssSerializer
from calliope_web.models import Bss

class BssViewSet(viewsets.ModelViewSet):
    queryset = Bss.objects.all()
    serializer_class = BssSerializer