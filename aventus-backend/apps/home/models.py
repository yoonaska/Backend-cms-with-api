from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users
from random import randint
from django.utils.text import slugify

def default_image():
    return f"default/image/default-image.png"  


def our_projects_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-projects/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def our_clients_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-clients/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def our_servicer_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-service/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def default_blog_og_image():
    return f"default/blog/default_bog_og_image.png"

def seo_blog_image_media(self, filename):
    return 'assets/seo-blog-image/{}.png'.format(self.meta_image_title, uuid4())


def blog_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/blog-image/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def tech_stack_image_media(self, filename):
    return f"assets/tech-stack/{self.id}/{self.stack_title}.png"

class OurProjects(AbstractDateFieldMix):
    title           = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    order           = models.IntegerField(_("Display Order"),null=True,blank=True)
    project_image   = models.FileField(_("Project Image"),null=True,blank=True,upload_to=our_projects_image_media,default=default_image)
    web_link        = models.URLField(_("Web Url"),null=True,blank=True)
    is_active       = models.BooleanField(_('Status'),default=True)
    created_by      = models.ForeignKey(Users, related_name="OurProjects_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by      = models.ForeignKey(Users, related_name="OurProjects_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "OurProjects"
        verbose_name_plural   = "OurProjects"

def product_image_upload_image_dir(request):
    return 'assets/our_projects/images/{}/{}.png'.format(str(request.user.id).lower(), uuid4())


class OurProjectsImages(AbstractDateFieldMix):
    learn_campaign  = models.ForeignKey(OurProjects, related_name="Our_Client", on_delete=models.CASCADE, blank=True, null=True)
    uuid            = models.CharField(_('UUID'),  max_length=150, editable=False)
    image           = models.ImageField(_(' Image'), upload_to=product_image_upload_image_dir, default=default_image,blank=True, null=True)
    
    def __str__(self) :
        return self.uuid
    
    class Meta : 
        verbose_name          = "OurProjectsImages"
        verbose_name_plural   = "OurProjectsImages"

# OURS SERVICE 

class OurServices(AbstractDateFieldMix):
    slug                = models.SlugField(_('Slug'),  max_length=250, editable=False)
    title               = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    full_name           = models.CharField(_("Full Name"),max_length=250,null=True,blank=True,db_index=True)
    order               = models.IntegerField(_("Display Order"),null=True,blank=True)
    url                 = models.CharField(_("Url"),max_length=250,null=True,blank=True,db_index=True)
    button_titile       = models.CharField(_("Button Title"),max_length=250,null=True,blank=True,db_index=True)
    description_title   = models.CharField(_('Description Title'),max_length=250,null=True,blank=True,db_index=True)
    description         = models.TextField(_("Description"),null=True,blank=True)
    service_image       = models.FileField(_("Service Image"),null=True,blank=True,upload_to=our_servicer_image_media,default=default_image)
    
    is_active           = models.BooleanField(_('Status'),default=True)
    is_main             = models.BooleanField(_('Is Main'),default=False)

    is_popular          = models.BooleanField(_('Is Popular'),default=False)
    created_by          = models.ForeignKey(Users, related_name="OurServices_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by          = models.ForeignKey(Users, related_name="OurServices_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    #Seo
    og_image            = models.FileField(_("Og Image"),upload_to=seo_blog_image_media,default=default_blog_og_image,null=True,blank=True)
    meta_image_title    = models.CharField(_("Image Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_title          = models.CharField(_("Meta Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_description    = models.TextField(_("Description"),null=True,blank=True)
    meta_keyword        = models.TextField(_("Meta Keywords"),null=True,blank=True)
    #

    def save(self, *args, **kwargs):
        if not self.slug or self.url:
            self.slug = self.url.replace(' ', '-')
            if OurServices.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{self.url.replace(' ', '-')}-{randint(1, 9999999)}"
        super().save(*args, **kwargs) 
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "OurServices"
        verbose_name_plural   = "OurServices"


class OurServicesPoints(AbstractDateFieldMix):
    service       = models.ForeignKey(OurServices, verbose_name=_("Service"), on_delete=models.CASCADE,null=True,blank=True)
    title         = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    description   = models.TextField(_("Description"),null=True,blank=True)
    
    def __str__(self) :
        return self.service.slug
    
    class Meta : 
        verbose_name          = "OurServicesPoints"
        verbose_name_plural   = "OurServicesPoints" 

#####

class Department(AbstractDateFieldMix):
    title           = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    order           = models.IntegerField(_("Order"),null=True,blank=True)
    is_active       = models.BooleanField(_('Status'),default=True)
    created_by      = models.ForeignKey(Users, related_name="Department_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by      = models.ForeignKey(Users, related_name="Department_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "Department"
        verbose_name_plural   = "Department"
        
##

class OurClients(AbstractDateFieldMix):
    # title           = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    order           = models.IntegerField(_("Order"),null=True,blank=True)
    client_logo     = models.FileField(_("Project Image"),null=True,blank=True,upload_to=our_clients_image_media,default=default_image)
    # web_link        = models.URLField(_("Web Url"),null=True,blank=True)
    is_active       = models.BooleanField(_('Status'),default=True)
    created_by      = models.ForeignKey(Users, related_name="OurClients_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by      = models.ForeignKey(Users, related_name="OurClients_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) :
        return str(self.id)
    
    class Meta : 
        verbose_name          = "OurClients"
        verbose_name_plural   = "OurClients"
        
        
class ProjectDomain(AbstractDateFieldMix):
    slug            = models.SlugField(_('Slug'),  max_length=250, editable=False)
    title           = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    is_active       = models.BooleanField(_('Status'),default=True)
    created_by      = models.ForeignKey(Users, related_name="Domain_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by      = models.ForeignKey(Users, related_name="Domain_updated_by", on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if ProjectDomain.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(ProjectDomain, self).save(*args, **kwargs)

    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "ProjectDomain"
        verbose_name_plural   = "ProjectDomain"

def tech_stack_default_image():
    return f"default/image/face-logo.png"

class TechStack(AbstractDateFieldMix):
    stack_title   = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    stack_logo    = models.FileField(_("Image"), upload_to=tech_stack_image_media,null=True,blank=True)
    is_active     = models.BooleanField(_('Status'),default=True)
    created_by    = models.ForeignKey(Users, related_name="Tech_Stack_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by    = models.ForeignKey(Users, related_name="Tech_Stack_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) :
        return self.stack_title
    
    class Meta : 
        verbose_name          = "TechStack"
        verbose_name_plural   = "TechStack"
        
        
#___________________ COMPANY PROFILE PDF _______________________________ #

def CompanyProfilePdf_upload_dir(self,request):
    return 'assets/company-profile-pdf/files/{}/{}'.format(self.title, self.file)


class CompanyProfilePdf(AbstractDateFieldMix)   : 
    title       = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    file        = models.FileField(_("Company Profile Pdf"),upload_to=CompanyProfilePdf_upload_dir,null=True,blank=True)
    is_active   = models.BooleanField(_("Status"),default=True)
    
    class Meta:
        verbose_name = 'CompanyProfilePdf'
        verbose_name_plural = 'CompanyProfilePdf'
        
        
    def __str__(self):
        return "{}".format(self.title)
    
    