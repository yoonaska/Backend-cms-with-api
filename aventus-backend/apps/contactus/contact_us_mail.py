import threading
from aventus import settings
from aventus.helpers.mail_fuction import SendEnquiryEmailsSend


def contact_us_fom_submits_mail_send(request,instance):
    try:
        admin_email = [settings.ADMIN_MAIL]
        subject = "New Service Enquiry From " + (instance.name)
        context = {
            'service'               : instance.service,
            'name'                  : instance.name,
            'email'                 : instance.email,
            'phone_number'          : instance.phone_number,
            'company_name'          : instance.company_name,
            'how_did_you_find_us'   : instance.how_did_you_find_us,
            'other_message'         : instance.other_message,
            'message'               : instance.message,
            'domain'                : settings.EMAIL_DOMAIN,
            'protocol'              : 'https',
        }
        
        send_email = SendEnquiryEmailsSend()
        x = threading.Thread(target=send_email.sendEnquiryEmailSend, args=(subject, request, context, 'admin/home-page/email-templates/contact-us/contact-us-mail.html', settings.EMAIL_HOST_USER, admin_email))
        x.start()
    except Exception as es:
        pass
    
    
def consultation_enquiry_form_submits_mail_send(request,instance):
        try:
            admin_email = [settings.ADMIN_MAIL]
            subject = "Consultation Enquiry " 
            context = {
                'email'         : instance.email,
                'department'    : instance.department,
                'domain'        : settings.EMAIL_DOMAIN,
                'protocol'      : 'https',
            }
            
            send_email = SendEnquiryEmailsSend()
            x = threading.Thread(target=send_email.sendEnquiryEmailSend, args=(subject, request, context, 'admin/home-page/email-templates/get-a-consultation-email/consultation-email-template.html', settings.EMAIL_HOST_USER, admin_email))
            x.start()
        except Exception as es:
            pass
        
"""FOR CUSTOMER"""
        
def Success_mail_for_Customer(request,instance):
        try:
            admin_email = instance.email,
            subject = "Consider IT solved now that you have reached out to us" 
            context = {
                'email'         : instance.email,
                'domain'        : settings.EMAIL_DOMAIN,
                'protocol'      : 'https',
            }
            
            send_email = SendEnquiryEmailsSend()
            x = threading.Thread(target=send_email.Success_mail_for_Customer, args=(subject, request, context, 'admin/home-page/email-templates/enquiry-sucess-mail-customer/enquiry_sucess_mail.html', settings.EMAIL_HOST_USER, admin_email))
            x.start()
        except Exception as es:
            pass