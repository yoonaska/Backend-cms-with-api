import logging
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.career.models import JobApplication,JobVacancy, Responsibilities, Skills, WhyAventus, WhyAventusPoints
from aventus.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)


#______________________________JOB MANAGEMENT MANAGEMENT______________________________#

class JobVacancyView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/admin/career/job-vacancy/job-vacancy.html' 
        self.context['title'] = 'Job'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Designation", "route" : '','active' : True})
        
        
class LoadJobVacancyDatatable(BaseDatatableView):
    model = JobVacancy
    order_columns = ['id','designation','min_exp','max_exp','created_date','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return JobVacancy.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(designation__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'category'      : escape(item.designation),
                'experience'    : '{}-{}'.format(escape(item.min_exp), escape(item.max_exp)),
                'posted_on'     : escape(item.created_date.date()),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveJobVacancy(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = JobVacancy.objects.get(id = instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    
    
class JobVacancyCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Job'
        self.template = 'admin/admin/career/job-vacancy/create-or-update-job-vacancy.html'    

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(JobVacancy, id=id)
        
        responsibilities = Responsibilities.objects.filter(job_id=id)
        skills = Skills.objects.filter(job_id=id)
        if responsibilities:
            self.context['responsibilities'] = Responsibilities.objects.filter(job=id)
        else:
            self.context['responsibilities'] = None
        if skills:
            self.context['skills'] = Skills.objects.filter(job=id)


        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Job", "route" : reverse('career:job.vacancy.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Job ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(JobVacancy, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = JobVacancy()

            instance.designation    = request.POST.get('designation',None)
            instance.min_exp        = request.POST.get('min_exp',None)
            instance.max_exp        = request.POST.get('max_exp',None)
            instance.description    = request.POST.get('description',None)
            instance.tags           = request.POST.get('tags',None)
            instance.created_by     = request.user
            instance.save()
            
            Responsibilities.objects.filter(job=instance).delete()
            Skills.objects.filter(job=instance).delete()
            
            responsibilities = []
            skills = []
            
            for key, value in request.POST.items():
                if key.startswith('features') and '[name]' in key:
                    responsibilities.append(value)
            for key, value in request.POST.items():
                if key.startswith('subfeatures') and '[subname]' in key:
                    skills.append(value)
                    
            for index in responsibilities:
                if index.strip():
                    responsibilities=Responsibilities()
                    responsibilities.job=instance
                    responsibilities.Points=index
                    responsibilities.save()
            
            for index in skills:
                if index.strip():
                    skill=Skills()
                    skill.job=instance
                    skill.Points=index
                    skill.save()

            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('career:job.vacancy.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyJobVacancyRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                JobVacancy.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
#____________________________WHY AVENTUS__________________________________________________#



class WhyAventusView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/admin/career/why-aventus/why-aventus-load-datatable.html'    
        self.context['title'] = 'Why Aventus'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()
        self.context['data_exists'] = data_exists
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Why Aventus", "route" : '','active' : True})
        
    def check_data_exists(self):
        data_exists = WhyAventus.objects.exists()
        return data_exists


class LoadWhyAventusDatatable(BaseDatatableView):
    model = WhyAventus
    order_columns = ['id','title','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return WhyAventus.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'title'         : escape(item.title),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveWhyAventus(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = WhyAventus.objects.get(id = instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)

    
class WhyAvenytusCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Why Aventus'
        self.template = 'admin/admin/career/why-aventus/why-aventus-create-or-update.html'      


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(WhyAventus, id=id)
        
        benefits = WhyAventusPoints.objects.filter(why_aventus=id)
        if benefits:
            self.context['benefits'] = WhyAventusPoints.objects.filter(why_aventus=id)


        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Why Aventus", "route" : reverse('career:why.aventus.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Why Aventus ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        benefits_points = []

        # Iterate through the keys and values in request.POST
        for key, value in request.POST.items():
            if key.startswith('features') and '[name]' in key:
                benefits_points.append(f'Points: {value}>')

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(WhyAventus, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = WhyAventus()

            instance.title        = request.POST.get('title',None)
            instance.created_by   = request.user
            instance.save()
            
            WhyAventusPoints.objects.filter(why_aventus=instance).delete()
            
            benefits = []
            
            for key, value in request.POST.items():
                if key.startswith('features') and '[name]' in key:
                    benefits.append(value)

            for index in benefits:
                if index.strip():
                    benefit=WhyAventusPoints()
                    benefit.why_aventus=instance
                    benefit.Points=index
                    benefit.save()

            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['benefits'] = benefits_points
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('career:why.aventus.view.index')


@method_decorator(login_required, name='dispatch')
class DestroyWhyAventusRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                WhyAventus.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
    
"""----------------------JOB APPLICATION LISTING-------------------"""

class JobApplicationView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/job-application/job-application-listing.html'  
        self.context['title'] = 'Job Applications'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Job Application", "route" : '','active' : True})


class LoadJobApplicationDatatable(BaseDatatableView):
    model = JobApplication
    order_columns = ['id','job','name','email','phone_number'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return JobApplication.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(email__istartswith=search)|Q(job__designation__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'job-name'        : escape(item.designation),
                'name'            : escape(item.name),
                'email'           : escape(item.email),
                'phone-number'    : escape(item.phone_number),
                'enquiry-on'      : escape(item.created_date.date()),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


@method_decorator(login_required, name='dispatch')
class DestroyJobApplicationRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                JobApplication.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


class JobApplicationDetailViewView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Job Application'
        self.template = 'admin/home-page/job-application/job-application-detail.html'
        

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Detail View"
            self.context['instance'] = get_object_or_404(JobApplication, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Job Application", "route" : reverse('career:job-application.view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Job Application".format(self.action), "route" : '','active' : True})
