
from drf_yasg.utils import swagger_auto_schema
from apps.home.models import TechStack
from apps.projects.api.schemas import ProjectCaseStudyApiListingApiSchemas, ProjectCaseStudyBannerApiListingApiSchemas, ProjectCaseStudyDetailViewApiListingApiSchemas
from apps.projects.models import ProjectCaseStudy, ProjectCaseStudyBannerImage
from aventus.helpers.paginations import RestPagination
from aventus.helpers.response import ResponseInfo
from rest_framework.generics import GenericAPIView
from rest_framework import filters
from drf_yasg import openapi
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q


class GetAllProjectCaseStudyView(GenericAPIView):
    queryset                    = ProjectCaseStudy.objects.filter(is_active=True).order_by('-id')
    serializer_class            = ProjectCaseStudyApiListingApiSchemas
    details_serializer_class    = ProjectCaseStudyDetailViewApiListingApiSchemas
    pagination_class            = RestPagination
    filter_backends             = [filters.SearchFilter]
    search_fields               = ['project_name', 'domain__title','project_tags','slug','other_technology','front_technology','backend_technology']

    domain_id   = openapi.Parameter('domain_id', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=False, description="Enter Domain id")
    id          = openapi.Parameter('id', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=False, description="Enter id For Detail View")
    service_id  = openapi.Parameter('service_id', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=False, description="Enter service id for filtering")
    project_tags  = openapi.Parameter('project_tags', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=False, description="Tag Search")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Project CaseStudy"],manual_parameters=[domain_id, id, service_id,project_tags])
    
    def get(self, request, *args, **kwargs):
        domain_id       = request.GET.get('domain_id')
        id              = request.GET.get('id')
        service_id      = request.GET.get('service_id')
        project_tags    = request.GET.get('project_tags')
        queryset    = self.filter_queryset(self.get_queryset())
        
        if id:
            queryset = queryset.filter(slug=id)
            if service_id :
                queryset = queryset.filter(service__slug=service_id)
            page = self.paginate_queryset(queryset)
            serializer = self.details_serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        if domain_id:
            queryset = queryset.filter(domain__slug=domain_id)
            
        if service_id:
            queryset = queryset.filter(service__slug=service_id)
            
        if project_tags:
            queryset = queryset.filter(Q(project_tags__icontains=project_tags)|Q(project_name__icontains=project_tags)|(Q(front_technology__icontains=project_tags))|Q(backend_technology__icontains=project_tags)|Q(backend_technology__icontains=project_tags)
                                       |Q(domain__title__icontains=project_tags))
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class ProjectCaseStudyListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ProjectCaseStudyListingApiView, self).__init__(**kwargs)

    serializer_class            = ProjectCaseStudyApiListingApiSchemas
    details_serializer_class    = ProjectCaseStudyDetailViewApiListingApiSchemas
    filter_backends             = [filters.SearchFilter]
    search_fields               = ['project_name', 'domain__title','project_tags','slug','other_technology','front_technology','backend_technology']

    domain_id = openapi.Parameter('domain_id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter Domain id")
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter id For Detail View")
    service_id = openapi.Parameter('service_id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter service id for filtering")
    project_tags  = openapi.Parameter('project_tags', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=False, description="Tag Search")


    @swagger_auto_schema(pagination_class=RestPagination, tags=["Project CaseStudy"], manual_parameters=[domain_id,id,service_id,project_tags])
    def get(self, request, *args, **kwargs):
        queryset        = ProjectCaseStudy.objects.filter(is_active=True).order_by('-id')
        domain_id       = request.GET.get('domain_id', None)
        service_id      = request.GET.get('service_id', None)
        project_tags    = request.GET.get('project_tags')
        
        id = request.GET.get('id', None)
        if id :
            queryset = queryset.filter(slug=id)
            if service_id :
                queryset = queryset.filter(service__slug=service_id)
                
            serializer = self.details_serializer_class(queryset, many=True,context={'request': request})
            self.response_format['status'] = True
            self.response_format['data'] = {'results':serializer.data}
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        if domain_id :
            queryset = queryset.filter(domain__slug=domain_id)
            
        if service_id :
            queryset = queryset.filter(service__slug=service_id)
            
        if project_tags:
            queryset = queryset.filter(Q(project_tags__icontains=project_tags)|Q(project_name__icontains=project_tags)|(Q(front_technology__icontains=project_tags))|Q(backend_technology__icontains=project_tags)|Q(backend_technology__icontains=project_tags)
                                       |Q(domain__title__icontains=project_tags))
            
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
    
"""---------------------------PROJECT CASE STUDY BANNER SECTIONS-----------------------------"""

class GetAllProjectCaseStudyBannerView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllProjectCaseStudyBannerView, self).__init__(**kwargs)
        
    queryset = ProjectCaseStudyBannerImage.objects.filter(is_active=True).order_by('-id')
    serializer_class   = ProjectCaseStudyBannerApiListingApiSchemas
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['project__project_name']

    service_id = openapi.Parameter('service_id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter service id for filtering")
    
    @swagger_auto_schema(pagination_class=RestPagination, tags=["Project CaseStudy Banner"],manual_parameters=[service_id])
    def get(self, request, *args, **kwargs):
        queryset= self.filter_queryset(self.get_queryset())
        service_id      = request.GET.get('service_id', None)
        if service_id :
            queryset = queryset.filter(project__service__slug=service_id)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)


class OurProjectCaseStudyBannerListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(OurProjectCaseStudyBannerListingApiView, self).__init__(**kwargs)

    serializer_class = ProjectCaseStudyBannerApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['project__project_name']

    service_id = openapi.Parameter('service_id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter service id for filtering")
    
    @swagger_auto_schema(tags=["Project CaseStudy Banner"],manual_parameters=[service_id])
    def get(self, request, *args, **kwargs):
        queryset = ProjectCaseStudyBannerImage.objects.filter(is_active=True).order_by('-id')
        service_id      = request.GET.get('service_id', None)
        if service_id :
            queryset = queryset.filter(project__service__slug=service_id)

        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
    
    