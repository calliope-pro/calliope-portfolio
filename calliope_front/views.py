from django.views.generic import TemplateView


class FrontWorkOneView(TemplateView):
    template_name = "calliope_front/work1.html"

class FrontWorkTwoView(TemplateView):
    template_name = 'calliope_front/index.html'
