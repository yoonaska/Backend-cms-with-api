import os
from random import randint
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect, render
import logging
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import uuid
from apps.home.models import OurServices, ProjectDomain, TechStack
from apps.projects.models import  EliminatingChallengesPoints, ProblemStatement, ProjectAminPoints, ProjectCaseStudy, ProjectCaseStudyBannerImage, ProjectCaseStudyBannerMultipleImages, ProjectCaseStudyImages, ProjectCaseStudyOutcomes, ProjectLiveUrls, about_image_upload_image_dir
from aventus.helpers.module_helper import imageDeletion
from aventus.helpers.signer import URLEncryptionDecryption
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
from urllib.parse import urlparse
logger = logging.getLogger(__name__)
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


"""-------------------------- PROJECT CASE STUDY MANAGEMENT SECTIONS-----------------------------------------"""

class ProjectCaseStudyView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-projects/project-case-study/our-project-case-study-listing.html'    
        self.context['title'] = 'Project'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Project", "route" : '','active' : True})
        
        
class LoadProjectCaseStudyDatatable(BaseDatatableView):
    model = ProjectCaseStudy
    order_columns = ['id','project_name','domain','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return ProjectCaseStudy.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(project_name__istartswith=search)|Q(domain__title__istartswith=search)|Q(service__title__istartswith=search)|Q(url__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'project_image' : escape(self.request.build_absolute_uri(item.project_image.url)),
                'title'         : escape(item.project_name),
                'domain'        : escape(item.domain),
                'service'       : escape(item.service),
                'url'           : escape(item.url),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class CreateOrUpdateProjectCaseStudySection(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-projects/project-case-study/create-or-update-project-case-study.html'
        self.context['title'] = 'projects'
        self.action = "Create"
        
    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()
        
        if id:
            self.action = "Update "
            self.context['instance']    = ProjectCaseStudy.objects.get(id=id)
        self.context['categories']      = ProjectDomain.objects.filter(is_active=True)
        self.context['our_services']     = OurServices.objects.filter(is_active=True)
        
        project_aim                 = ProjectAminPoints.objects.filter(project=id)
        project_problem_statement   = ProblemStatement.objects.filter(project=id)
        project_challenges_points   = EliminatingChallengesPoints.objects.filter(project=id)
        project_live_urls           = ProjectLiveUrls.objects.filter(project=id)
        project_out_comes           = ProjectCaseStudyOutcomes.objects.filter(project=id)
        
        if project_live_urls:
            self.context['project_live_urls'] = ProjectLiveUrls.objects.filter(project=id)
            
        if project_out_comes:
            self.context['project_out_comes'] = ProjectCaseStudyOutcomes.objects.filter(project=id)
            
        if project_aim:
            self.context['project_aim'] = ProjectAminPoints.objects.filter(project=id)
            
        if project_problem_statement:
            self.context['project_problem_statement'] = ProblemStatement.objects.filter(project=id)
            
        if project_challenges_points:
            self.context['project_challenges_points'] = EliminatingChallengesPoints.objects.filter(project=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "projects", "route" : reverse('projects:project-case-study.listing') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} projects".format(self.action), "route" : '','active' : True})
        
    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('campaigns_id', None)
        form_data = request.POST
        #project_aim
        
        project_aims = []
        for key, value in request.POST.items():
            if key.startswith('features') and '[name]' in key:
                project_aims.append(f'Points: {value}>')
                
        #project_challenges_points
        project_challenges_pointss = []
        for key, value in request.POST.items():
            if key.startswith('project_challenges_points') and '[name]' in key:
                project_challenges_pointss.append(f'Points: {value}>')
                
        #project_problem_statement
        project_problem_statements = []
        for key, value in request.POST.items():
            if key.startswith('problem_statement') and '[name]' in key:
                project_problem_statements.append(f'Points: {value}>')
        
        #project_out_comes
        project_out_comess = []
        for key, value in request.POST.items():
            if key.startswith('outcomes') and '[name]' in key:
                description_key = key.replace('[name]', '[url]')
                description_value = request.POST.get(description_key, '')
                project_out_comess.append(f'title: {value}, url: {description_value}')
        try:
            if instance_id:
                instance = ProjectCaseStudy.objects.get(id=instance_id)
            else:
                instance = ProjectCaseStudy()
        


            if request.FILES.get('project_image', None) is not None:
                instance.project_image = request.FILES.get('project_image',None)
            
            if request.FILES.get('project_logo', None) is not None:
                instance.project_logo = request.FILES.get('project_logo',None)
                
            if request.FILES.get('project_image_banner', None) is not None:
                instance.project_image_banner = request.FILES.get('project_image_banner',None)
                
            campaign_uuid                                 = request.POST.get('campaign_uuid', None)
            instance.project_name                         = request.POST.get('project_name',None)
            instance.project_tags                         = request.POST.get('project_tags',None)
            instance.url                                  = request.POST.get('url',None)
            instance.domain_id                            = request.POST.get('domain',None)
            instance.service_id                           = request.POST.get('service',None)
            instance.research                             = request.POST.get('research', None)
            instance.design_strategy                      = request.POST.get('design_strategy',None)
            instance.ui                                   = request.POST.get('ui',None)
            instance.backend_development                  = request.POST.get('backend_development',None)
            instance.other_technology                     = request.POST.get('other_technology',None)
            instance.frontend_development                 = request.POST.get('frontend_development',None)
            instance.testing                              = request.POST.get('testing',None)
            instance.web_url_title                        = request.POST.get('web_url_title',None)
            instance.eliminating_challenges_description   = request.POST.get('challenges_description',None)
            instance.front_technology                     = request.POST.get('front_technology',None)
            instance.backend_technology                   = request.POST.get('backend_technology',None)
            instance.project_mode_of_functions            = request.POST.get('project_mode_of_functions',None)
            # BANNER
            instance.banner_description                   = request.POST.get('banner_description',None)
            instance.banner_title                         = request.POST.get('banner_title',None)
            #
            # SEO SECTION
            if request.FILES.get('og_image', None) is not None:
                instance.og_image       = request.FILES.get('og_image',None)

            instance.meta_title         = request.POST.get('meta_title',None)
            instance.meta_description   = request.POST.get('meta_description',None)
            instance.meta_keyword       = request.POST.get('meta_keyword',None)
            instance.meta_image_title   = request.POST.get('meta_image_title',None)
            instance.save()
            
            ProjectCaseStudyImages.objects.filter(uuid=campaign_uuid).update(project_case_study=instance)
            ProjectAminPoints.objects.filter(project=instance).delete()
            ProblemStatement.objects.filter(project=instance).delete()
            EliminatingChallengesPoints.objects.filter(project=instance).delete()
            ProjectLiveUrls.objects.filter(project=instance).delete()
            ProjectCaseStudyOutcomes.objects.filter(project=instance).delete()

            project_aim = []
            
            for key, value in request.POST.items():
                if key.startswith('features') and '[name]' in key:
                    project_aim.append(value)

            for index in project_aim:
                if index.strip():
                    benefit=ProjectAminPoints()
                    benefit.project=instance
                    benefit.Points=index
                    benefit.save()
                    
            project_challenges = []
            
            for key, value in request.POST.items():
                if key.startswith('project_challenges_points') and '[name]' in key:
                    project_challenges.append(value)

            for index in project_challenges:
                if index.strip():
                    benefit=EliminatingChallengesPoints()
                    benefit.project=instance
                    benefit.Points=index
                    benefit.save()
                    
            project_problem_statement = []
            
            for key, value in request.POST.items():
                if key.startswith('problem_statement') and '[name]' in key:
                    project_problem_statement.append(value)

            for index in project_problem_statement:
                if index.strip():
                    benefit=ProblemStatement()
                    benefit.project=instance
                    benefit.Points=index
                    benefit.save()
                    
            project_url_links = []
            
            for key, value in request.POST.items():
                if key.startswith('url_links') and '[name]' in key:
                    project_url_links.append(value)

            for index in project_url_links:
                if index.strip():
                    benefit=ProjectLiveUrls()
                    benefit.project=instance
                    benefit.Points=index
                    benefit.save()

                
            project_out_comes = []

            for key, value in request.POST.items():
                if key.startswith('outcomes') and '[name]' in key:
                    index = key.split('[', 2)[1].split(']', 1)[0]
                    name = request.POST.get(f'outcomes[{index}][name]')
                    url = request.POST.get(f'outcomes[{index}][url]')
                    project_out_comes.append((name, url))

            for name, url in project_out_comes:
                if name.strip():  # Use 'name' here instead of 'index'
                    service_points = ProjectCaseStudyOutcomes()
                    service_points.project = instance
                    service_points.title = name
                    service_points.url = url
                    service_points.save()

            messages.success(request, f"Data Successfully "+ self.action)
        
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['project_aim'] = project_aims
            self.context['project_problem_statement'] = project_problem_statements
            self.context['project_challenges_points'] = project_challenges_pointss
            self.context['project_out_comes'] = project_out_comess
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('projects:project-case-study.listing')
    
    
class DestroyProjectCaseStudyRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                ProjectCaseStudy.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


class ActiveInactiveProjectCaseStudys(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            learn_id = request.POST.get('id')
            instance = ProjectCaseStudy.objects.get(id = learn_id)
            if learn_id:
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
    
    
class ProjectCaseStudyImageImageUploadView(View):
     def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
     def post(self, request, *args, **kwargs):

        try:
            instance_id = 0
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
                product_image = ProjectCaseStudyImages()
                product_image.uuid = request.POST.get('uuid', None)   
                path = default_storage.save(about_image_upload_image_dir(request), ContentFile(image.read()))
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
class GetProjectCaseStudyImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}

    def post(self, request, *args, **kwargs):
        campaign_id = request.POST.get('campaign_id')
        if campaign_id:
            product_images = ProjectCaseStudyImages.objects.filter(project_case_study=campaign_id).order_by('id')
            json_data = []
            for item in product_images:
                image_url = request.build_absolute_uri(item.image.url)
                image_name = os.path.basename(urlparse(image_url).path)
                
                try:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    content_length = escape(response.headers['Content-length'])
                except (requests.exceptions.RequestException, KeyError):
                    # Handle the case when the 'Content-length' header is not present
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
                    image_del_obj = ProjectCaseStudyImages.objects.get(id=image_id)
                    imageDeletion(request,image_del_obj)
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)
    

"""DUPLICATE CREATION """

class ProjectCaseStudyDuplicateUrlValidation(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            title = request.POST.get('url',None)
            id = request.POST.get('casestudy_id', None)
            check_url   = ProjectCaseStudy.objects.filter(url__iexact=title)
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


class DuplicateProjectCaseStudyRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.get('id')
            if instance_id:
                original_instance = get_object_or_404(ProjectCaseStudy, id=instance_id)
                
                # Create a duplicate of the ProjectCaseStudy record
                new_instance = ProjectCaseStudy.objects.create(
                    project_tags                          = original_instance.project_tags,
                    project_name                          = original_instance.project_name,
                    url                                   = original_instance.url,
                    project_image                         = original_instance.project_image,
                    domain                                = original_instance.domain,
                    service                               = original_instance.service,
                    
                    research                              = original_instance.research,
                    design_strategy                       = original_instance.design_strategy,
                    ui                                    = original_instance.ui,
                    backend_development                   = original_instance.backend_development,
                    frontend_development                  = original_instance.frontend_development,
                    testing                               = original_instance.testing,
                    
                    backend_technology                    = original_instance.backend_technology,
                    other_technology                      = original_instance.other_technology ,
                    front_technology                      = original_instance.front_technology,
                    web_url_title                         = original_instance.web_url_title,
                    eliminating_challenges_description    = original_instance.eliminating_challenges_description ,
                    project_mode_of_functions             = original_instance.project_mode_of_functions,
                    
                    
                    project_image_banner                  = original_instance.project_image_banner,  
                    project_logo                          = original_instance.project_logo,          
                    banner_title                          = original_instance.banner_title,          
                    banner_description                    = original_instance.banner_description,    
                    # SEO original_instance.# SEO ori
                    og_image                              = original_instance.og_image,              
                    meta_image_title                      = original_instance.meta_image_title,      
                    meta_title                            = original_instance.meta_title,            
                    meta_description                      = original_instance.meta_description,      
                    meta_keyword                          = original_instance.meta_keyword,          
                    is_active                             = False
                )

                # Duplicate related records (assuming ForeignKey relationships)
                related_models = [ProjectAminPoints, ProblemStatement, EliminatingChallengesPoints, ProjectLiveUrls]
                for related_model in related_models:
                    related_records = related_model.objects.filter(project=original_instance)
                    for related_record in related_records:
                        new_related_record = related_record.__class__.objects.create(
                            project=new_instance,
                            Points=related_record.Points,
                            # ... other related fields ...
                        )
                        
                # Duplicate ProjectCaseStudyOutcomes related records
                project_outcomes_records = ProjectCaseStudyOutcomes.objects.filter(project=original_instance)
                for project_outcomes_record in project_outcomes_records:
                    new_project_outcomes_record = ProjectCaseStudyOutcomes.objects.create(
                        project=new_instance,
                        title=project_outcomes_record.title,
                        url=project_outcomes_record.url,
                        # ... other related fields ...
                    )
                
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                
        except Exception as e:
            self.response_format['message'] = 'Error'
            self.response_format['error'] = str(e)
        
        return JsonResponse(self.response_format, status=200)

"""-----------------------------------PROJECT CASE STUDY BANNER MANAGEMENT SECTION --------------------------------------"""

class ProjectCaseStudyBannerView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-projects/project-case-study-banner/our-project-case-study-banner-listing.html'   
        self.context['title'] = 'Project Case Study Banner'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Project Case Study Banner", "route" : '','active' : True})
        
        
class LoadProjectCaseStudyBannerDatatable(BaseDatatableView):
    model = ProjectCaseStudyBannerImage
    order_columns = ['id','project','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return ProjectCaseStudyBannerImage.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(project__project_name__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            project_name = item.project.project_name if item.project else ''
            service_title = item.project.service.title if item.project.service else ''
            display_text = f"{project_name}/{service_title}" if project_name and service_title else project_name or service_title
            
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                # 'banner_image'  : escape(self.request.build_absolute_uri(item.banner_image.url)),
                'project'       : escape(display_text),
                'is_active'     : escape(item.is_active),
            })
        return json_data
    

class DestroyProjectCaseStudyBannerRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                ProjectCaseStudyBannerImage.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveProjectCaseStudyBanner(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id')
            instance = ProjectCaseStudyBannerImage.objects.get(id = instance_id)
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
    

class CreateOrUpdateProjectCaseStudyBannerSection(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/our-projects/project-case-study-banner/create-or-update-project-banner.html'
        self.context['title'] = 'Project Case Study Banner'
        self.action = "Create"
        
    
    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()
        
        if id:
            self.action = "Update"
            self.context['instance']    = ProjectCaseStudyBannerImage.objects.get(id=id)
        self.context['categories']  = ProjectCaseStudy.objects.filter(is_active=True)
        self.context['tech_stack']  = TechStack.objects.filter(is_active=True)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Project Case Study Banner", "route" : reverse('projects:project.case.study.banner.listing') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Project Case Study Banner".format(self.action), "route" : '','active' : True})
        
    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('campaigns_id', None)
        form_data = request.POST

        try:
            if instance_id:
                instance = ProjectCaseStudyBannerImage.objects.get(id=instance_id)
            else:
                instance = ProjectCaseStudyBannerImage()

            campaign_uuid                 = request.POST.get('campaign_uuid', None)
            instance.project_id           = request.POST.get('project',None)
            instance.tech_stack_one_id    = request.POST.get('tech_stack_one',None)
            instance.tech_stack_two_id    = request.POST.get('tech_stack_two',None)
            instance.description          = request.POST.get('description',None)
            instance.title                = request.POST.get('title',None)
            instance.url                  = request.POST.get('url',None)
            instance.domain_title         = request.POST.get('domain_title',None)
            instance.save()
            
            ProjectCaseStudyBannerMultipleImages.objects.filter(uuid=campaign_uuid).update(project_case_study=instance)
            messages.success(request, f"Data Successfully "+ self.action)
        
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('projects:project.case.study.banner.listing')
    
    
# MULTIPLE IMAGE SECTION

class ProjectCaseStudyBannerImageImageUploadView(View):
     def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
     def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.get('campaign_id')
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
              
                product_image = ProjectCaseStudyBannerMultipleImages()
                product_image.uuid = request.POST.get('uuid', None) 
                path = default_storage.save(about_image_upload_image_dir(request), ContentFile(image.read()))
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
class GetProjectCaseStudyBannerImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data": []}

    def post(self, request, *args, **kwargs):
        campaign_id = request.POST.get('campaign_id')
        if campaign_id:
            product_images = ProjectCaseStudyBannerMultipleImages.objects.filter(project_case_study=campaign_id)
            json_data = []
            for item in product_images:
                image_url = request.build_absolute_uri(item.image.url)
                image_name = os.path.basename(urlparse(image_url).path)
                
                try:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    content_length = escape(response.headers['Content-length'])
                except (requests.exceptions.RequestException, KeyError):
                    # Handle the case when the 'Content-length' header is not present
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
class ProjectCaseStudyBannerTemporaryImageDestroyView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            image_id = request.POST.get('id')
            action_type = request.POST.get('action_type')
            if image_id:
                if action_type == '5':  #ProductImages
                    image_del_obj = ProjectCaseStudyBannerMultipleImages.objects.get(id=image_id)
                    imageDeletion(request,image_del_obj)
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)