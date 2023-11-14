from rest_framework import serializers
from apps.subscription.models import EmailSubscription
from apps.subscription.subscription_mail import subscription_success_mail_send


#_____________________________EMAIL SUBSCRIPTION MAIL_____________________________#

class SubscribeEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = EmailSubscription
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        check_email = EmailSubscription.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError(
                {'email ': ('Sorry This Email Is Already Registered')})
        return super().validate(attrs)
    
    def create(self, validated_data):
        request = self.context.get('request')
        instance = EmailSubscription()
        instance.email = validated_data.get('email')
        instance.save()
        subscription_success_mail_send(request,instance)
        return instance
    
class UnSubscribeEmailSerializer(serializers.ModelSerializer):
   
    
    class Meta:
        model = EmailSubscription
        fields = ['email']