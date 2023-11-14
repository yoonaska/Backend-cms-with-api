from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'home'

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name= 'dashboard'),
    

    re_path(r'^our-projects/', include([
        path('', login_required(views.OurProjectsView.as_view()), name='our.project-view.index'),
        path('load_our-project_datatable', login_required(views.LoadOurProjectDatatable.as_view()), name='load.our.project.datatable'),
        path('active/', login_required(views.ActiveInactiveOurProjects.as_view()), name="active.or.inactive.our-projects"),
        path('create/',login_required(views.OurProjectCreateOrUpdateView.as_view()), name='our.projects.create'),
        path('<str:id>/update/', login_required(views.OurProjectCreateOrUpdateView.as_view()), name='our.projects.update'),
        path('destroy_records/', login_required(views.DestroyOurProjectsRecordsView.as_view()), name='our.projects.records.destroy'),
        
        #MUTLTIPLE IMAGE MANAGEMENT SECTION #
        path('campaign-image-upload', login_required(views.CampaignImageUploadView.as_view()), name='our.approach.image.upload'),
        path('destroy-temporary-image-upload', login_required(views.TemporaryImageDestroyView.as_view()), name='temporary.image.destroy'),
        path('get-campaign-images', views.GetCampaignImages.as_view(), name='get.our.approach.images'),
    ])),
    
    re_path(r'^our-services/', include([
        path('', login_required(views.OurServicesView.as_view()), name='our.services-view.index'),
        path('load_our-services_datatable', login_required(views.LoadOurServicesDatatable.as_view()), name='load.our.services.datatable'),
        path('active/', login_required(views.ActiveInactiveOurServices.as_view()), name="active.or.inactive.our.services"),
        path('popular/', login_required(views.PopularOrNonPopularOurServices.as_view()), name="popular.or.non-popular.our.services"),
        path('create/',login_required(views.OurServicesCreateOrUpdateView.as_view()), name='our.services.create'),
        path('<str:id>/update/', login_required(views.OurServicesCreateOrUpdateView.as_view()), name='our.services.update'),
        path('destroy_records/', login_required(views.DestroyOurServicesRecordsView.as_view()), name='our.services.records.destroy'),

        ##
        path('validation-our-services-case-study',login_required(views.OurServiceDuplicateUrlValidation.as_view()), name='validation.our.services-case-study'),
        path('is-main/', login_required(views.NavBarMainOurServices.as_view()), name="is_main.or.non-is_main.our.services"),

    ])),
    
    re_path(r'^department/', include([
        path('', login_required(views.DepartmentView.as_view()), name='department-view.index'),
        path('load_department_datatable', login_required(views.LoadDepartmentDatatable.as_view()), name='load.department.datatable'),
        path('active/', login_required(views.ActiveInactiveDepartment.as_view()), name="active.or.inactive.department"),
        path('create/',login_required(views.DepartmentCreateOrUpdateView.as_view()), name='department.create'),
        path('<str:id>/update/', login_required(views.DepartmentCreateOrUpdateView.as_view()), name='department.update'),
        path('destroy_records/', login_required(views.DestroyDepartmentRecordsView.as_view()), name='department.records.destroy'),
    ])),

    re_path(r'^our-clients/', include([
        path('', login_required(views.OurClientsView.as_view()), name='our.clients-view.index'),
        path('load_our-clients_datatable', login_required(views.LoadOurClientsDatatable.as_view()), name='load.our.clients.datatable'),
        path('active/', login_required(views.ActiveInactiveOurClients.as_view()), name="active.or.inactive.our-clients"),
        path('create/',login_required(views.OurClientsCreateOrUpdateView.as_view()), name='our.clients.create'),
        path('<str:id>/update/', login_required(views.OurClientsCreateOrUpdateView.as_view()), name='our.clients.update'),
        path('destroy_records/', login_required(views.DestroyOurClientsRecordsView.as_view()), name='our.clients.records.destroy'),
        
        path('update_client-image/', login_required(views.OurClientsImageUploadingView.as_view()), name='update_image_order'),
        path('delete_client-image/', login_required(views.DestroyOurClientsOrderRecordsView.as_view()), name='delete_image_order'),
        
    ])),
    
    re_path(r'^domain/', include([
        path('', login_required(views.ProjectDomainView.as_view()), name='domain-view.index'),
        path('load_domain_datatable', login_required(views.ProjectDomainDatatable.as_view()), name='load.domain.datatable'),
        path('active/', login_required(views.ActiveInactiveProjectDomain.as_view()), name="active.or.inactive.domain"),
        path('create/',login_required(views.ProjectDomainCreateOrUpdateView.as_view()), name='domain.create'),
        path('<str:id>/update/', login_required(views.ProjectDomainCreateOrUpdateView.as_view()), name='domain.update'),
        path('destroy_records/', login_required(views.DestroyProjectDomainRecordsView.as_view()), name='domain.records.destroy'),
    ])),
    
    re_path(r'^project-stack/', include([
        path('', login_required(views.ProjectStackView.as_view()), name='stack-view.index'),
        path('load_stack_datatable', login_required(views.ProjectStackDatatable.as_view()), name='load.stack.datatable'),
        path('active/', login_required(views.ActiveInactiveProjectStack.as_view()), name="active.or.inactive.stack"),
        path('create/',login_required(views.ProjectStackCreateOrUpdateView.as_view()), name='stack.create'),
        path('<str:id>/update/', login_required(views.ProjectStackCreateOrUpdateView.as_view()), name='stack.update'),
        path('destroy_records/', login_required(views.DestroyProjectStackRecordsView.as_view()), name='stack.records.destroy'),
    ])),
    
    re_path(r'^download-factsheet/', include([
        path('', views.FactsheetView.as_view(), name='factsheet.index'),
        path('load-factsheet', views.FactsheetDatatable.as_view(), name='load.factsheet.datatable'),
        path('create/',views.FactsheetCreateOrUpdateView.as_view(), name='factsheet.create'),  
        path('<str:id>/update/', views.FactsheetCreateOrUpdateView.as_view(), name='factsheet.update'),
        path('destroy_records/', views.DestroyFactsheetRecordsView.as_view(), name='factsheet.destroy'),
        path('active/', views.ActiveInactiveFactsheet.as_view(), name="active.or.inactive.factsheet"),
    ])),
    
]
