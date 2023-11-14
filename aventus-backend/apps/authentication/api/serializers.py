from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import Users



class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, min_length=4)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255, min_length=4)
    last_name = serializers.CharField(max_length=255, min_length=2)
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = Users
        fields = ['id','phone', 'email', 'first_name','last_name','is_active']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        email = attrs.get('email', '') 
        
        
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
            
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email address is already in use')})
            
        return super().validate(attrs)

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)




class UserRegisterUpdateSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    password = serializers.CharField(max_length=65, min_length=8)
    username = serializers.CharField(max_length=255, min_length=4)
    confirm_password = serializers.CharField(max_length=65, min_length=8)

    class Meta:
        model = Users
        fields = ('password', 'username','pk')

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', None)
        pk = attrs.get('pk', None)

        if confirm_password != password:
            raise serializers.ValidationError(
                {'password_mismatch': ('password an confirm password are not match')})
        
        
        if not Users.objects.filter(pk=pk).exists():
            raise serializers.ValidationError(
                {'not_found': ('user not found in our system.')})
            
      
        return super().validate(attrs)
    
    

    def update(self):
        pk = self.data.get('pk')
        if pk:
            user = Users.objects.get(pk=pk)
            user.username = self.data.get('username')
            user.set_password(self.data.get('password'))
            user.is_active = True
            user.save()
            return True
        
        return False
        






class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['username', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['otp']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
