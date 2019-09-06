from rest_framework import serializers

from core.models import Tag, Attribute, Product


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


class ProductSerializer(serializers.ModelSerializer):
    """Serialize a product"""
    attributes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Attribute.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'attributes', 'tags', 'time_minutes',
            'price', 'link',
        )
        read_only_fields = ('id',)


class ProductDetailSerializer(ProductSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to product"""

    class Meta:
        model = Product
        fields = ('id', 'image')
        read_only_fields = ('id',)
