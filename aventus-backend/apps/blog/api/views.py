
from drf_yasg.utils import swagger_auto_schema
from apps.blog.api.schemas import BlogApiDerailsListingApiSchemas, BlogApiListingApiSchemas
from apps.blog.models import Blog
from aventus.helpers.paginations import RestPagination
from aventus.helpers.response import ResponseInfo
from rest_framework.generics import GenericAPIView
from rest_framework import filters
from drf_yasg import openapi
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response



class GetAllBlogView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllBlogView, self).__init__(**kwargs)
        
    queryset                        = Blog.objects.filter(is_active=True).order_by('-id')
    serializer_class                = BlogApiDerailsListingApiSchemas
    blog_details_serializer_class   = BlogApiDerailsListingApiSchemas
    pagination_class                = RestPagination
    filter_backends                 = [filters.SearchFilter]
    search_fields                   = ['title']
    
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter id")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Blog"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        queryset= self.filter_queryset(self.get_queryset())
        if id is not None and id:
            queryset = queryset.filter(slug=id)
            page = self.paginate_queryset(queryset)
            serializer = self.blog_details_serializer_class(page, many=True,context={'request': request})
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)


class GetBlogListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetBlogListingApiView, self).__init__(**kwargs)

    serializer_class = BlogApiDerailsListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Blog"])
    def get(self, request, *args, **kwargs):
        queryset = Blog.objects.filter(is_active=True).order_by('-id')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)


class PopularBlogListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PopularBlogListingApiView, self).__init__(**kwargs)

    serializer_class = BlogApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(tags=["Blog"])
    def get(self, request, *args, **kwargs):
        queryset = Blog.objects.filter(is_active=True,is_popular=True).order_by('-id')
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
