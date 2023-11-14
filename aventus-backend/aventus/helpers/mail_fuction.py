from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import  get_connection
from aventus import settings



"""-----------------------------------SINGLE MAIL SEND------------------------------------------"""

class SendEnquiryEmailsSend:
    
    def __init__(self, *args, **kwargs):
        pass
    
    def sendEnquiryEmailSend(self, subject, request, context, template, email_host, user_email):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME
        try:
            connection  = get_connection()
            connection.open()
            context = context
            
            image = request.build_absolute_uri("/")
            context['image']                    = str(image)+'media/default/logo/logo.png'
            context['sub_logo_back']            = str(image)+'static/assets/media/images/email-images/logo.png'
            context['header_back_image']        = str(image)+'static/assets/media/images/email-images/bg.png'
            context['sub_footer_back_ground']   = str(image)+'static/assets/media/images/email-images/footer-bg1.png'
            context['sub_head_back_ground']     = str(image)+'static/assets/media/images/email-images/bg.png'
            context['instagram']                = str(image)+'media/default/logo/instagram-icon.png'
            context['youtube']                  = str(image)+'media/default/logo/youtube-round.png'
            context['linkedin']                 = str(image)+'media/default/logo/linkedin-icon.png'
            context['twitter']                  = str(image)+'media/default/logo/x-icon.png'
            context['facebook']                 = str(image)+'media/default/logo/facebook-icon.png'

            html_content = render_to_string(str(template), {'context':context})
            text_content = strip_tags(html_content)
            send_e = EmailMultiAlternatives(subject, text_content, f'{sender_name} <{context["email"]}>', user_email, connection=connection)
            send_e.attach_alternative(html_content, "text/html")
            send_e.send()
            connection.close()
            sending_status = True
        except Exception as es:
            pass
        return sending_status

    def Success_mail_for_Customer(self, subject, request, context, template, email_host, user_email):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME
        try:
            connection  = get_connection()
            connection.open()
            context = context
            
            image = request.build_absolute_uri("/")
            context['image']                    = str(image)+'media/default/logo/logo.png'
            context['sub_logo_back']            = str(image)+'static/assets/media/images/email-images/logo.png'
            context['header_back_image']        = str(image)+'static/assets/media/images/email-images/bg.png'
            context['sub_footer_back_ground']   = str(image)+'static/assets/media/images/email-images/footer-bg1.png'
            context['sub_head_back_ground']     = str(image)+'static/assets/media/images/email-images/bg.png'
            
            context['instagram']                = str(image)+'media/default/logo/instagram-icon.png'
            context['youtube']                  = str(image)+'media/default/logo/youtube-round.png'
            context['linkedin']                 = str(image)+'media/default/logo/linkedin-icon.png'
            context['twitter']                  = str(image)+'media/default/logo/x-icon.png'
            context['facebook']                 = str(image)+'media/default/logo/facebook-icon.png'

            html_content = render_to_string(str(template), {'context':context})
            text_content = strip_tags(html_content)
            send_e = EmailMultiAlternatives(subject, text_content, f'{sender_name} <{context["email"]}>', {context["email"]}, connection=connection)
            send_e.attach_alternative(html_content, "text/html")
            send_e.send()
            connection.close()
            sending_status = True
        except Exception as es:
            pass
        return sending_status
    
    
"""------------------------------ BULK EMAIL SENDING FOR SUBSCRIPTION---------------------------------------------"""


class SendBulkEmailsSend:
    
    def __init__(self, *args, **kwargs):
        pass
    
    
    def sendBulkEmailSend(self, subject, request, context, template, email_host, user_emails,encrypted_emails):

        sender_name = settings.EMAIL_SENDER_NAME
        sending_status = False
        try:
         
            for key,value in encrypted_emails.items():
                connection  = get_connection()
                connection.open()
                context = context  
                context['encrypt_email'] = value  
                image = request.build_absolute_uri("/")
                context['image']                    = str(image)+'media/default/logo/logo.png'
                context['favicon_logo']             = str(image)+'static/assets/media/images/favicon.ico'
                context['header_back_image']        = str(image)+'static/assets/media/images/email-images/bg.png'
                context['sub_logo_back']            = str(image)+'static/assets/media/images/email-images/logo.png'
                context['sub_footer_back_ground']   = str(image)+'static/assets/media/images/email-images/footer-bg1.png'
                context['instagram']                = str(image)+'media/default/logo/instagram-icon.png'
                context['youtube']                  = str(image)+'media/default/logo/youtube-round.png'
                context['linkedin']                 = str(image)+'media/default/logo/linkedin-icon.png'
                context['twitter']                  = str(image)+'media/default/logo/x-icon.png'
                context['facebook']                 = str(image)+'media/default/logo/facebook-icon.png'
                
                html_content = render_to_string(str(template), {'context':context})
                text_content = strip_tags(html_content)
            
                send_e = EmailMultiAlternatives(str(subject), text_content, f'{sender_name} <email_host>', bcc=[key], connection=connection)
                send_e.attach_alternative(html_content, "text/html")
                send_e.send()
                connection.close()
                sending_status = True
        except Exception as es:
            pass
        
        return sending_status

