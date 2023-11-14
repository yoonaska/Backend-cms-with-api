import threading
from apps.subscription.models import EmailSubscription
from aventus import settings
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from aventus.helpers.mail_fuction import SendBulkEmailsSend, SendEnquiryEmailsSend

"""------------------------------ NEWS EMAIL SEND ---------------------------------------------"""

key = b'B4VK5NGB?m*Y5(#knHAx^9Jas[*=&g;V'

def encrypt_email(email):
    email_bytes = email.encode('utf-8')
    pad_len = 16 - len(email_bytes) % 16
    padded_email = pad(email_bytes, 16)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_email = cipher.encrypt(padded_email)
    iv = cipher.iv
    ciphertext = iv + encrypted_email
    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt_email(encrypted_email):
    encrypted_email_bytes = base64.b64decode(encrypted_email.encode('utf-8'))
    iv = encrypted_email_bytes[:16]  # Extract IV from ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_email_bytes = cipher.decrypt(encrypted_email_bytes[16:])
    decrypted_email = unpad(decrypted_email_bytes, AES.block_size).decode('utf-8')
    return decrypted_email



def blog_subscription_mail_send(request,instance):
    user_emails = [subscription.email for subscription in EmailSubscription.objects.all()]
    encrypted_emails = [encrypt_email(email) for email in user_emails]
    email_map = dict(zip(user_emails, encrypted_emails))
    
    subject = instance.title
    context = {
        "blog_id":instance.slug,
        "blog_title":instance.title,
        "blog_image":request.build_absolute_uri(instance.blog_image.url),
        "email":user_emails,
        "detail_view_path":settings.BLOG_DETAILS_VIEW_PATH,
        "email_map":email_map,
        'domain':settings.EMAIL_DOMAIN,
        'unsubscription':settings.UNSUBSCRIPTION_PATH,
        'protocol': 'https',
    }
    send_email = SendBulkEmailsSend()
    x = threading.Thread(target= send_email.sendBulkEmailSend, args=(subject, request, context, 'admin/home-page/email-templates/subscription/news-subscription/blog-subscription/blog.html',settings.EMAIL_HOST_USER,user_emails,email_map))
    x.start()



"""------------------------------ SUBSCRIPTION SUCCESS EMAIL ---------------------------------------------"""

def subscription_success_mail_send(request,instance):
        subject = "🎉 Welcome to the Club!"
        email = [instance.email]
        context = {
            
            "email":instance.email,
            'domain':settings.EMAIL_DOMAIN,
            'protocol': 'http',
        }

        send_email = SendEnquiryEmailsSend()
        mail_sending=threading.Thread(target=send_email.sendEnquiryEmailSend, args=(subject, request, context, 'admin/home-page/email-templates/subscription/subscription-sucess.html',settings.EMAIL_HOST_USER, email))
        mail_sending.start()



    

    
