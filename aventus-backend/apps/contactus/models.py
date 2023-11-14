from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix

# Create your models here.

class ContactUs(AbstractDateFieldMix):
    service               = models.CharField(_("Service"),max_length=250,null=True,blank=True)
    name                  = models.CharField(_("Name"),max_length=250,null=True,blank=True)
    email                 = models.CharField(_("Email"),max_length=250,null=True,blank=True)
    company_name          = models.CharField(_("Company Name"),max_length=250,null=True,blank=True)
    phone_number          = models.CharField(_("Phone Number"),max_length=250,null=True,blank=True)
    how_did_you_find_us   = models.CharField(_("How Did You Find Us"),max_length=250,null=True,blank=True)
    other_message         = models.CharField(_("Other Message"),max_length=250,null=True,blank=True)
    message               = models.CharField(_("Message"),max_length=250,null=True,blank=True)
    department            = models.CharField(_("Departments"),max_length=250,null=True,blank=True)
    enquires_from         = models.CharField(_("Enquires From"),max_length=250,null=True,blank=True)

    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"
        
    def __str__(self):
        return "{}".format(self.email)
    
