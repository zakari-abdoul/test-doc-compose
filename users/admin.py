from django.contrib import admin

# Register your models here.
from django.contrib.auth.hashers import make_password

from users.models import User
from users.views import getActivationMail
from django.contrib.auth.admin import UserAdmin

#UserAdmin.fieldsets += ('Custom fields set', {'fields': ('name', 'contact')}),
class UserAdmin(admin.ModelAdmin):
    #fields = ('first_name', 'last_name', 'matricule', 'username', 'email')
    list_display = ['username', 'first_name', 'last_name']
    exclude = ('username', 'groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        obj.username = obj.matricule+"_"+obj.last_name
        p = obj.password
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
        if 'password' in form.changed_data:
            getActivationMail(obj.email, p, obj.username)


admin.site.register(User, UserAdmin)

admin.site.site_header = "Digidex Administration"
admin.site.title = "DIGIDEX"