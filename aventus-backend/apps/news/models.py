from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users



def default_image():
    return f"default/image/default-image.png"  

def news_image_media(self, filename):
    return 'assets/news/{}.png'.format(self.title, uuid4())


class News(AbstractDateFieldMix):
    title         = models.TextField(_("Title"),null=True,blank=True,db_index=True)
    news_image    = models.FileField(_("News Image"),null=True,blank=True,upload_to=news_image_media,default=default_image)
    url_link      = models.URLField(_("Link"),null=True,blank=True)
    is_active     = models.BooleanField(_('Status'),default=True)
    created_by    = models.ForeignKey(Users, related_name="News_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by    = models.ForeignKey(Users, related_name="News_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "News"
        verbose_name_plural   = "News"