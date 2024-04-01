from rest_framework import serializers


class GenreSerialzierResponse(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreSerialzierResponse(many=True)
