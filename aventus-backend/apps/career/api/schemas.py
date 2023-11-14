from rest_framework import serializers
from apps.career.models import JobVacancy, Responsibilities, Skills, WhyAventus, WhyAventusPoints


class JobResponsibilityResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Responsibilities
        fields = ['Points']
        
class JobSkillsResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Skills
        fields = ['Points']
        
class WhyAventusResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = WhyAventusPoints
        fields = ['Points']


class JobApiListingApiSchemas(serializers.ModelSerializer):

    class Meta:
        model = JobVacancy
        fields = ['slug','id', 'designation','is_job']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

    
    
class JobDetailsApiListingApiSchemas(serializers.ModelSerializer):
    responsibility = serializers.SerializerMethodField('get_responsibility')
    skills = serializers.SerializerMethodField('get_skills')
    why_aventus = serializers.SerializerMethodField('get_why_aventus')
    class Meta:
        model = JobVacancy
        fields = ['slug','id','created_date','designation', 'min_exp', 'max_exp', 'description', 'is_active','responsibility','skills','why_aventus']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


    def get_responsibility(self,obj):
        job_responsibility = Responsibilities.objects.filter(job=obj.id)
        job_responsibility_response = JobResponsibilityResponseSchemas(job_responsibility,many=True)
        if job_responsibility_response:
            return job_responsibility_response.data
        else:
            return []
        
    def get_skills(self,obj):
        job_skills = Skills.objects.filter(job=obj.id)
        job_skill_response = JobResponsibilityResponseSchemas(job_skills,many=True)
        if job_skill_response:
            return job_skill_response.data
        else:
            return []
        
    def get_why_aventus(self,obj):
        why_aventus_data = WhyAventus.objects.filter(is_active=True).first()
        if why_aventus_data:
            why_aventus = WhyAventusPoints.objects.filter(why_aventus_id=why_aventus_data.id)
            why_aventus_response = WhyAventusResponseSchemas(why_aventus, many=True)
            return why_aventus_response.data
        else:
            return []


