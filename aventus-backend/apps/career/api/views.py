
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.career.api.schemas import JobApiListingApiSchemas, JobDetailsApiListingApiSchemas
from apps.career.api.serializer import JobApplicationFormSubmissionRequestSerializer
from apps.career.models import JobApplication, JobVacancy
from aventus.helpers.paginations import RestPagination
from aventus.helpers.response import ResponseInfo
from rest_framework.generics import GenericAPIView
from rest_framework import filters
from drf_yasg import openapi
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from aventus.helpers.custom_messages import _success
from django.views import View


class GetAllJobsView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllJobsView, self).__init__(**kwargs)
        
    queryset = JobVacancy.objects.filter(is_active=True).order_by('-id')
    serializer_class   = JobApiListingApiSchemas
    details_serializer_class = JobDetailsApiListingApiSchemas
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__title']
    
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING, required=False, description="Enter id")

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Job"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        queryset= self.filter_queryset(self.get_queryset())
        if id is not None and id:
            queryset = queryset.filter(slug=id)
            page = self.paginate_queryset(queryset)
            serializer = self.details_serializer_class(page, many=True,context={'request': request})
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)



class JobListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(JobListingApiView, self).__init__(**kwargs)

    serializer_class = JobApiListingApiSchemas
    details_serializer_class = JobDetailsApiListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__title']
    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_STRING, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Job"],manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        queryset = JobVacancy.objects.filter(is_active=True).order_by('-id')
        if id is not None and id:
            queryset = queryset.filter(slug=id)
            serializer = self.details_serializer_class(queryset, many=True,context={'request': request})
            self.response_format['status'] = True
            self.response_format['data'] = {'results':serializer.data}
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = {'results':serializer.data}
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)


"""----------------------------------JOB APPLICATION SUBMISSION -------------------------------------------------"""


class JobApplicationFormApplicationApplicationSubmitApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(JobApplicationFormApplicationApplicationSubmitApiView, self).__init__(**kwargs)

    serializer_class = JobApplicationFormSubmissionRequestSerializer
    @swagger_auto_schema(tags=["Job Application"])
    def post(self, request):
            try:
                data = request.data
                if data is not None and data:
                    serializer = self.serializer_class(
                        data=data, context={'request': request})
                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["status"] = False
                    self.response_format["errors"] = serializer.errors
                    return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.is_valid():
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["status"] = False
                    self.response_format["errors"] = serializer.errors
                    return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                self.response_format['status_code'] = status.HTTP_201_CREATED
                self.response_format["message"] = _success
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_201_CREATED)

            except Exception as e:
                self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                self.response_format['status'] = False
                self.response_format['message'] = str(e)
                return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCandidateCv(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def get(self, request, *args, **kwargs):
        try:
            instance_id = request.GET.get('id')
            if instance_id:
                pdf = get_object_or_404(JobApplication, id=instance_id)
                # Assuming that pdf.cv_pdf is the PDF file field
                if pdf.cv_pdf:
                    response = HttpResponse(pdf.cv_pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'inline; filename="{pdf.cv_pdf.name}"'
                    return response

        except Exception as e:
            ...