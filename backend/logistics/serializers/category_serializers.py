from rest_framework import serializers

from logistics import models


class RequestCategorySerializer(serializers.Serializer):
    name = serializers.CharField()


class ResponseCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class ResponseCategoryPageSerializer(serializers.Serializer):
    categories = ResponseCategorySerializer(many=True)
    total = serializers.IntegerField()


class PaginationSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10)
    offset = serializers.IntegerField(default=0)
