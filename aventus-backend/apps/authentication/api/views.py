import logging
from apps.users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from aventus.response import ResponseInfo
from apps.authentication.api.serializers import RefreshTokenSerializer, UserRegisterSerializer, LoginSerializer, LogoutSerializer, OTPSerializer, UserRegisterUpdateSerializer
from apps.authentication.api.schemas import FinalRegistrationPostSchema, FinalRegistrationSchema, LoginPostSchema, LoginSchema, RegisterPostSchema, RegisterSchema, UsersSchema, VerifyOTPPostSchema


logger = logging.getLogger(__name__)


class RegisterAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterAPIView, self).__init__(**kwargs)

    serializer_class = RegisterPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            user_data.update({'is_active' : False})
            serializer = UserRegisterSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.save():
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format['status_code'] = status.HTTP_201_CREATED
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = status.HTTP_200_OK
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                data = {'user': {}, 'errors': serializer.errors}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FinalRegistrationAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FinalRegistrationAPIView, self).__init__(**kwargs)

    serializer_class = FinalRegistrationPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            serializer = UserRegisterUpdateSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.update():
                    data = request.data
                    password = data.get('password', '')
                    user_obj = Users.objects.get(pk=data.get('pk', ''))
                    user = auth.authenticate(username=user_obj.email, password=password)
                    if user:
                        refresh = RefreshToken.for_user(user)
                        serializer = FinalRegistrationSchema(user)
                        data = {'user': serializer.data, 'errors': {}, 'token': str(
                            refresh.access_token), 'refresh': str(refresh)}
                        self.response_format['status_code'] = 200
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                    else:
                        self.response_format['status_code'] = 106
                        data = {'user': serializer.data, 'errors': {}, 'token': '', 'refresh': ''}
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = 102
                    data = {'user': {}, 'errors': {},
                            'token': '', 'refresh': ''}
                    self.response_format["data"] = data
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.response_format['status_code'] = 102
                data = {'user': {}, 'errors': serializer.errors,
                        'token': '', 'refresh': ''}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)

        

class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    serializer_class = LoginPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            data = request.data
            email = data.get('email', '')
            password = data.get('password', '')
            
            user = auth.authenticate(username=email, password=password)
            
            if user:
                serializer = LoginSchema(user)

                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    self.response_format["message"] = 'Account Temparary suspended, contact admin'
                    return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    refresh = RefreshToken.for_user(user)
                    data = {'user': serializer.data, 'token': str(
                        refresh.access_token), 'refresh': str(refresh)}
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = 'Invalid credentials'
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            pass
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)



