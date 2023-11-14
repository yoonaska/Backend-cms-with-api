from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.home.models import OurServices, ProjectDomain, TechStack
from apps.users.models import Users
from random import randint
from django.utils.text import slugify


def default_image():
    return f"default/image/default-image.png"  


def case_study_projects_image_media(instance, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/case-study-project/'
    if extension == 'png' or extension == 'gif':
        return '{}{}.{}'.format(upload_path, uuid4(), extension)
    return '{}default.png'.format(upload_path)


def project_banner_image_media(instance, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/project-banner/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def service_banner_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/service-banner/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def project_logo_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/project-logo/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def about_image_upload_image_dir(request):
    return 'assets/home-about-us/{}.png'.format(str(request.user.id).lower(), uuid4())


# SEO
def default_project_og_image():
    return f"default/blog/default_bog_og_image.png"  

def seo_project_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/home-about-us/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)


class ProjectCaseStudy(AbstractDateFieldMix):
    slug                                  = models.SlugField(_('Slug'),  max_length=250, editable=False)
    project_tags                          = models.TextField(_("Project Tags"),null=True,blank=True)
    project_name                          = models.CharField(_("Project Name"),max_length=250,null=True,blank=True,db_index=True)
    url                                   = models.CharField(_("Url"),max_length=250,null=True,blank=True,db_index=True)
    project_image                         = models.FileField(_("Project Image"),null=True,blank=True,upload_to=case_study_projects_image_media,default=default_image)
    domain                                = models.ForeignKey(ProjectDomain,related_name='Domain',on_delete=models.CASCADE,null=True,blank=True)
    service                               = models.ForeignKey(OurServices,related_name='Service',on_delete=models.CASCADE,null=True,blank=True)
    # MILESTONE
    research                              = models.CharField(_("Research"),max_length=250,null=True,blank=True,db_index=True)
    design_strategy                       = models.CharField(_("Design Strategy"),max_length=250,null=True,blank=True,db_index=True)
    ui                                    = models.CharField(_("User Interface"),max_length=250,null=True,blank=True,db_index=True)
    backend_development                   = models.CharField(_("Backend Development"),max_length=250,null=True,blank=True,db_index=True)
    frontend_development                  = models.CharField(_("Frontend Development"),max_length=250,null=True,blank=True,db_index=True)
    testing                               = models.CharField(_("Testing"),max_length=250,null=True,blank=True,db_index=True)
    #
    backend_technology                    = models.CharField(_("Backend Technology"),max_length=250,null=True,blank=True,db_index=True)
    other_technology                      = models.CharField(_("Other Technology"),max_length=250,null=True,blank=True,db_index=True)
    front_technology                      = models.CharField(_("Front Technology"),max_length=250,null=True,blank=True,db_index=True)
    web_url_title                         = models.CharField(_("Url Title"),max_length=250,null=True,blank=True)
    eliminating_challenges_description    = models.TextField(_("Eliminating Challenges Description"),null=True,blank=True)
    project_mode_of_functions             = models.TextField(_("Project Mode Of Functions"),null=True,blank=True)
    # BANNER SECTION
    project_image_banner                  = models.FileField(_("Project banner Image"),null=True,blank=True,upload_to=project_banner_image_media,default=default_image)
    project_logo                          = models.FileField(_("Project logo"),null=True,blank=True,upload_to=project_logo_image_media,default=default_image)
    banner_title                          = models.CharField(_("Banner Title"),max_length=250,null=True,blank=True,db_index=True)
    banner_description                    = models.TextField(_("Banner_Description"),null=True,blank=True)
    # SEO 
    og_image                              = models.FileField(_("Og Image"),upload_to=seo_project_image_media,default=default_project_og_image)
    meta_image_title                      = models.CharField(_("Image Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_title                            = models.CharField(_("Meta Title"),max_length=250,null=True,blank=True,db_index=True)
    meta_description                      = models.TextField(_("Description"),null=True,blank=True)
    meta_keyword                          = models.TextField(_("Meta Keywords"),null=True,blank=True)
    #
    is_active                             = models.BooleanField(_('Status'),default=True)
    created_by                            = models.ForeignKey(Users, related_name="ProjectCaseStudy_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by                            = models.ForeignKey(Users, related_name="ProjectCaseStudy_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    is_project_casestudy                  = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug or self.url:
            # Replace spaces with hyphens in the slug
            self.slug = self.url.replace(' ', '-')
            if OurServices.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{self.url.replace(' ', '-')}-{randint(1, 9999999)}"
        super().save(*args, **kwargs)  
    
    def __str__(self) :
        return self.project_name
    
    class Meta : 
        verbose_name          = "ProjectCaseStudy"
        verbose_name_plural   = "ProjectCaseStudy"


#----------------------------- HOME ABOUT US IMAGE SECTIONS--------------------------------#

    
class ProjectCaseStudyImages(AbstractDateFieldMix):
    project_case_study    = models.ForeignKey(ProjectCaseStudy, related_name="learn_campaign", on_delete=models.CASCADE, blank=True, null=True)
    uuid                  = models.CharField(_('UUID'),  max_length=150, editable=False)
    image                 = models.ImageField(_('Project Screen Image'), upload_to=about_image_upload_image_dir,default=default_image,blank=True, null=True)

    class Meta:
        verbose_name = 'ProjectCaseStudyImages'
        verbose_name_plural = 'ProjectCaseStudyImages'
        
    def __str__(self):
        return "{}".format(self.project_case_study.project_name)
    

#--------------------------------PROJECT AIM MANAGEMENT -------------------------------------#

class ProjectAminPoints(AbstractDateFieldMix):
    project   = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project"), on_delete=models.CASCADE,null=True,blank=True)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True,db_index=True)
    
    def __str__(self) :
        return self.project.project_name
    
    class Meta : 
        verbose_name          = "ProjectAminPoints"
        verbose_name_plural   = "ProjectAminPoints" 
        
#--------------------------------PROJECT LIVE URLS MANAGEMENT -------------------------------------#

class ProjectLiveUrls(AbstractDateFieldMix):
    project   = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project"), on_delete=models.CASCADE,null=True,blank=True)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True,db_index=True)
    
    def __str__(self) :
        return self.project.project_name
    
    class Meta : 
        verbose_name          = "ProjectLiveUrls"
        verbose_name_plural   = "ProjectLiveUrls" 
        
        
#--------------------------------PROBLEM STATEMENT MANAGEMENT -------------------------------------#
class ProblemStatement(AbstractDateFieldMix):
    project   = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project"), on_delete=models.CASCADE,null=True,blank=True)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True,db_index=True)
    
    def __str__(self) :
        return self.project.project_name
    
    class Meta : 
        verbose_name          = "ProblemStatement"
        verbose_name_plural   = "ProblemStatement" 
        
#--------------------------------Eliminating Challenges-------------------------------------#

class EliminatingChallengesPoints(AbstractDateFieldMix):
    project   = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project"), on_delete=models.CASCADE,null=True,blank=True)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True,db_index=True)
    
    def __str__(self) :
        return self.project.project_name
    
    class Meta : 
        verbose_name          = "EliminatingChallengesPoints"
        verbose_name_plural   = "EliminatingChallengesPoints"

#------------------------------- THE OUTCOMES--------------------------------------------------------------------------#
class ProjectCaseStudyOutcomes(AbstractDateFieldMix):
    project   = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project_CaseStudy_Outcomes"), on_delete=models.CASCADE,null=True,blank=True)
    title     = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    url       = models.TextField(_("Url"),null=True,blank=True)
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "ProjectCaseStudyOutcomes"
        verbose_name_plural   = "ProjectCaseStudyOutcomes" 
        
        
#------------------------------PROJECT CASE STUDY BANNER ------------------------------------------------------------#


class ProjectCaseStudyBannerImage(AbstractDateFieldMix):
    project           = models.ForeignKey(ProjectCaseStudy, verbose_name=_("Project"), on_delete=models.CASCADE, null=True, blank=True)
    # banner_image = models.FileField(_("Banner Image"), null=True, blank=True, upload_to=service_banner_image_media, default=default_image)
    title             = models.CharField(_("Title"), max_length=250, null=True, blank=True,db_index=True)
    domain_title      = models.CharField(_("Domain Title"), max_length=250, null=True, blank=True,db_index=True)
    url               = models.CharField(_("Url"), max_length=250, null=True, blank=True,db_index=True)
    description       = models.TextField(_("Description"), null=True, blank=True)
    tech_stack_one    = models.ForeignKey(TechStack, verbose_name=_("Tech Stack One"), on_delete=models.CASCADE, null=True, blank=True, related_name="tech_stack_one_images")
    tech_stack_two    = models.ForeignKey(TechStack, verbose_name=_("Tech Stack Two"), on_delete=models.CASCADE, null=True, blank=True, related_name="tech_stack_two_images")
    is_active         = models.BooleanField(_('Status'), default=True)
    created_by        = models.ForeignKey(Users, related_name="projectcasestudybannerimage_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by        = models.ForeignKey(Users, related_name="projectcasestudybannerimage_updated_by", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'ProjectCaseStudyBannerImage'
        verbose_name_plural = 'ProjectCaseStudyBannerImages'

    def __str__(self):
        return "{}".format(self.title)

    
    
class ProjectCaseStudyBannerMultipleImages(AbstractDateFieldMix):
    project_case_study    = models.ForeignKey(ProjectCaseStudyBannerImage, related_name="Project", on_delete=models.CASCADE, blank=True, null=True)
    uuid                  = models.CharField(_('UUID'),  max_length=150, editable=False)
    image                 = models.ImageField(_('Project Screen Image'), upload_to=about_image_upload_image_dir,default=default_image,blank=True, null=True)

    class Meta:
        verbose_name = 'ProjectCaseStudyBannerMultipleImages'
        verbose_name_plural = 'ProjectCaseStudyBannerMultipleImages'
        
    def __str__(self):
        return "{}".format(self.uuid)