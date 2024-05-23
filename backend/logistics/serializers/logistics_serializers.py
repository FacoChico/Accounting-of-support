from rest_framework import serializers

from .category_serializers import PaginationSerializer


class RequestLogisticsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category_id = serializers.IntegerField()
    type = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    quantity_available = serializers.IntegerField()


class ResponseLogisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    category_id = serializers.IntegerField()
    type = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    quantity_available = serializers.IntegerField()


class ResponseLogisticsPageSerializer(serializers.Serializer):
    logistics = ResponseLogisticsSerializer(many=True)
    total = serializers.IntegerField()


class LogisticsPaginationSerializer(PaginationSerializer):
    category_id = serializers.IntegerField(default=None)
