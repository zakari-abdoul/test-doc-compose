from rest_framework import serializers
from domaine.models import Domaine
from users.serializers import UserSerializer


class DomaineSerializer(serializers.HyperlinkedModelSerializer):
    #create_by = UserSerializer(read_only=True)

    class Meta:
        model = Domaine
        fields = ['id', 'libelle', 'create_at', 'modify_at']

    def validate_Libelle(self, value):
        qs = Domaine.objects.filter(libelle == value)
        if qs.exists():
            raise serializers.ValidationError("Ce libelle existe déjà")
        return value