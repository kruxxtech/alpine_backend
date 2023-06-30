from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

# from rest_framework_simplejwt.tokens import RefreshToken


# class UserSerializer(serializers.ModelSerializer):
#     # custom fields
#     name = serializers.SerializerMethodField(read_only=True)
#     isAdmin = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = User
#         fields = ("id", "username", "email", "name", "isAdmin")

#     def get_name(self, obj):
#         name = obj.first_name
#         if name == "":
#             name = obj.email
#         return name

#     def get_isAdmin(self, obj):
#         return obj.is_staff


# class UserSerializerWithToken(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField(read_only=True)
#     token = serializers.SerializerMethodField(read_only=True)
#     isAdmin = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = User
#         fields = ("id", "username", "email", "name", "isAdmin", "token")

#     def get_token(self, obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)

#     def get_name(self, obj):
#         name = obj.first_name
#         if name == "":
#             name = obj.email
#         return name

#     def get_isAdmin(self, obj):
#         return obj.is_staff


# new serializers for updated User class/Model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
        )
        return user
