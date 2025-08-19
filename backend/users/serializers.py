from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

# Gestion de l'enregistrement d'un nouvel utilisateur
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # Champs acceptés pour la création du compte
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'password', 'password2')

    # Méthode de vérification que les 2 passwords sont identiques, sinon renvoi d'une erreur
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne sont pas identiques."})
        return attrs

    # méthode appelée pour créer l'utilisateur en base
    def create(self, validated_data):
        validated_data.pop('password2') # champ password2 retiré car non présent en base
        user = CustomUser.objects.create_user(**validated_data)
        return user

# gestion de la modification d'un compte utilisateur
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email')
        read_only_fields = ('username',)
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
        }

