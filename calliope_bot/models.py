from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class LineProfile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    line_id = models.SlugField(_("line_id"), unique=True, blank=True, null=True)
    line_icon_url = models.URLField(_("line_icon_url"), max_length=200, blank=True, null=True)
    line_name = models.CharField(_("line_name"), max_length=20, blank=True, null=True)

    def __str__(self):
        tmp_name = self.line_name
        if tmp_name:
            return tmp_name
        else:
            return 'None'
