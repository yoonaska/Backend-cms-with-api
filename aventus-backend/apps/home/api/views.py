
import itertools
from drf_yasg.utils import swagger_auto_schema
from apps.blog.api.schemas import  BlogApiListingApiSchemas
from apps.blog.models import Blog
from apps.career.api.schemas import JobApiListingApiSchemas
from apps.career.models import JobVacancy
from apps.home.api.schemas import ComPanyProfilePdfListingApiSchemas, DepartmentsChoiceApiListingApiSchemas, OurClientsApiListingApiSchemas, OurProjectsApiListingApiSchemas, OurServiceApiListingApiSchemas, OurServiceChoiceApiListingApiSchemas, ProjectDomainChoiceApiListingApiSchemas
from apps.home.models import CompanyProfilePdf, Department, OurClients, OurProjects, OurServices, ProjectDomain
from apps.projects.api.schemas import ProjectCaseStudyApiListingApiSchemas
from apps.projects.models import ProjectCaseStudy
from aventus.helpers.paginations import RestPagination
from aventus.helpers.response import ResponseInfo
from rest_framework.generics import GenericAPIView
from rest_framework import filters
from drf_yasg import openapi
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
"""-----------------------------OUR PROJECT----------------------------------"""

class GetAllOurProjectView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllOurProjectView, self).__init__(**kwargs)
        
    queryset = OurProjects.objects.filter(is_active=True).order_by('order')
    serializer_class   = OurProjectsApiListingApiSchemas
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                    type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Our Projects"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        queryset= self.filter_queryset(self.get_queryset())
        if id is not None and id:
            queryset = queryset.filter(pk=id)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)



class OurProjectsListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(OurProjectsListingApiView, self).__init__(**kwargs)

    serializer_class = OurProjectsApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Our Projects"])
    def get(self, request, *args, **kwargs):
        queryset = OurProjects.objects.filter(is_active=True).order_by('order')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)


"""------------------OUR SERVICE-------------------------------"""

class GetAllOurServiceView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllOurServiceView, self).__init__(**kwargs)
        
    serializer_class = OurServiceApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    is_both = openapi.Parameter('is_both', openapi.IN_QUERY,
                                    type=openapi.TYPE_BOOLEAN, required=False, description="Enter is_both")
    
    is_sub = openapi.Parameter('is_sub', openapi.IN_QUERY,
                                    type=openapi.TYPE_BOOLEAN, required=False, description="Enter is_sub")
    
    is_main = openapi.Parameter('is_main', openapi.IN_QUERY,
                                    type=openapi.TYPE_BOOLEAN, required=False, description="Enter is_main")
    
    @swagger_auto_schema(tags=["Our Service"],manual_parameters=[is_both,is_sub,is_main])
    def get(self, request, *args, **kwargs):
        is_both = request.GET.get('is_both', None)
        is_sub = request.GET.get('is_sub', None)
        is_main = request.GET.get('is_main', None)

        queryset = OurServices.objects.filter(is_active=True).order_by('order')

        if is_both == "true":
            queryset = queryset.filter(is_both=True)
        if is_sub == "true":
            queryset = queryset.filter(is_sub=True)
        if is_main == "true":
            queryset = queryset.filter(is_main=True)

        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)


class OurServiceListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(OurServiceListingApiView, self).__init__(**kwargs)

    serializer_class = OurServiceChoiceApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Our Service"])
    def get(self, request, *args, **kwargs):
        queryset = OurServices.objects.filter(is_active=True).order_by('order')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
"""------------------OUR CLIENTS-------------------------------"""

class GetAllOurClientsView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllOurClientsView, self).__init__(**kwargs)
        
    queryset = OurClients.objects.filter(is_active=True).order_by('order')
    serializer_class   = OurClientsApiListingApiSchemas
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                    type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Our Clients"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        queryset= self.filter_queryset(self.get_queryset())
        if id is not None and id:
            queryset = queryset.filter(pk=id)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)


class OurClientsListingResponseApi(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(OurClientsListingResponseApi, self).__init__(**kwargs)

    serializer_class = OurClientsApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Our Clients"])
    def get(self, request, *args, **kwargs):
        queryset = OurClients.objects.filter(is_active=True).order_by('order')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
    
"""---------------------DEPARTMENTS---------------------------------------"""

class DepartmentsChoiceListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DepartmentsChoiceListingApiView, self).__init__(**kwargs)

    serializer_class = DepartmentsChoiceApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Departments"])
    def get(self, request, *args, **kwargs):
        queryset = Department.objects.filter(is_active=True).order_by('order')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
    
"""---------------------PROJECT DOMAIN---------------------------------------"""

class ProjectDomainChoiceListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ProjectDomainChoiceListingApiView, self).__init__(**kwargs)

    serializer_class = ProjectDomainChoiceApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Project Domain"])
    def get(self, request, *args, **kwargs):
        queryset = ProjectDomain.objects.filter(is_active=True).order_by('-id')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
    
    """------------------COMPANY PROFILE PDF---------------------------"""


class ComPanyProfilePdfListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ComPanyProfilePdfListingApiView, self).__init__(**kwargs)

    serializer_class = ComPanyProfilePdfListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Company Profile Pdf"])
    def get(self, request, *args, **kwargs):
        queryset = CompanyProfilePdf.objects.filter(is_active=True).order_by('-id')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    

"""=========================== GLOBAL SEARCH API VIEW ==========================================="""

   
class GlobalSearchApiPaginatedView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GlobalSearchApiPaginatedView, self).__init__(**kwargs)
        
    queryset                = Blog.objects.filter(is_active=True).order_by('-id')
    project_queryset        = ProjectCaseStudy.objects.filter(is_active=True).order_by('-id')
    blo_serializer_class    = BlogApiListingApiSchemas
    pro_serializer_class    = ProjectCaseStudyApiListingApiSchemas
    job_serializer_class    = JobApiListingApiSchemas
    pagination_class        = RestPagination

    search_key = openapi.Parameter('search_key', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=True, description="Enter the Title")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Global Search"], manual_parameters=[search_key])
    def get(self, request, *args, **kwargs):
        search_key = request.GET.get('search_key', None)
        
        if not search_key:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status": False,
                "errors": {"search_key": ["The 'search_key' field is required."]}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        blog_queryset       = self.filter_queryset(self.get_queryset())
        project_queryset    = ProjectCaseStudy.objects.filter(Q(project_tags__icontains=search_key),is_active=True)
        blog_querysets       = Blog.objects.filter(Q(tags__icontains=search_key)|Q(title__icontains=search_key),is_active=True)
        job_queryset        = JobVacancy.objects.filter(Q(tags__icontains=search_key)|Q(designation__icontains=search_key),is_active=True)

        blog_querysets       = self.blo_serializer_class(blog_querysets,many=True, context={'request': request, 'blog_queryset': blog_queryset})
        project_queryset    = self.pro_serializer_class(project_queryset,many=True, context={'request': request, 'project_queryset': project_queryset})
        job_queryset        = self.job_serializer_class(job_queryset,many=True, context={'request': request})
        
        combined_data = list(itertools.chain(blog_querysets.data, project_queryset.data,job_queryset.data))
        
        paginator = RestPagination()

      
        paginated_combined_data = paginator.paginate_queryset(combined_data, request)
        paginated_response = paginator.get_paginated_response(paginated_combined_data)

        return paginated_response



class GlobalSearchApiView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GlobalSearchApiView, self).__init__(**kwargs)
        
    queryset                = Blog.objects.filter(is_active=True).order_by('-id')
    project_queryset        = ProjectCaseStudy.objects.filter(is_active=True).order_by('-id')
    blo_serializer_class    = BlogApiListingApiSchemas
    pro_serializer_class    = ProjectCaseStudyApiListingApiSchemas
    job_serializer_class    = JobApiListingApiSchemas
    pagination_class        = RestPagination

    search_key = openapi.Parameter('search_key', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=True, description="Enter the Title")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Global Search"], manual_parameters=[search_key])
    def get(self, request, *args, **kwargs):
        search_key = request.GET.get('search_key', None)
        
        if not search_key:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status": False,
                "errors": {"search_key": ["The 'search_key' field is required."]}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        blog_queryset = self.filter_queryset(self.get_queryset())
        project_queryset = ProjectCaseStudy.objects.filter(Q(project_name__icontains=search_key)|Q(slug__icontains=search_key)|Q(project_tags__icontains=search_key)|Q(service__slug__icontains=search_key)|Q(service__title__icontains=search_key)|Q(domain__title__icontains=search_key)|Q(domain__slug__icontains=search_key))
        blog_queryset = blog_queryset.filter(Q(title__icontains=search_key)|Q(slug__icontains=search_key)|Q(description__icontains=search_key)|Q(tags__icontains=search_key))
        job_queryset        = JobVacancy.objects.filter(Q(tags__icontains=search_key)|Q(designation__icontains=search_key))


        page = self.paginate_queryset(blog_queryset)
        project_page = self.paginate_queryset(project_queryset)
        job_page = self.paginate_queryset(job_queryset)

        response = {
            'blog_queryset': self.blo_serializer_class(page, many=True, context={'request': request, 'blog_queryset': blog_queryset}).data,
            'project_queryset': self.pro_serializer_class(project_page, many=True, context={'request': request, 'project_queryset': project_page}).data,
            'job_queryset': self.job_serializer_class(job_page, many=True, context={'request': request}).data,
        }
        return self.get_paginated_response(response)
