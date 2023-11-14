from django.db import models
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel
from django.utils.translation import gettext_lazy as _


class AbstractDateFieldMix(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False,null=True,blank=True)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False,null=True,blank=True)
    
    class Meta:
        abstract = True
