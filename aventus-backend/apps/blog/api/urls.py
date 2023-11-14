from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^blog/', include([
        path('get-all-blog', views.GetAllBlogView.as_view()),
        path('get-blogs', views.GetBlogListingApiView.as_view()),
        path('get-popular-blog', views.PopularBlogListingApiView.as_view()),
    ])),
]
