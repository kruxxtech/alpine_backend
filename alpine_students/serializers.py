from rest_framework import serializers
from .models import *


class StudentIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = "__all__"


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class StudentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ("student_id", "stu_name")


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
