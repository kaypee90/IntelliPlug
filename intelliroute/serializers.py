from intelliroute.models import IntegratingApp, RequestAudit
from rest_framework import serializers


class IntegratingAppSerializer(serializers.ModelSerializer):
    """Model serializer for IntegratingApp Model"""
    integrating_app_name = serializers.CharField(source='name', )

    class Meta:
        model = IntegratingApp
        fields = ('id', 'integrating_app_name', 'alias', 'base_url')

class RequestAuditSerializer(serializers.ModelSerializer):
    """Model serializer for IntegratingApp Model"""
    integrating_app = IntegratingAppSerializer()

    class Meta:
        model = RequestAudit
        fields = ('id', 'http_method', 'response_time', 'response_code', 'integrating_app')

class IntelliRouteSerializer(serializers.Serializer):
    data = serializers.JSONField()