from django.contrib import admin

# Register your models here.
from sit.models import Sit

class SitAdmin(admin.ModelAdmin):
    #fields = ('first_name', 'last_name', 'matricule', 'username', 'email')
    list_display = ['libelle']


admin.site.register(Sit, SitAdmin)

