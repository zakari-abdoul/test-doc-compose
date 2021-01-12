import uuid
from django.db import models
from domaine.models import Domaine
from django_currentuser.middleware import get_current_authenticated_user
from django.utils.translation import ugettext_lazy as _

# Create your models here.
current = get_current_authenticated_user


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return '/'.join(['images', str('avatar').lower(), filename])

class App(models.Model):
    """
    docstring
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, blank=False, default='')
    lien = models.CharField(max_length=100, blank=False, default='')
    domaines = models.ManyToManyField(Domaine)
    avatar = models.ImageField(_("avatar"), upload_to=upload_path, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True, editable=False)
    # created_by = models.ForeignKey('users.User', null=True, blank=True, related_name='apps_created_by',
    #                                on_delete=models.DO_NOTHING, editable=False, default=get_current_authenticated_user)


    def save(self, *args, **kwargs):
        super(App, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_at']