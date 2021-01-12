from django.contrib import admin

# Register your models here.
from app.models import App

class AppAdmin(admin.ModelAdmin):
    #fields = ('first_name', 'last_name', 'matricule', 'username', 'email')
    list_display = ['nom', 'lien']


admin.site.register(App, AppAdmin)
