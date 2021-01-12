from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import App
from users.serializers import UserSerializer



class AppDomainesSerializer(serializers.Serializer):
    domaines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

class AppDomaineSerializer(serializers.Serializer):
    domaine = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

class AppSerializer(serializers.HyperlinkedModelSerializer):
    #created_by = UserSerializer(read_only=True)
    domaines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = App
        fields = ['id', 'nom', 'lien', 'domaines','avatar', 'create_at',
                  'modify_at',  #'created_by'
                  ]
    """
    def validate_other_schmeNm(self, value):
        qs = Partenaire.objects.filter(other_schmeNm==value)
        if qs.exists():
            raise serializers.ValidationError("Ce partenaire existe déjà")
        return value"""