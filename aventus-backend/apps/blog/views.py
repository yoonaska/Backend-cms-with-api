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
from apps.blog.models import Blog
from apps.subscription.subscription_mail import blog_subscription_mail_send
from aventus.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)
from aventus import settings
import boto3
from django.views.decorators.csrf import csrf_exempt
#______________________________BLOG MANAGEMENT MANAGEMENT______________________________#

class BlogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/blog-management/blog-listing.html'  
        self.context['title'] = 'Blog'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Blog", "route" : '','active' : True})
        
        
class LoadBlogDatatable(BaseDatatableView):
    model = Blog
    order_columns = ['id','blog_image','title','date','is_active'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Blog.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'blog_image'    : escape(self.request.build_absolute_uri(item.blog_image.url)),
                'title'         : escape(item.title),
                'date'          : escape(item.date.date()),
                'is_popular'     : escape(item.is_popular),
                'is_active'     : escape(item.is_active),
            })
        return json_data


class ActiveInactiveBlog(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Blog.objects.get(id = instance_id)
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


class BlogPopularStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Blog.objects.get(id = instance_id)
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

    
class BlogCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Blog'
        self.template = 'admin/home-page/blog-management/create-or-update-blog.html'
        

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Blog, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Blog", "route" : reverse('blog:blog-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Blog".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        form_data = request.POST
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Blog, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Blog()
                
            if request.FILES.get('blog_image', None) is not None:
                instance.blog_image = request.FILES.get('blog_image',None)
            
            instance.title              = request.POST.get('title',None)
            instance.tags              = request.POST.get('tags',None)
            instance.date               = request.POST.get('blog_date',None)
            instance.description        = request.POST.get('description',None)

            if request.FILES.get('og_image', None) is not None:
                instance.og_image       = request.FILES.get('og_image',None)

            instance.meta_title         = request.POST.get('meta_title',None)
            instance.meta_description   = request.POST.get('meta_description',None)
            instance.meta_keyword       = request.POST.get('meta_keyword',None)
            instance.meta_image_title   = request.POST.get('meta_image_title',None)
            instance.created_by         = request.user
            instance.save()
            
            if self.action == 'Create':
                blog_subscription_mail_send(request,instance)
            
            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            self.context['instance'] = form_data
            self.context['err_message'] = f"Something went wrong." + str(e)
            self.context['instance_id'] = instance_id
            
            if instance_id is not None and instance_id != "":
                return render(request, self.template, context=self.context)
            return render(request, self.template, context=self.context)
        return redirect('blog:blog-view.index')


@method_decorator(login_required, name='dispatch')
class DestroyBlogRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Blog.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    

@csrf_exempt
def ckeditor_file_to_server(request):
    
    if request.method == 'POST':
        uploaded_file = request.FILES['upload']
        s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_key = settings.MEDIA_URL + uploaded_file.name
        # Create an S3 client
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME, aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
        try:
            # Upload the file to S3
            s3.upload_fileobj(uploaded_file, s3_bucket_name, s3_key)
            # Generate the S3 URL
            s3_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_key}"

            return JsonResponse({'url': s3_url})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})