from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Attribute, Product

from product import serializers


class BaseAttributeViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    """Base viewset for user owned attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttributeViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class AttributeViewSet(BaseAttributeViewSet):
    """Manage ingredients in the database"""
    queryset = Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Manage products in the database"""
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the products for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
