import json
import logging
import uuid
from apps.home.functions import ConvertBase64File
from aventus import settings
from aventus.helpers.module_helper import imageDeletion
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
from apps.blog.models import Blog
from apps.career.models import JobApplication, JobVacancy
from apps.home.models import CompanyProfilePdf, Department,  OurClients, OurProjects, OurProjectsImages, OurServices, OurServicesPoints, ProjectDomain, TechStack, product_image_upload_image_dir
from apps.projects.models import ProjectCaseStudy
from apps.subscription.models import EmailSubscription
from aventus.helpers.signer import URLEncryptionDecryption
import requests
from urllib.parse import urlparse
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
logger = logging.getLogger(__name__)



class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Dashboard'

    def get(self, request, *args, **kwargs):
        project_count = ProjectCaseStudy.objects.filter(is_active=True)
        if project_count:
            self.context['total_project'] = project_count.count()
        else:
            self.context['total_project'] = '0'
            
        open_job_count = JobVacancy.objects.filter(is_active=True)
        if open_job_count:
            self.context['total_jobs'] = open_job_count.count()
        else:
            self.context['total_jobs'] = '0'

        total_clients = OurClients.objects.filter(is_active=True)
        if total_clients:
            self.context['total_clients'] = total_clients.count()
        else:
            self.context['total_clients'] = '0'

        total_blogs = Blog.objects.filter(is_active=True)
        if total_blogs:
            self.context['total_blogs'] = total_blogs.count()
        else:
            self.context['total_blogs'] = '0'
            
        total_our_service = OurServices.objects.filter(is_active=True)
        if total_our_service:
            self.context['total_our_service'] = total_our_service.count()
        else:
            self.context['total_our_service'] = '0'
            
        total_job_application = JobApplication.objects.all()
        if total_job_application:
            self.context['total_job_application'] = total_job_application.count()
        else:
            self.context['total_job_application'] = '0'
            
        total_sub_users = EmailSubscription.objects.all()
        if total_sub_users:
            self.context['total_sub_users'] = total_sub_users.count()
        else:
            self.context['total_sub_users'] = '0'
            
        return render(request, "admin/home/dashboard.html", self.context)

#______________________________OUR PROJECTS MANAGEMENT______________________________#



class OurProjectsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-projects/our-project-listing.html' 
        self.context['title'] = 'Home Page Projects'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Home Page Projects", "route" : '','active' : True})
        
        
class LoadOurProjectDatatable(BaseDatatableView):
    model = OurProjects
    order_columns = ['id','title','web_link','order','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return OurProjects.objects.all().order_by('-id')
    
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
                'order'         : escape(item.order),
                'title'         : escape(item.title),
                'web_link'      : escape(item.web_link),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveOurProjects(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OurProjects.objects.get(id = instance_id)
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
    


class OurProjectCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Home Page Projects'
        self.template = 'admin/home-page/our-projects/create-or-update-our-projects.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()

        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(OurProjects, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Home Page Projects", "route" : reverse('home:our.project-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Home Page Projects ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('campaigns_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(OurProjects, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = OurProjects()
                
            if request.FILES.get('image', None) is not None:
                instance.project_image = request.FILES.get('image',None)
                
            campaign_uuid       = request.POST.get('campaign_uuid', None)
            instance.title      = request.POST.get('title',None)
            instance.web_link   = request.POST.get('web_link',None)
            if request.POST.get('order',None):
                instance.order      = request.POST.get('order',None)
            else:
                instance.order = OurProjects.objects.all().count()+1
            instance.created_by = request.user
            instance.save()
            
            OurProjectsImages.objects.filter(uuid=campaign_uuid).update(learn_campaign=instance)
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:our.project-view.index')


@method_decorator(login_required, name='dispatch')
class DestroyOurProjectsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                OurProjects.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
#MULTIPLE IMAGE MANAGEMENT #
class CampaignImageUploadView(View):
     def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
     def post(self, request, *args, **kwargs):
        try:
            instance_id = 0
            
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
                uuid = request.POST.get('uuid', None)
                product_image = OurProjectsImages()
                product_image.uuid = uuid           
                path = default_storage.save(product_image_upload_image_dir(request), ContentFile(image.read()))
                product_image.image = path
                product_image.save()
                instance_id = product_image.id
                    
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
            self.response_format['data'] = instance_id
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
    
@method_decorator(login_required, name='dispatch')
class GetCampaignImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}

    def post(self, request, *args, **kwargs):
        campaign_id = request.POST.get('campaign_id')
        if campaign_id:
            product_images = OurProjectsImages.objects.filter(learn_campaign_id=campaign_id)
            json_data = []
            for item in product_images:
                image_url = request.build_absolute_uri(item.image.url)
                image_name = os.path.basename(urlparse(image_url).path)
                try:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    content_length = escape(response.headers['Content-length'])
                except (requests.exceptions.RequestException, KeyError):
                    content_length = "Unknown"
                
                json_data.append({
                    'id': escape(item.id),
                    'image': image_url,
                    'image_name': escape(image_name),
                    'size': content_length,
                })
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
            self.response_format['data'] = json_data

        return JsonResponse(self.response_format, status=200)


@method_decorator(login_required, name='dispatch')
class TemporaryImageDestroyView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            image_id = request.POST.get('id')


            action_type = request.POST.get('action_type')
            if image_id:
                if action_type == '5':  #ProductImages
                    image_del_obj = OurProjectsImages.objects.get(pk=image_id)
                    imageDeletion(request,image_del_obj)
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)
    
"""---------------------------------OurServices-----------------------------------------------"""

class OurServicesView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-services/our-services-listing.html' 
        self.context['title'] = 'Our Services'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Our Services", "route" : '','active' : True})
        
        
class LoadOurServicesDatatable(BaseDatatableView):
    model = OurServices
    order_columns = ['id','title','is_active','is_popular'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return OurServices.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search)|Q(url__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'title'         : escape(item.title),
                'is_main'       : escape(item.is_main),
                'is_active'     : escape(item.is_active),
                'is_popular'    : escape(item.is_popular),
                'order'         : escape(item.order),
                'url'           : escape(item.url),
            })
        return json_data
    
    
@method_decorator(login_required, name='dispatch')
class DestroyOurServicesRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                OurServices.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveOurServices(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OurServices.objects.get(id = instance_id)
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
    

class PopularOrNonPopularOurServices(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OurServices.objects.get(id = instance_id)
            if instance_id:
                if instance.is_popular:
                    instance.is_popular = False
                else:
                    instance.is_popular =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class OurServicesCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Our Services'
        self.template = 'admin/home-page/our-services/create-or-update-our-services.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(OurServices, id=id)
            
        service_points  = OurServicesPoints.objects.filter(service=id)
        
        if service_points:
            self.context['service_points'] = OurServicesPoints.objects.filter(service=id)

            
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Our Services", "route" : reverse('home:our.services-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Our Services ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        
        service_points = []
        for key, value in request.POST.items():
            if key.startswith('features') and '[name]' in key:
                description_key = key.replace('[name]', '[description]')
                description_value = request.POST.get(description_key, '')
                service_points.append(f'title: {value}, description: {description_value}')

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(OurServices, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = OurServices()
                
            instance.title                = request.POST.get('title',None)
            instance.full_name            = request.POST.get('full_name',None)
            if request.POST.get('order',None):
                instance.order                = request.POST.get('order',None)
            else:
                instance.order = OurServices.objects.all().count()+1
            instance.url                  = request.POST.get('url',None)
            instance.description_title    = request.POST.get('description_title',None)
            instance.description          = request.POST.get('description',None)
            instance.button_titile          = request.POST.get('button_titile',None)
            
            if request.FILES.get('service_image', None) is not None:
                instance.service_image       = request.FILES.get('service_image',None)
                
            # SEO
            if request.FILES.get('og_image', None) is not None:
                instance.og_image       = request.FILES.get('og_image',None)

            instance.meta_title         = request.POST.get('meta_title',None)
            instance.meta_description   = request.POST.get('meta_description',None)
            instance.meta_keyword       = request.POST.get('meta_keyword',None)
            instance.meta_image_title   = request.POST.get('meta_image_title',None)
            instance.created_by         = request.user
            instance.save()
            OurServicesPoints.objects.filter(service=instance).delete()
            
            project_aim = []

            for key, value in request.POST.items():
                if key.startswith('features') and '[name]' in key:
                    index = key.split('[', 2)[1].split(']', 1)[0]
                    name = request.POST.get(f'features[{index}][name]')
                    description = request.POST.get(f'features[{index}][description]')
                    project_aim.append((name, description))

            for name, description in project_aim:
                if name.strip():  # Use 'name' here instead of 'index'
                    service_points = OurServicesPoints()
                    service_points.service = instance
                    service_points.title = name
                    service_points.description = description
                    service_points.save()
                        
                messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            self.context['service_points'] = service_points
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:our.services-view.index')


class NavBarMainOurServices(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OurServices.objects.get(id = instance_id)
            if instance_id:
                if instance.is_main:
                    instance.is_main = False
                else:
                    instance.is_main =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class OurServiceDuplicateUrlValidation(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            title = request.POST.get('url',None)
            id = request.POST.get('instance_id', None)
            check_url   = OurServices.objects.filter(url__iexact=title)
            if check_url is not None and id:
                check_url = check_url.exclude(pk=id)
            if check_url.exists():
                self.response_format['status_code']=100
                self.response_format['message']= 'Url Already Exist'
            else:
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)

"""---------------------------------OurServices-----------------------------------------------"""


class DepartmentView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/department/department-listing.html' 
        self.context['title'] = 'Department'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Department", "route" : '','active' : True})
        
        
class LoadDepartmentDatatable(BaseDatatableView):
    model = Department
    order_columns = ['id','title','is_active','order'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Department.objects.all().order_by('-id')
    
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
                'order'         : escape(item.order),
                'is_active'     : escape(item.is_active),
            })
        return json_data
    
    
@method_decorator(login_required, name='dispatch')
class DestroyDepartmentRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Department.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveDepartment(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Department.objects.get(id = instance_id)
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
    

class DepartmentCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Department'
        self.template = 'admin/home-page/department/create-or-update-department.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Department, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Department", "route" : reverse('home:department-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Department ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Department, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Department()
                
            instance.title    = request.POST.get('title',None)
            if request.POST.get('order',None):
                instance.order    = request.POST.get('order',None)
            else:
                instance.order    = Department.objects.all().count()+1

            instance.created_by     = request.user
            instance.save()
                
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:department-view.index')
    
    
#______________________________OUR CLIENTS MANAGEMENT______________________________#

class OurClientsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-clients/our-clients-listing.html' 
        self.context['title'] = 'Our Clients'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        self.context['instance'] = OurClients.objects.all().order_by('-order')
        self.context['instance_count'] = OurClients.objects.count()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Our Project", "route" : '','active' : True})
        
        
class LoadOurClientsDatatable(BaseDatatableView):
    model = OurClients
    order_columns = ['id','title','web_link','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return OurClients.objects.all().order_by('-id')
    
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
                'project_image' : escape(self.request.build_absolute_uri(item.client_logo.url)),
                'title'         : escape(item.title),
                'web_link'      : escape(item.web_link),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveOurClients(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OurClients.objects.get(id = instance_id)
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
    
    
class OurClientsCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Our Clients'
        self.template = 'admin/home-page/our-clients/create-or-update-our-clients.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(OurClients, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "our Clients", "route" : reverse('home:our.clients-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} our Clients ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(OurClients, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = OurClients()
                
            if request.FILES.get('image', None) is not None:
                instance.client_logo = request.FILES.get('image',None)
                
            instance.title    = request.POST.get('title',None)
            instance.web_link        = request.POST.get('web_link',None)
            instance.created_by     = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if instance_id is not None and instance_id != "":
                return redirect('home:our.clients.update', id=instance_id)
            return redirect('home:our.clients.create')
        return redirect('home:our.clients-view.index')


@method_decorator(login_required, name='dispatch')
class DestroyOurClientsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                OurClients.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)



"""OUR CLIENTS NEW METHOD"""
from django.http import JsonResponse



class OurClientsImageUploadingView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            is_update = request.POST.get('is_update')
            
            if is_update == "True":
                # Update existing instances
                data = json.loads(request.POST.get('images'))
                for image_info in data:
                    order = image_info['order']
                    image_id = image_info['image_id']
                    if image_id:
                        # Check if the instance with the given image_id exists
                        client_instance = OurClients.objects.get(id=image_id)
                        if client_instance:
                            client_instance.order = order
                            client_instance.save()
            else:
                # Create new instances
                orders = request.FILES.keys()
                instances_to_create = []

                for order in orders:
                    uploaded_file = request.FILES[order]
                    if uploaded_file:
                        instance = OurClients(order=order, client_logo=uploaded_file)
                        instances_to_create.append(instance)

                # Bulk create instances
                OurClients.objects.bulk_create(instances_to_create)

            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'Error occurred during bulk insert'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)





@method_decorator(login_required, name='dispatch')
class DestroyOurClientsOrderRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.get('instance_id')
            delete_all = request.POST.get('is_delete_all')
            if delete_all == "true":
                OurClients.objects.all().delete()
            if instance_id:
                OurClients.objects.filter(id=instance_id).delete()
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

"""---------------------------------PROJECT DOMAIN-----------------------------------------------"""


class ProjectDomainView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/domain/domain-listing.html' 
        self.context['title'] = 'Domain'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Domain", "route" : '','active' : True})
        
        
class ProjectDomainDatatable(BaseDatatableView):
    model = ProjectDomain
    order_columns = ['id','title','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return ProjectDomain.objects.all().order_by('-id')
    
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
    
    
@method_decorator(login_required, name='dispatch')
class DestroyProjectDomainRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                ProjectDomain.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveProjectDomain(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = ProjectDomain.objects.get(id = instance_id)
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
    

class ProjectDomainCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Domain'
        self.template = 'admin/home-page/domain/create-or-update-domain.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(ProjectDomain, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Domain", "route" : reverse('home:domain-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Domain ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(ProjectDomain, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = ProjectDomain()
                
            instance.title    = request.POST.get('title',None)
            instance.created_by     = request.user
            instance.save()
                
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:domain-view.index')
    
    
    

#_____________________________DOWNLOAD FACTSHEET MANAGEMENT__________________________________#


class FactsheetView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.template = 'admin/home-page/company-profile-pdf/factsheet.html'
        self.context['title'] = 'Download Company Profile'
        self.generateBreadcrumbs()

    def get(self, request, *args, **kwargs):
        data_exists = self.check_data_exists()  # Add this line to check if data exists
        self.context['data_exists'] = data_exists  # Add this line to pass data_exists to the template
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Company Profile", "route": '', 'active': True})

    def check_data_exists(self):
        data_exists = CompanyProfilePdf.objects.exists()
        return data_exists


class FactsheetDatatable(BaseDatatableView):
    model = CompanyProfilePdf
    order_columns = ['id','title','is_active']
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return CompanyProfilePdf.objects.all().order_by('-id')
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
                'title'         : escape(item.title),
                'file'          : escape(self.request.build_absolute_uri(item.file.url)),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'is_active'     : escape(item.is_active)
            })
        return json_data


class FactsheetCreateOrUpdateView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Download Company Profile'
        self.action = "Create"  
        self.template = 'admin/home-page/company-profile-pdf/create-or-update.html'
                
    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update "    
            self.context['instance'] = get_object_or_404(CompanyProfilePdf, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
        
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Company Profile", "route" : reverse('home:factsheet.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Company Profile".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        id = request.POST.get('instance_id', None)
        try:
            if id:
                self.action = 'Updated'
                instance = get_object_or_404(CompanyProfilePdf, id=id)
            else:
                instance = CompanyProfilePdf()
            instance.title               = request.POST.get('title',None)
            
            if request.FILES.__len__() != 0:
                if request.FILES.get('doument_pdf', None) is not None:
                    instance.file = request.FILES.get('doument_pdf', None)
            instance.save()
            
            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if id is not None:
                return redirect('home:factsheet.update', id=id)
            return redirect('home:factsheet.create')
        return redirect('home:factsheet.index')


@method_decorator(login_required, name='dispatch')
class DestroyFactsheetRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            ids = request.POST.getlist('ids[]')
            if ids:
                CompanyProfilePdf.objects.filter(id__in=ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

class ActiveInactiveFactsheet(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            id = request.POST.get('id', None)
            instance = CompanyProfilePdf.objects.get(id = id)
            if id:
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


"""----------------------TECH STACK----------------------------------"""

class ProjectStackView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/tech_stack/tech-stack-listing.html' 
        self.context['title'] = 'Tech Stack'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Tech Stack", "route" : '','active' : True})
        
        
class ProjectStackDatatable(BaseDatatableView):
    model = TechStack
    order_columns = ['id','stack_title','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return TechStack.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(stack_title__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        image = self.request.build_absolute_uri("/")
        default_image_url = str(image)+'media/default/image/face-logo.png'
        
        for item in qs:
            stack_logo_url = default_image_url  
            
            if item.stack_logo:  # Check if stack_logo is not null
                stack_logo_url = self.request.build_absolute_uri(item.stack_logo.url)
            
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'stack_logo'    : escape(stack_logo_url),
                'title'         : escape(item.stack_title),
                'is_active'     : escape(item.is_active),
            })
        return json_data
    
    
@method_decorator(login_required, name='dispatch')
class DestroyProjectStackRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                TechStack.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveProjectStack(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = TechStack.objects.get(id = instance_id)
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
    

class ProjectStackCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Tech Stack'
        self.template = 'admin/home-page/tech_stack/create-or-update-tech-stack.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(TechStack, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Tech Stack", "route" : reverse('home:stack-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Tech Stack ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(TechStack, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = TechStack()
                
            if request.FILES.get('stack_logo', None) is not None:
                instance.stack_logo       = request.FILES.get('stack_logo',None)
            # else:
            #     instance.stack_logo = 'assets/media/images/face-logo.png'
                
            instance.stack_title    = request.POST.get('stack_title',None)
            instance.created_by     = request.user
            instance.save()
                
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('home:stack-view.index')