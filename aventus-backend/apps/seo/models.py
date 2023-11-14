from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users


def default_blog_og_image():
    return f"default/blog/default_bog_og_image.png"

def seo_blog_image_media(self, filename):
    return 'assets/seo-blog-image/{}.png'.format(self.meta_image_title, uuid4())



#__________________ SEO MANAGEMENT SECTION MODELS______________________#



class SeoManagement(AbstractDateFieldMix):
    
    SEO_DISPLAY_PAGE = (
        ('Home', 'Home'),
        ('Blog', 'Blog'),
        ('Services', 'Services'),
        ('Contact_Us', 'Contact Us'),
        ('Career', 'Career'),
        ('About_Us', 'About Us'),
        ('', 'Not Selected'),
    )

    
    seo_page            = models.CharField(_("Seo Display Page"),choices=SEO_DISPLAY_PAGE,max_length=250,null=True,blank=True,db_index=True)
    og_image            = models.FileField(_("Og Image"),upload_to=seo_blog_image_media,default=default_blog_og_image,null=True,blank=True)
    meta_image_title    = models.CharField(_("Image Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_title          = models.CharField(_("Meta Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_description    = models.TextField(_("Description"),null=True,blank=True)
    meta_keyword        = models.TextField(_("Meta Keywords"),null=True,blank=True)
    #
    is_active           = models.BooleanField(default=True)
    created_by          = models.ForeignKey(Users, related_name="Seo_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by          = models.ForeignKey(Users, related_name="Seo_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self) :
        return self.meta_image_title
    
    class Meta : 
        verbose_name          = "SeoManagement"
        verbose_name_plural   = "SeoManagement"
