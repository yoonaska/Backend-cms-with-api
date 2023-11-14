from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'seo'

urlpatterns = [

    re_path(r'^seo-management/', include([
        path('', login_required(views.SeoManagementView.as_view()), name='seo-management-view.index'),
        path('load_seo-management_datatable', login_required(views.LoadSeoManagementDatatable.as_view()), name='load.seo-management.datatable'),
        path('active/', login_required(views.ActiveInactiveSeoManagement.as_view()), name="active.or.inactive.seo-management"),
        path('create/',login_required(views.SeoManagementCreateOrUpdateView.as_view()), name='seo.management.create'),
        path('<str:id>/update/', login_required(views.SeoManagementCreateOrUpdateView.as_view()), name='seo.management.update'),
        path('destroy_records/', login_required(views.DestroySeoManagementRecordsView.as_view()), name='seo-management.records.destroy'),
    ])),
    
]