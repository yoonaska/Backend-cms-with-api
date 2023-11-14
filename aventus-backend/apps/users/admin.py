from django.contrib import admin
from apps.users.models import Users
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['id', 'email','first_name','last_name','username','phone']
    list_display_links = ['email']
    
    fieldsets = (
        ("Profile", {'fields': ('email', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin','is_superuser','is_verified','groups','user_permissions')}),
        ('Personal', {
            'fields': ('username','phone',)
            }),
    )

    
    search_fields = ('email', 'first_name','last_name')
    ordering = ('email',)
    filter_horizontal = ()
    
    

admin.site.register(Users,UsersAdmin)
