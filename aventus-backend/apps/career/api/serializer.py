from rest_framework import serializers
from apps.career.api.job_application_mail import job_application_submits_mail_send
from apps.career.models import JobApplication, JobVacancy



class JobApplicationFormSubmissionRequestSerializer(serializers.ModelSerializer):
    job_instance    = serializers.PrimaryKeyRelatedField(queryset=JobVacancy.objects.all(),required=False)
    designation     = serializers.CharField(required=False)
    name            = serializers.CharField(required=False)
    email           = serializers.EmailField(required=True)
    phone_number    = serializers.CharField(required=True)
    portfolio       = serializers.CharField(required=False)
    cv              = serializers.URLField(required=False)
    portfolio_pdf   = serializers.FileField(required=False)
    cv_pdf          = serializers.FileField(required=False)
    ratting         = serializers.CharField(required=False)
    about_yourself  = serializers.CharField(required=False)
    
    
    class Meta:
        model=JobApplication
        fields = ['job_instance','designation','name','email','phone_number','ratting','portfolio','cv','portfolio_pdf','cv_pdf','about_yourself']
        
    
    def create(self, validated_data):
        request                 = self.context.get('request')
        instance                = JobApplication()
        instance.job            = validated_data.get("job_instance",None)
        instance.designation    = validated_data.get("designation",None)
        instance.name           = validated_data.get("name",None)
        instance.email          = validated_data.get("email",None)
        instance.phone_number   = validated_data.get("phone_number",None)
        instance.ratting        = validated_data.get("ratting",None)
        instance.portfolio      = validated_data.get("portfolio",None)
        instance.cv             = validated_data.get("cv",None)
        instance.portfolio_pdf  = validated_data.get("portfolio_pdf",None)
        instance.cv_pdf         = validated_data.get("cv_pdf",None)
        instance.about_yourself = validated_data.get("about_yourself",None)
        instance.save()
        job_application_submits_mail_send(request,instance)
        return instance
