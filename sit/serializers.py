from rest_framework import serializers
from sit.models import Sit


class SitSerializer(serializers.HyperlinkedModelSerializer):
    #created_by = UserSerializer(read_only=True)

    class Meta:
        model = Sit
        fields = ['id', 'libelle', 'create_at', 'modify_at'
                  ]

    def validate_Libelle(self, value):
        qs = Sit.objects.filter(libelle == value)
        if qs.exists():
            raise serializers.ValidationError("Ce site existe déjà")
        return value