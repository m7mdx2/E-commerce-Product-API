from django.shortcuts import render
from rest_framework import viewsets
from .models import Product , Order , Review , Category 
from .serializers import ProductSerializer , UserSerializer , OrderSerializer , ReviewSerializer , CategorySerializer
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as django_filters
from rest_framework_simplejwt.authentication import JWTAuthentication
class UserViewSet(viewsets.ModelViewSet): # this view for handeling user creation and updatation and crud
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can interact with user
    def get_permissions(self):
        # Allow non-authenticated users to create an account (POST)
        if self.action == 'create':
            return []
        return [IsAuthenticated()]  # Require authentication for other actions (view, update, delete)

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] # i added authenticaytion classes fielde to insure token based auth
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter) # ADDING SEARCH FUNCTIONALITY example (GET /products/?search=laptop)
    search_fields = ['name', 'category'] # ADDING SEARCH FUNCTIONALITY
    def get_queryset(self):
        queryset = super().get_queryset()
        # You can further customize queryset here if needed
        return queryset
# API Endpoints for Products:

# Retrieve List of Products:

#     GET /products/
#     Retrieves all products with optional filters:

#     Filters:
#         Category: ?category=<category_id>
#         Price Range: ?min_price=<value>&max_price=<value>
#         In Stock: ?in_stock=True to check if the product has stock.

# Retrieve Individual Product:

#     GET /products/{id}/
#     Retrieves details of a specific product by its ID.
class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())  # Assuming Category is another model
    in_stock = django_filters.BooleanFilter(field_name='stock_quantity', lookup_expr='gt', label='In Stock')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']

class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can interact with order

    def get_queryset(self):
        # Allow users to see only their own orders
        if self.request.user.is_staff:  # Admin users can see all orders
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
