from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'news'

urlpatterns = [

    re_path(r'^news/', include([
        path('', login_required(views.NewsView.as_view()), name='news-view.index'),
        path('load_news_datatable', login_required(views.LoadNewsDatatable.as_view()), name='load.news.datatable'),
        path('active/', login_required(views.ActiveInactiveNews.as_view()), name="active.or.inactive.news"),
        path('create/',login_required(views.NewsCreateOrUpdateView.as_view()), name='news.create'),
        path('<str:id>/update/', login_required(views.NewsCreateOrUpdateView.as_view()), name='news.update'),
        path('destroy_records/', login_required(views.DestroyNewsRecordsView.as_view()), name='news.records.destroy'),
    ])),
    
]