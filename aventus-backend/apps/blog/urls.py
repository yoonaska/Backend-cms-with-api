from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [

    re_path(r'^blog/', include([
        path('', login_required(views.BlogView.as_view()), name='blog-view.index'),
        path('load_blog_datatable', login_required(views.LoadBlogDatatable.as_view()), name='load.blog.datatable'),
        path('active/', login_required(views.ActiveInactiveBlog.as_view()), name="active.or.inactive.blog"),
        path('popular/', login_required(views.BlogPopularStatusChange.as_view()), name="popular.blog"),
        path('create/',login_required(views.BlogCreateOrUpdateView.as_view()), name='blog.create'),
        path('<str:id>/update/', login_required(views.BlogCreateOrUpdateView.as_view()), name='blog.update'),
        path('destroy_records/', login_required(views.DestroyBlogRecordsView.as_view()), name='blog.records.destroy'),
        
        path("ckeditor-file-to-server/", views.ckeditor_file_to_server, name="ckeditor_file_to_server"),
    ])),
    
]
