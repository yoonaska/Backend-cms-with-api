from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^contact-us/', include([
        path('contact-us-form-submit', views.ContactUsFormApplicationApplicationSubmitApiView.as_view()),
    ])),
    
    re_path(r'^consultation-enquiry/', include([
        path('consultation-enquiry-form-submit', views.ConsultationEnquiryFormApplicationApplicationSubmitApiView.as_view()),
    ])),
]
