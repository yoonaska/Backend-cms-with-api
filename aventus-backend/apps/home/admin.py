from django.contrib import admin
from apps.home.models import OurProjects, OurProjectsImages,OurServices,Department,OurClients, TechStack

admin.site.register(OurProjects)
admin.site.register(OurServices)
admin.site.register(Department)
admin.site.register(OurProjectsImages)
admin.site.register(TechStack)


class OurClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'order')  # Add any other fields you want to search by
    ordering = ('order',)  # This line specifies the ordering by 'order' field

admin.site.register(OurClients, OurClientsAdmin)