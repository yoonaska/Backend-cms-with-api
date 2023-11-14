from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^jobs/', include([
        path('get-all-jobs', views.GetAllJobsView.as_view()),
        path('get-jobs', views.JobListingApiView.as_view()),
    ])),
    re_path(r'^jobs/', include([
        path('jobs-application-submission-form', views.JobApplicationFormApplicationApplicationSubmitApiView.as_view()),
        
    ])),
    path('get-career-cv', views.GetCandidateCv.as_view(), name='get-career-cv'),
]
