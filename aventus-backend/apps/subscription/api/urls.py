from django.urls import path, include,re_path
from . import views
urlpatterns = [
        
    re_path(r'^email/', include([
        path('create-subscribe-email', views.EmailSubscriptionApi.as_view()),
        path('unsubscribe', views.EmailUnsubscriptionApi.as_view(),name='unsubscribe'),
    ])),
]
