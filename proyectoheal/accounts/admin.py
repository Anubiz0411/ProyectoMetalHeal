# accounts/admin.py

from django.contrib.auth.admin import admin
from .models import *



admin.site.register(AdminProfile)

admin.site.register(EpsProfile)

class EspecialistaAdmin(admin.ModelAdmin):
	 list_display = ('username', 'first_name', 'last_name', 'especialidad', 'email')

admin.site.register(EspecialistaProfile, EspecialistaAdmin)

class MedicalAdmin(admin.ModelAdmin):
	 list_display = ('username', 'first_name', 'last_name', 'email')

admin.site.register(MedicalProfile, MedicalAdmin)

class PatientAdmin(admin.ModelAdmin):
	 list_display = ('username', 'first_name', 'last_name', 'email')

admin.site.register(PatientProfile, PatientAdmin)
