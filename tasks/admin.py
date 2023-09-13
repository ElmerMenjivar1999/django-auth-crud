from django.contrib import admin
from .models import Task

#creando una clase para poner campos de solo lectura
class taskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.

admin.site.register(Task,taskAdmin)
