from django.contrib import admin

# Register your models here.
from domaine.models import Domaine

class DomaineAdmin(admin.ModelAdmin):
    #fields = ('first_name', 'last_name', 'matricule', 'username', 'email')
    list_display = ['libelle']


admin.site.register(Domaine, DomaineAdmin)
