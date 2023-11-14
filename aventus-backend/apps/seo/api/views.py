from drf_yasg.utils import swagger_auto_schema
from apps.seo.api.schemas import SeoManagementApiListingApiSchemas
from apps.seo.models import SeoManagement
from aventus.helpers.response import ResponseInfo
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi




class SeoManagementListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SeoManagementListingApiView, self).__init__(**kwargs)

    serializer_class = SeoManagementApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['meta_title', 'meta_image_title']

    seo_page = openapi.Parameter('seo_page', openapi.IN_QUERY,type=openapi.TYPE_STRING, required=True,description="'Home''Blog''Services','Contact_Us','Career''About_Us'")

    @swagger_auto_schema(tags=["Seo Management"], manual_parameters=[seo_page])
    def get(self, request, *args, **kwargs):
        seo_page = request.GET.get('seo_page')
        queryset = SeoManagement.objects.filter(is_active=True, seo_page=seo_page).order_by('-id')
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)





