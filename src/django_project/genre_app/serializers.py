from rest_framework import serializers


class GenreSerialzierResponse(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = SetField(child=serializers.UUIDField(), required=False)


class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = SetField(child=serializers.UUIDField(), required=False)


class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreSerialzierResponse(many=True)
