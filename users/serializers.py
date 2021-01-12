
from django.contrib.auth.models import Group
from rest_framework import serializers
from sit.serializers import SitSerializer
from users.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserLimiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=4)
    new_password = serializers.CharField(required=True, min_length=8)
    #site = SitSerializer(many=False, read_only=True)
    sit = serializers.UUIDField()
    #sit = serializers.PrimaryKeyRelatedField('sit.Sit', read_only=True)




class UserSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'matricule']
        extra_kwargs = {
            'email': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    domaine = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sit = SitSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'password', 'last_name', 'domaine', 'sit', 'email', 'avatar', 'matricule', 'is_active',
                   'groups', 'username', 'modified_by', 'created_by', 'date_joined', 'modified']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'validators': []},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'modified_by': {'read_only': True},
            'created_by': {'read_only': True},
            'created': {'read_only': True},
            'modified': {'read_only': True}
        }



class AccountEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=4)
    password = serializers.CharField(required=True, min_length=8)


class AccountUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=4)
    password = serializers.CharField(required=True, min_length=4)
"""
class AccountPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, min_length=13, max_length=14)
    password = serializers.CharField(required=True, min_length=8)"""



