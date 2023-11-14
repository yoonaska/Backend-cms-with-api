import threading
from aventus import settings
from aventus.helpers.mail_fuction import SendEnquiryEmailsSend


def job_application_submits_mail_send(request,instance):
    try:
        admin_email = [settings.ADMIN_MAIL]
        subject = "Job Application For"+ instance.designation
        context = {
            'pk'              : instance.pk,
            'name'            : instance.name,
            'email'           : instance.email,
            'job_instance'    : instance.designation,
            'phone_number'    : instance.phone_number,
            'about_yourself'  : instance.about_yourself,
            'portfolio'       : instance.portfolio,
            'cv'              : instance.cv,
            'portfolio_pdf'   : None,
            'cv_pdf'          : None,
            'ratting'         : instance.ratting,
            'detail_view_path': settings.GET_CANDIDATE_CV_PATH,
        }
        if instance.portfolio_pdf:
            context['portfolio_pdf'] = request.build_absolute_uri(instance.portfolio_pdf.url)
        if instance.cv_pdf:
            context['cv_pdf'] = request.build_absolute_uri(instance.cv_pdf.url)

        send_email = SendEnquiryEmailsSend()
        x = threading.Thread(target=send_email.sendEnquiryEmailSend, args=(subject, request, context, 'admin/home-page/email-templates/job-application-mail/job-application-mail.html', settings.EMAIL_HOST_USER, admin_email))
        x.start()
    except Exception as es:
        pass