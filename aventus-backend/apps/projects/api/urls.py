from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^projects/', include([
        path('get-all-project-case-study', views.GetAllProjectCaseStudyView.as_view()),
        path('get-project-case-study', views.ProjectCaseStudyListingApiView.as_view()),
    ])),
    
    re_path(r'^projects-banner/', include([
        path('get-all-project-case-study-banner', views.GetAllProjectCaseStudyBannerView.as_view()),
        path('get-project-case-study-banner', views.OurProjectCaseStudyBannerListingApiView.as_view()),
    ])),
]
