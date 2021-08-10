from django.shortcuts import render
from django.views.generic import (
    TemplateView,
)

class FrontWorkOneView(TemplateView):
    template_name = "calliope_front/work1.html"

# Create your views here.
