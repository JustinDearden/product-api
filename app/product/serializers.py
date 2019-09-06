from rest_framework import serializers

from core.models import Tag, Attribute


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class AttributeSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Attribute
        fields = ('id', 'name')
        read_only_fields = ('id',)
