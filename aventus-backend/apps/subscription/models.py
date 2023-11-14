from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix

# Create your models here.

class EmailSubscription(AbstractDateFieldMix):
    email       = models.EmailField(_('Email'),null=True,blank=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name = "EmailSubscription"
        verbose_name_plural = "EmailSubscriptions"
        
    def __str__(self):
        return "{}".format(self.email)