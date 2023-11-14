from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^seo-management/', include([
        path('get-all-seo-management', views.SeoManagementListingApiView.as_view()),
    ])),
]
