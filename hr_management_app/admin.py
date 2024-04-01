from django.contrib import admin
from . models import AdminHOD,HRs,Employees


@admin.register(AdminHOD)
class AdminHODAdmin(admin.ModelAdmin):
    list_display =['id','admin','created_at','updated_at','objects']


@admin.register(HRs)
class HRAdmin(admin.ModelAdmin):
    list_display =['id','admin','created_at','updated_at','objects']


@admin.register(Employees)
class EmployeeAdmin(admin.ModelAdmin):
    list_display =['id','admin','created_at','updated_at']