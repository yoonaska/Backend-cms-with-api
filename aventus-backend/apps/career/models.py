from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users
from random import randint
from django.utils.text import slugify

class JobVacancy(AbstractDateFieldMix):
    slug          = models.SlugField(_('Slug'),  max_length=250, editable=False)
    designation   = models.CharField(_("Designation"),max_length=250,null=True,blank=True, db_index=True)
    tags          = models.TextField(_("Tags"),null=True,blank=True,db_index=True)
    min_exp       = models.IntegerField(_("Min Expe"),null=True,blank=True,default=0)
    max_exp       = models.IntegerField(_("Max Expe"),null=True,blank=True,default=0)
    description   = models.TextField(_("Description"),null=True,blank=True)
    is_active     = models.BooleanField(_('Status'),default=True)
    created_by    = models.ForeignKey(Users, related_name="JobVacancy_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by    = models.ForeignKey(Users, related_name="JobVacancy_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    is_job        = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.slug or self.designation:
            self.slug = slugify(str(self.designation))
            if JobVacancy.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.designation)) + '-' + str(randint(1, 9999999))
        super(JobVacancy, self).save(*args, **kwargs)
    def __str__(self) :
        return self.designation
    
    class Meta : 
        verbose_name          = "JobVacancy"
        verbose_name_plural   = "JobVacancy"
        
        
class Responsibilities(AbstractDateFieldMix):
    job       = models.ForeignKey(JobVacancy, verbose_name=_("Job Vacancy"), on_delete=models.CASCADE)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True)
    
    def __str__(self) :
        return self.job.designation
    
    class Meta : 
        verbose_name          = "Responsibilities"
        verbose_name_plural   = "Responsibilities"
        

class Skills(AbstractDateFieldMix):
    job       = models.ForeignKey(JobVacancy, verbose_name=_("Job Vacancy"), on_delete=models.CASCADE)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True)
    
    def __str__(self) :
        return self.job.designation
    
    class Meta : 
        verbose_name          = "Skills"
        verbose_name_plural   = "Skills"
        

#_________________________WHY AVENTUS________________________#

class WhyAventus(AbstractDateFieldMix):
    title       = models.CharField(_("Title"),max_length=250,null=True,blank=True,db_index=True)
    is_active   = models.BooleanField(_('Status'),default=True)
    created_by  = models.ForeignKey(Users, related_name="WhyAventus_created_by", on_delete=models.CASCADE, null=True, blank=True)
    updated_by  = models.ForeignKey(Users, related_name="WhyAventus_updated_by", on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self) :
        return self.title
    
    class Meta : 
        verbose_name          = "WhyAventus"
        verbose_name_plural   = "WhyAventus"
        
        
class WhyAventusPoints(AbstractDateFieldMix):
    why_aventus       = models.ForeignKey(WhyAventus, verbose_name=_("Why Aventus"), on_delete=models.CASCADE)
    Points    = models.CharField(_("Points"),max_length=250,null=True,blank=True,db_index=True)
    
    def __str__(self) :
        return self.why_aventus.title
    
    class Meta : 
        verbose_name          = "WhyAventusPoints"
        verbose_name_plural   = "WhyAventusPoints"
        
        
"""-------------------------JOB APPLICATION SUBMISSION---------------------"""

def resume_media(instance, filename):
    return f"assets/resume/{instance.email}-{uuid4()}.pdf"

def portfolio_media(instance, filename):
    return f"assets/portfolio/{instance.email}-{uuid4()}.pdf"



class JobApplication(AbstractDateFieldMix):
    job             = models.ForeignKey(JobVacancy, verbose_name=_("Job"),on_delete=models.CASCADE,null=True,blank=True)
    designation     = models.CharField(_('Name'),max_length=250,null=True,blank=True,db_index=True)
    name            = models.CharField(_('Name'),max_length=250,null=True,blank=True,db_index=True)
    email           = models.EmailField(_("Email"),null=True,blank=True)
    phone_number    = models.CharField(_('Phone Number'),max_length=100,null=True,blank=True,db_index=True)
    portfolio       = models.URLField(_("Portfolio Url"), null=True,blank=True)
    cv              = models.URLField(_("Cv Url"), null=True,blank=True)
    portfolio_pdf   = models.FileField(_("Portfolio Pdf"), null=True,blank=True,upload_to=portfolio_media)
    cv_pdf          = models.FileField(_("Cv Pdf"), null=True,blank=True,upload_to=resume_media)
    ratting         = models.CharField(_("Rating"),max_length=50,null=True,blank=True,db_index=True)
    about_yourself  = models.TextField(_("About Your Self"),max_length=350,null=True,blank=True)
    
    def __str__(self) :
        return self.name
    
    class Meta : 
        verbose_name          = "JobApplication"
        verbose_name_plural   = "JobApplication"