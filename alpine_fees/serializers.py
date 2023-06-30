from rest_framework import serializers
from .models import *


class FeeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeTable
        fields = "__all__"


class FeeReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeReceipts
        fields = "__all__"
