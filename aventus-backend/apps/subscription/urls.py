from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'subscription'

urlpatterns = [

    re_path(r'^subscription/', include([
        path('', login_required(views.EmailSubscriptionView.as_view()), name='email.subscription.index'),
        path('load-subscripted-data-table', login_required(views.LoadEmailSubscriptionDatatable.as_view()), name='load.email.subscription.datatable'),
        path('destroy_records/', login_required(views.DestroyEmailSubscriptionEnquiryRecordsView.as_view()), name='subscription-enquiry.records.destroy'),

    ])),

    
]