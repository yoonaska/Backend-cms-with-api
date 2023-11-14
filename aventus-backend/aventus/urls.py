"""root_project_django_v4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from aventus.views import page_not_found_view, custom_500

admin.site.site_header = "AVENTUS INFORMATICS"
admin.site.site_title = "AVENTUS INFORMATICS"

schema_view = get_schema_view(
   openapi.Info(
      title="Aventus Informatics",
      default_version='v1',
      terms_of_service="",
      contact=openapi.Contact(email="sachu@aventusinformatics.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('', include('apps.home.urls')),
    path('contact-us/', include('apps.contactus.urls')),
    path('blog/', include('apps.blog.urls')),
    path('career/', include('apps.career.urls')),
    path('news/', include('apps.news.urls')),
    path('projects/', include('apps.projects.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('seo-management/', include('apps.seo.urls')),

    
    
    
    re_path(r'^api/', include([
        
        # path('auth/', include('apps.authentication.api.urls')),
        path('home/', include('apps.home.api.urls')),
        path('blog/', include('apps.blog.api.urls')),
        path('career/', include('apps.career.api.urls')),
        path('contact-us/', include('apps.contactus.api.urls')),
        path('subscription/', include('apps.subscription.api.urls')),
        path('news/', include('apps.news.api.urls')),
        path('projects/', include('apps.projects.api.urls')),
        path('seo-managements/', include('apps.seo.api.urls')),

    
        re_path(r'^docs/', include([

            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ])),    
    ])),    
    
        
    
]


# if settings.DEBUG == True:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view
handler500 = custom_500
