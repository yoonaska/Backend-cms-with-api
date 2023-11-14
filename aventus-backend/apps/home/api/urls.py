from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^our-projects/', include([
        path('get-all-our-projects', views.GetAllOurProjectView.as_view()),
        path('get-our-projects', views.OurProjectsListingApiView.as_view()),
    ])),
    
    re_path(r'^our-service/', include([
        path('get-all-our-service', views.GetAllOurServiceView.as_view()),
        path('get-our-service-choice', views.OurServiceListingApiView.as_view()),
    ])),
    
    re_path(r'^our-clients/', include([
        path('get-all-our-clients', views.GetAllOurClientsView.as_view()),
        path('get-our-clients', views.OurClientsListingResponseApi.as_view()),
    ])),
    
    re_path(r'^department/', include([
        path('get-our-department-choice', views.DepartmentsChoiceListingApiView.as_view()),
    ])),
    
    re_path(r'^domain/', include([
        path('get-our-domain-choice', views.ProjectDomainChoiceListingApiView.as_view()),
    ])),

    re_path(r'^company-profile/', include([
        path('get-company-profile-pdf', views.ComPanyProfilePdfListingApiView.as_view()),
    ])),

    re_path(r'^global/', include([
        path('get-global-search', views.GlobalSearchApiView.as_view()),
        path('get-global-search-paginated', views.GlobalSearchApiPaginatedView.as_view()),
    ])),
]
