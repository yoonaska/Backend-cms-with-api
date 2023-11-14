from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
import threading
import  logging
from aventus import settings
from apps.contactus.api.serializer import ConsultationEnquiryFormSubmissionRequestSerializer, ContactUsFormSubmissionRequestSerializer
from aventus.response import ResponseInfo
logger = logging.getLogger(__name__)
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from aventus.helpers.custom_messages import _success


"""-------------------------CONTACT-US ----------------------------------------"""


class ContactUsFormApplicationApplicationSubmitApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ContactUsFormApplicationApplicationSubmitApiView, self).__init__(**kwargs)

    serializer_class = ContactUsFormSubmissionRequestSerializer
    @swagger_auto_schema(tags=["Contact Us"])
    def post(self, request):
            try:
                data = request.data
                if data is not None and data:
                    serializer = self.serializer_class(data=data, context={'request': request})
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


"""-------------------------CONSULTATION ENQUIRY ----------------------------------------"""

class ConsultationEnquiryFormApplicationApplicationSubmitApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ConsultationEnquiryFormApplicationApplicationSubmitApiView, self).__init__(**kwargs)

    serializer_class = ConsultationEnquiryFormSubmissionRequestSerializer
    @swagger_auto_schema(tags=["Contact Us"])
    def post(self, request):
            try:
                data = request.data
                if data is not None and data:
                    serializer = self.serializer_class(data=data, context={'request': request})
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

