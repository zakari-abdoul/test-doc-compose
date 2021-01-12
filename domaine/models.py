import uuid
from django.db import models
from django_currentuser.middleware import get_current_authenticated_user

# Create your models here.
current = get_current_authenticated_user


class Domaine(models.Model):
    """
    Sites model representation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=100, blank=False, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True, editable=False)
    # created_by = models.ForeignKey('users.User', null=True, blank=True, related_name='domaine_created_by',
    #                                on_delete=models.DO_NOTHING, editable=False, default=get_current_authenticated_user)


    def save(self, *args, **kwargs):
        super(Domaine, self).save(*args, **kwargs)

    def __str__(self):
        return ('%s' % (self.libelle))

    class Meta:
        ordering = ['create_at']