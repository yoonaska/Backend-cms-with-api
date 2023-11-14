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
from apps.news.models import News
from aventus.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)





#______________________________NEWS MANAGEMENT______________________________#

class NewsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/news/news-listing.html'    
        self.context['title'] = 'News'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "News", "route" : '','active' : True})
        
        
class LoadNewsDatatable(BaseDatatableView):
    model = News
    order_columns = ['id','title','url_link','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return News.objects.all().order_by('-id')
    
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
                'project_image' : escape(self.request.build_absolute_uri(item.news_image.url)),
                'title'         : escape(item.title),
                'web_link'      : escape(item.url_link),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveNews(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = News.objects.get(id = instance_id)
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
    
    
class NewsCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'News'
        self.template = 'admin/home-page/news/create-or-update-news.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(News, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "News", "route" : reverse('news:news-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} News ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(News, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = News()
                
            if request.FILES.get('image', None) is not None:
                instance.news_image = request.FILES.get('image',None)
                
            instance.title    = request.POST.get('title',None)
            instance.url_link        = request.POST.get('url_link',None)
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
        return redirect('news:news-view.index')


@method_decorator(login_required, name='dispatch')
class DestroyNewsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                News.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)