from ctypes import Union
from re import I, T
from django.contrib.auth.models import Group, Permission
import logging
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from apps.users.models import Users
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)


# """""""""""""""""""""""""""""""""""""
# CRUDE OPERATIONS OF USERS STARTS HERE
# """"""""""""""""""""""""""""""""""""
class UsersView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/user/users/users.html'
        self.context['title'] = 'Users'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Users", "route" : '','active' : True})


class LoadUsersDatatable(BaseDatatableView):
    model = Users
    order_columns = ['id', 'email', 'username', 'image', 'first_name', 'last_name', 'is_active'] 
    def get_initial_queryset(self):
        global initial_filter 
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            initial_filter = True
            return self.model.objects.filter(is_active=True, is_admin=True)
        elif filter_value == '2':
            initial_filter = True
            return self.model.objects.filter(is_active=False,is_admin=True)
        else:
            initial_filter = False
            return Users.objects.filter(is_admin=True)
    
    def filter_queryset(self, qs):
        if initial_filter == False:
            qs=Users.objects.filter(is_admin=True)
        search = self.request.POST.get('search[value]', None)
        
        if search:
            qs = qs.filter(Q(first_name__istartswith=search))
        return qs
    
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            :   escape(item.id),
                'email'         :   escape(item.email),
                'image'         :   escape(item.image.url),
                'is_active'     :   escape(item.is_active),
                'first_name'    :   escape(item.first_name),
                'last_name'     :   escape(item.last_name),
            })
        return json_data




class ActiveInactiveUsers(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            user_id = request.POST.get('id', None)
            user = Users.objects.get(id = user_id)
            if user_id:
                if user.is_active:
                    user.is_active = False
                    print(user.is_active)
                else:
                    user.is_active =True
                user.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
        except Exception as es:

            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
            

class UserCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.action = "Create"
        self.template = 'admin/user/users/create-or-update.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id', None)
        if id:
            self.context['users'] = get_object_or_404(Users, id=id)
        return render(request, self.template, context=self.context)

    def post(self, request, *args, **kwargs):

        user_id = request.POST.get('user_id', None)
        try:
            if user_id:
                self.action = 'Updated'
                user = get_object_or_404(Users, id=user_id)
            else:
                user = Users()
                
            if request.FILES.__len__() != 0:
                 if request.POST.get('user_image', None) is None:
                   user.image = request.FILES.get('user_image') 
                         
            user.email      = request.POST.get('email')
            if request.POST.get('user_status'):
                user.is_active  = request.POST.get('user_status')
            # user.username   = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name  = request.POST.get('last_name')
            user.phone      = request.POST.get('phone')
            user.password   = make_password(request.POST.get('password'))
            user.is_admin   = True
            user.is_staff   = True
            user.is_verified   = True
            user.save()
            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if user_id is not None:
                return redirect('users:users.update', id=user_id)
            return redirect('users:users.create')
        return redirect('users:users.index')


@method_decorator(login_required, name='dispatch')
class DestroyUsersRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            users_ids = request.POST.getlist('ids[]')
            if users_ids:
                Users.objects.filter(id__in=users_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)



class EmailValidations(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):

        try:
            email = request.POST.get('email')
            if Users.objects.filter(email=email):
                self.response_format["result"] = True
            else:
                self.response_format["result"] = False
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)



# """""""""""""""""""""""""""""""""""""""""""""
# CRUD OPERATIONS OF PERMISSION STARTS HERE 
# """""""""""""""""""""""""""""""""""""""""""""



class PermissionToGroupViews(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/user/permissions_to_group/permission_group_list.html', context=self.context)

class LoadPermissionToGroupDatatable(BaseDatatableView):
    model = Group

    order_columns = ['name', 'perimissions']

    def get_initial_queryset(self, ):
        qs = self.model.objects.all()
        return qs

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__istartswith=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id': escape(item.id),
                'encrypt_id': escape(URLEncryptionDecryption.enc(item.id)),
                'name': escape(item.name),
                'permissions': escape(str(item.permissions.values_list('name', flat=True)).replace("<QuerySet ['",'').replace("']>", '').replace("'",''))
            })
        return json_data


class PermissionToGroupCreateOrUpdate(View):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.context = {}
        self.action = "Create"
        self.context['title'] = 'Group'
        self.template = 'admin/user/permissions_to_group/create-or-update-permissions_to_group.html'

    def get(self, request, *args, **kwargs):

        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.context['group_name'] = get_object_or_404(Group, id=id)
            self.context['permissions_list'] = Group.objects.get(id=id).permissions.all().values_list('name', flat=True)
        self.context['permissions'] = Permission.objects.all()
        return render(request, self.template , context=self.context)

    def post(self, request, *args, **kwargs):
        group_permission_id = request.POST.get('group_permission_id', None)
        try:

            if group_permission_id:
                self.action = 'Updated'
                group = get_object_or_404(Group, id=group_permission_id)
                group.name = request.POST.get('group_obj_name')
                group.save()
                group_obj = Group.objects.get(id=group.id)
                permission_list = Group.objects.get(id=group_permission_id).permissions.all().values_list('id', flat=True)
                permission_update_list = request.POST.getlist('permissions')
                for pl in permission_list:
                    if pl in permission_update_list:
                        pass
                    else:
                        permission_obj = Permission.objects.get(id=pl)
                        group_obj.permissions.remove(permission_obj)

                for pl in permission_update_list:
                    if pl not in permission_list:
                        permission_obj = Permission.objects.get(id=pl)
                        group_obj.permissions.add(permission_obj)
                    else:
                        pass
            else:
                group = Group()
                group.name = request.POST.get('group_obj_name')
                group_obj = group.save()
                group_obj = Group.objects.get(id=group.id)
                permission_list = request.POST.getlist('permissions')
                for permission in permission_list:
                    permission_obj = Permission.objects.get(id=permission)
                    group_obj.permissions.add(permission_obj)
            messages.success(request, f"Data Successfully "+ self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if group_permission_id is not None:
                return redirect('users:permissions_to_group.update', id=URLEncryptionDecryption.dec(int(group_permission_id)))
            return redirect('users:permissions_to_group.create')
        return redirect('users:permission_to_group.view')



@method_decorator(login_required, name='dispatch')
class DestroyPermissionToGroupView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            group_permission_id = request.POST.getlist('ids[]')
            if group_permission_id:
                Group.objects.filter(id__in=group_permission_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)