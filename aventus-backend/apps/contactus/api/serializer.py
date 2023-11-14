from rest_framework import serializers
from apps.contactus.contact_us_mail import  Success_mail_for_Customer, consultation_enquiry_form_submits_mail_send, contact_us_fom_submits_mail_send
from apps.contactus.models import ContactUs
from apps.home.models import Department,OurServices


class ContactUsFormSubmissionRequestSerializer(serializers.ModelSerializer):
    service               = serializers.ListField(child=serializers.CharField(),required=True)
    name                  = serializers.CharField(required=False)
    email                 = serializers.EmailField(required=True)
    company_name          = serializers.CharField(required=False)
    phone_number          = serializers.CharField(required=False)
    how_did_you_find_us   = serializers.CharField(required=False)
    other_message         = serializers.CharField(required=False)
    message               = serializers.CharField(required=False)
    
    
    class Meta:
        model=ContactUs
        fields = ['service','name','email','phone_number','company_name','how_did_you_find_us','other_message','message',]
        
    def create(self, validated_data):
        request                 = self.context.get('request')
        instance                        = ContactUs()
        instance.service                = validated_data.get('service',None)
        instance.name                   = validated_data.get('name',None)
        instance.email                  = validated_data.get('email',None)
        instance.company_name           = validated_data.get('company_name',None)
        instance.phone_number           = validated_data.get('phone_number',None)
        instance.how_did_you_find_us    = validated_data.get('how_did_you_find_us',None)
        instance.other_message          = validated_data.get('other_message',None)
        instance.message                = validated_data.get('message',None)
        instance.enquires_from          = 'Contact Us Page'
        instance.save()
        contact_us_fom_submits_mail_send(request,instance)
        Success_mail_for_Customer(request,instance)
        return instance
    
    
class ConsultationEnquiryFormSubmissionRequestSerializer(serializers.ModelSerializer):
    department    = serializers.CharField(required=True)
    email         = serializers.EmailField(required=True)
    
    class Meta:
        model=ContactUs
        fields = ['email','department']
        
    def create(self, validated_data):
        request                   = self.context.get('request')
        instance                  = ContactUs()
        instance.department       = validated_data.get('department',None)
        instance.email            = validated_data.get('email',None)
        instance.enquires_from    = 'Home Page'
        instance.save()
        consultation_enquiry_form_submits_mail_send(request,instance)
        Success_mail_for_Customer(request,instance)
        return instance