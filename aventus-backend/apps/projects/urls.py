from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'projects'

urlpatterns = [

        re_path(r'^project-case-study/', include([
            path('project-case-study-listing', login_required(views.ProjectCaseStudyView.as_view()), name='project-case-study.listing'),
            path('load-project-case-study-listing-datatable',login_required(views.LoadProjectCaseStudyDatatable.as_view()), name='load.project-case-study.datatable'),
            path('create-project-case-study',login_required(views.CreateOrUpdateProjectCaseStudySection.as_view()), name='create.project-case-study'),
            path('<str:id>/update-project-case',login_required(views.CreateOrUpdateProjectCaseStudySection.as_view()), name='update.project-case-study'),
            path('destroy-project-case-study',login_required(views.DestroyProjectCaseStudyRecordsView.as_view()), name='destroy.project-case-study'),
            path('validation-project-case-study',login_required(views.ProjectCaseStudyDuplicateUrlValidation.as_view()), name='validation.project-case-study'),
            path('change-status-project-case-study',login_required(views.ActiveInactiveProjectCaseStudys.as_view()), name='active.inactive.project-case-study'),
            
            path('project-case-study-image-upload', login_required(views.ProjectCaseStudyImageImageUploadView.as_view()), name='project-case-study.image.upload'),
            path('destroy-temporary-image-upload', login_required(views.TemporaryImageDestroyView.as_view()), name='temporary.image.destroy'),
            path('get-project-case-study-images', views.GetProjectCaseStudyImages.as_view(), name='get.project-case-study.images'),
            
            path('duplicate-project-case-study',login_required(views.DuplicateProjectCaseStudyRecordsView.as_view()), name='duplicate.project-case-study'),

    ])),

        re_path(r'^project-case-study-banner/',include([
            path('project-case-study-banner-listing',login_required(views.ProjectCaseStudyBannerView.as_view()),name='project.case.study.banner.listing'),
            path('load-project-case-study-banner',login_required(views.LoadProjectCaseStudyBannerDatatable.as_view()),name='load.project.case.study.banner.datatable'),
            path('destroy-project-case-study-banner',login_required(views.DestroyProjectCaseStudyBannerRecordsView.as_view()),name='destroy.project.case.study.banner'),
            path('project-case-study-banner-status-change',login_required(views.ActiveInactiveProjectCaseStudyBanner.as_view()),name='active.inactive.project.case.study.banner'),
            path('create-project-case-study-banner',login_required(views.CreateOrUpdateProjectCaseStudyBannerSection.as_view()), name='create.projects.details.banner'),
            path('<str:id>/update-project-case-study-banner',login_required(views.CreateOrUpdateProjectCaseStudyBannerSection.as_view()), name='update.projects.details.banner'),
            
            # MULTIPLE IMAGE
            path('project-case-study-banner-image-upload', login_required(views.ProjectCaseStudyBannerImageImageUploadView.as_view()), name='project-case-study-banner.image.upload'),
            path('destroy-temporary-image-upload', login_required(views.ProjectCaseStudyBannerTemporaryImageDestroyView.as_view()), name='project-case-study-banner-temporary.image.destroy'),
            path('get-project-case-study-images', views.GetProjectCaseStudyBannerImages.as_view(), name='get.project-case-study-banner.images'),
        ]))
    ]