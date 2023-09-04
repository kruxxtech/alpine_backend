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

class StudentGuardianSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Admission.objects.all())

    class Meta:
        model = StudentGuardian
        fields = ['id', 'fathername', 'mothername', 'student']

    def validate(self, data):
        # Check if at least one of fathername or mothername is provided
        if not data.get('fathername') and not data.get('mothername'):
            raise serializers.ValidationError("Either fathername or mothername must be provided.")

        # If both are provided, prioritize the fathername
        if data.get('fathername'):
            data.pop('mothername', None)

        return data

    def create(self, validated_data):
        guardian = StudentGuardian.objects.create(**validated_data)
        return guardian