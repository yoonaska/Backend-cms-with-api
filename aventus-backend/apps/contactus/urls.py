from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'contact'

urlpatterns = [
     re_path(r'^contact-us-enquiry/', include([
        path('', login_required(views.ContactUsEnquieryView.as_view()), name='contact-us-enquiry.view.index'),
        path('load_contact_us_enquiry_datatable', login_required(views.LoadContactUsEnquieryDatatable.as_view()), name='contact-us-enquiry.datatable'),
        path('<str:id>/detail-view/', login_required(views.ContactUsEnquieryDetailViewView.as_view()), name='contact-us-enquiry.detail-view'),
        path('destroy_records/', login_required(views.DestroyContactUsEnquieryRecordsView.as_view()), name='contact-us-enquiry.records.destroy'),
    ])),

]


