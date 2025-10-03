from rest_framework import serializers
from apps.users.services import UserReadService
from core.serializers.service_serializer import ServiceSerializer


# Add your serializers here

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserSerializer(ServiceSerializer):
    service_class = UserReadService

    class Meta:
        fields = '__all__'

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        test = self.service_class()

        return "{0} {1}".format(obj.first_name, obj.last_name)


