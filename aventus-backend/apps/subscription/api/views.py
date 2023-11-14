
from drf_yasg.utils import swagger_auto_schema
from apps.subscription.api.serializer import SubscribeEmailSerializer, UnSubscribeEmailSerializer
from apps.subscription.models import EmailSubscription
from apps.subscription.subscription_mail import decrypt_email
from aventus.helpers.response import ResponseInfo
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from aventus.helpers.custom_messages import _success



#__________________SUBSCRIBE EMAIL__________________________________#

class EmailSubscriptionApi(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(EmailSubscriptionApi, self).__init__(**kwargs)

    serializer_class = SubscribeEmailSerializer

    @swagger_auto_schema(tags=["Email Subscription"])
    def post(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data, context={'request': request})

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


class EmailUnsubscriptionApi(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(EmailUnsubscriptionApi, self).__init__(**kwargs)

    serializer_class = UnSubscribeEmailSerializer

    @swagger_auto_schema(tags=["Email Subscription"])
    def post(self, request):
 
        try:
         
            email = request.data.get('email')
            email = decrypt_email(email)
            subscription = EmailSubscription.objects.filter(email=email)
            subscription.delete()

            self.response_format["data"] = ""
            self.response_format["message"] = 'You have successfully unsubscribed from our email list.'
            return Response(self.response_format, status=status.HTTP_200_OK)    

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  