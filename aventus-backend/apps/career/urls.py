from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'career'

urlpatterns = [

    re_path(r'^career/', include([
        path('', login_required(views.JobVacancyView.as_view()), name='job.vacancy.view.index'),
        path('load_job_category_datatable', login_required(views.LoadJobVacancyDatatable.as_view()), name='load.job.vacancy.datatable'),
        path('active/', login_required(views.ActiveInactiveJobVacancy.as_view()), name="active.or.inactive.job.vacancy"),
        path('create/',login_required(views.JobVacancyCreateOrUpdateView.as_view()), name='job.vacancy.create'),
        path('<str:id>/update/', login_required(views.JobVacancyCreateOrUpdateView.as_view()), name='job.vacancy.update'),
        path('destroy_records/', login_required(views.DestroyJobVacancyRecordsView.as_view()), name='job.vacancy.records.destroy'),
    ])),
    
    re_path(r'^why-aventus/', include([
        path('', login_required(views.WhyAventusView.as_view()), name='why.aventus.view.index'),
        path('load_job_category_datatable', login_required(views.LoadWhyAventusDatatable.as_view()), name='why.aventus.datatable'),
        path('active/', login_required(views.ActiveInactiveWhyAventus.as_view()), name="active.or.inactive.why.aventus"),
        path('create/',login_required(views.WhyAvenytusCreateOrUpdateView.as_view()), name='why.aventus.create'),
        path('<str:id>/update/', login_required(views.WhyAvenytusCreateOrUpdateView.as_view()), name='why.aventus.update'),
        path('destroy_records/', login_required(views.DestroyWhyAventusRecordsView.as_view()), name='why.aventus.records.destroy'),
    ])),
    
    re_path(r'^job-application/', include([
        path('', login_required(views.JobApplicationView.as_view()), name='job-application.view.index'),
        path('load_job_applications_datatable', login_required(views.LoadJobApplicationDatatable.as_view()), name='job-application.datatable'),
        path('<str:id>/detail-view/', login_required(views.JobApplicationDetailViewView.as_view()), name='job-application.detail-view'),
        path('destroy_records/', login_required(views.DestroyJobApplicationRecordsView.as_view()), name='job-application.records.destroy'),
    ])),
    
]