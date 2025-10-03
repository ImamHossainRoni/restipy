from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    """
    Enhanced ModelSerializer that works with service layer
    while maintaining ALL ModelSerializer features
    """
    service_class = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.service_class is None:
            raise TypeError(
                f"{cls.__name__} must define a `service_class` attribute"
            )

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service', None) or self.get_service()

        # Dynamically set Meta.model from service if not explicitly set
        if (hasattr(self, 'Meta') and not hasattr(self.Meta, 'model') and
                hasattr(self, 'service_class')):
            self.Meta.model = self.service.dao.model

        super().__init__(*args, **kwargs)

    def get_service(self):
        if self.service_class:
            return self.service_class()
        raise NotImplementedError("Must set service_class or pass service instance")

    def create(self, validated_data):
        return self.service.create(**validated_data)

    def update(self, instance, validated_data):
        return self.service.update(instance, **validated_data)