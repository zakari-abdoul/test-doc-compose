import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from django_currentuser.middleware import get_current_authenticated_user

from domaine.models import Domaine

current = get_current_authenticated_user


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return '/'.join(['images', str('avatar').lower(), filename])


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("first name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, null=True, blank=True)
    matricule = models.CharField(_("matricule"), max_length=50,  null=True, blank=False)
    domaine = models.ManyToManyField(Domaine)
    username = models.CharField(_("username"), max_length=50, null=True, blank=True, unique=True)
    sit = models.ForeignKey('sit.Sit', related_name='sites', null=True, default=None,
                            on_delete=models.DO_NOTHING, editable=False, blank=True,)
    email = models.EmailField(_("email"), max_length=100, blank=True, unique=True)
    avatar = models.ImageField(_("avatar"), upload_to=upload_path, blank=True, null=True)

    modified_by = models.ForeignKey('users.User', null=True, blank=True, related_name='user_modified_by',
                                    on_delete=models.DO_NOTHING, editable=False, default=get_current_authenticated_user)
    created_by = models.ForeignKey('users.User', null=True, blank=True, related_name='user_created_by',
                                   on_delete=models.DO_NOTHING, editable=False, default=get_current_authenticated_user)
    modified = models.DateTimeField(auto_now=True, editable=False)
    date_joined = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(_('active'), default=True, editable=False)
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['date_joined']

    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    # def save(self, *args, **kwargs):
    #     super(Domaine, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    global current
    if created:
        if current is None:
            User.objects.filter(pk=instance.id).update(created_by=instance.id, modified_by=instance.id)


