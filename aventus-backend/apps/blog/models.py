from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users
from random import randint
from django.utils.text import slugify


def blog_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/blog-image/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def default_blog_image():
    return f"default/blog/blog_default.jpg"

def default_blog_og_image():
    return f"default/blog/default_bog_og_image.png"

def seo_blog_image_media(self, filename):
    return 'assets/seo-blog-image/{}.png'.format(self.meta_image_title, uuid4())



#__________________ BLOG MANAGEMENT SECTION MODELS______________________#

class Blog(AbstractDateFieldMix):
    slug                = models.SlugField(_('Slug'),  max_length=250, editable=False,db_index=True)
    blog_image          = models.FileField(_("Blog Image"),upload_to=blog_image_media,default=default_blog_image,null=True,blank=True)
    title               = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    date                = models.DateTimeField(_("Date"),null=True,blank=True)
    description         = models.TextField(_("Description"),null=True,blank=True)
    tags                = models.TextField(_("Tags"),null=True,blank=True,db_index=True)
    #Seo
    og_image            = models.FileField(_("Og Image"),upload_to=seo_blog_image_media,default=default_blog_og_image,null=True,blank=True)
    meta_image_title    = models.CharField(_("Image Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_title          = models.CharField(_("Meta Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_description    = models.TextField(_("Description"),null=True,blank=True)
    meta_keyword        = models.TextField(_("Meta Keywords"),null=True,blank=True,db_index=True)
    #
    is_active           = models.BooleanField(default=True)
    is_popular          = models.BooleanField(default=False)
    created_by          = models.ForeignKey(Users, related_name="Blog_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by          = models.ForeignKey(Users, related_name="Blog_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    is_blog             = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Blog, self).save(*args, **kwargs)


    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "Blog"
        verbose_name_plural   = "Blog"
    
