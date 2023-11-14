from django.contrib import admin

from apps.career.models import JobVacancy, Responsibilities, Skills,JobApplication

# Register your models here.
admin.site.register(JobVacancy)
admin.site.register(Skills)
admin.site.register(Responsibilities)
admin.site.register(JobApplication)
