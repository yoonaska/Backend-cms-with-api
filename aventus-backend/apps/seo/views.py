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
from apps.seo.models import SeoManagement
from aventus.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)

#______________________________BLOG MANAGEMENT MANAGEMENT______________________________#

class SeoManagementView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/seo-management/seo-listing.html'  
        self.context['title'] = 'Seo Management'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Seo", "route" : '','active' : True})
        

class LoadSeoManagementDatatable(BaseDatatableView):
    model = SeoManagement
    order_columns = ['id','og_image','meta_image_title','meta_title','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True)
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False)
        else:
            return SeoManagement.objects.all()
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(meta_title__istartswith=search)|Q(meta_image_title__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'seo_page'      : escape(item.get_seo_page_display()),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'og_image'    : escape(self.request.build_absolute_uri(item.og_image.url)),
                'title'         : escape(item.meta_image_title),
                'date'          : escape(item.meta_title),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveSeoManagement(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = SeoManagement.objects.get(id = instance_id)
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
    
    
class SeoManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Seo Management'
        self.template = 'admin/home-page/seo-management/create-or-update-seo.html'
        

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(SeoManagement, id=id)

        self.generateBreadcrumbs()
        self.context['seo_page'] = SeoManagement.SEO_DISPLAY_PAGE  
        return render(request, self.template, context=self.context)
    
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Seo", "route" : reverse('seo:seo-management-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Seo".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST

        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(SeoManagement, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = SeoManagement()
                
            seo_page = request.POST.get('seo_page',None)
            id = request.POST.get('instance_id', None)
            check_title  = SeoManagement.objects.filter(seo_page=seo_page)
            if check_title is not None and id:
                check_title = check_title.exclude(pk=id)
            if check_title.exists():
                messages.error(request, f"Seo For {seo_page} Already Exist")
                
            else:
                if request.FILES.get('og_image', None) is not None:
                    instance.og_image       = request.FILES.get('og_image',None)

                instance.seo_page           = request.POST.get('seo_page',None)
                instance.meta_title         = request.POST.get('meta_title',None)
                instance.seo_page           = request.POST.get('seo_page',None)
                instance.meta_description   = request.POST.get('meta_description',None)
                instance.meta_keyword       = request.POST.get('meta_keyword',None)
                instance.meta_image_title   = request.POST.get('meta_image_title',None)
                instance.created_by         = request.user
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
        return redirect('seo:seo-management-view.index')


@method_decorator(login_required, name='dispatch')
class DestroySeoManagementRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                SeoManagement.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)