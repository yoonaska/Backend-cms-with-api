from django.contrib import admin
from django.urls import path, include, re_path
from . import views


app_name = 'users'


urlpatterns = [
    
    re_path(r'^user/', include([
         path('', views.UsersView.as_view(), name='users.index'),
         path('acitve/', views.ActiveInactiveUsers.as_view(), name="active.or.inactive.user"),
         path('create/',views.UserCreateOrUpdateView.as_view(), name='users.create'),
         path('<int:id>/update/', views.UserCreateOrUpdateView.as_view(), name='users.update'),
         path('load_users_datatable', views.LoadUsersDatatable.as_view(), name='load.users.datatable'),
         path('destroy_records/', views.DestroyUsersRecordsView.as_view(), name='users.records.destroy'),
    ])),


    re_path(r'^permission_to_group', include([
        path('', views.PermissionToGroupViews.as_view(), name='permission_to_group.view'),
        path('load-permission_to_group-datatable', views.LoadPermissionToGroupDatatable.as_view(), name='load.permission_to_group.datatable'),
        path('create/', views.PermissionToGroupCreateOrUpdate.as_view(), name='permissions_to_group.create'),
        path('<str:id>/update/', views.PermissionToGroupCreateOrUpdate.as_view(), name='permissions_to_group.update'),
        path('destroy-permission_to_group-records', views.DestroyPermissionToGroupView.as_view(), name='permission_to_group.records.destroy'),
    ])),
]
