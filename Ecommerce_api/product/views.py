from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order, Review, Category
from .serializers import (
    ProductSerializer,
    UserSerializer,
    OrderSerializer,
    ReviewSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as django_filters
from rest_framework_simplejwt.authentication import JWTAuthentication


# --------------------
# USER VIEWSET
# --------------------
class UserViewSet(viewsets.ModelViewSet):
    # Handles CRUD operations for users. Only authenticated users can view, update or delete a user,
    # but anyone can create a new account (POST action).
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can perform other actions

    def get_permissions(self):
        # Allow non-authenticated users to create an account (POST)
        if self.action == "create":
            return []  # No authentication required for user registration
        return [
            IsAuthenticated()
        ]  # Require authentication for other actions (view, update, delete)


# --------------------
# PRODUCT FILTER
# --------------------
class ProductFilter(django_filters.FilterSet):

    # Filters for products based on price range, category, and stock status.

    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )  # Minimum price filter
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )  # Maximum price filter
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all()
    )  # Filter by category
    in_stock = django_filters.BooleanFilter(
        field_name="stock_quantity", lookup_expr="gt", label="In Stock"
    )  # Filter products that are in stock

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "in_stock"]


# --------------------
# PRODUCT VIEWSET
# --------------------
class ProductViewSet(viewsets.ModelViewSet):
  
    # Handles CRUD operations for products. Provides token-based authentication and allows read-only access to unauthenticated users.
    # Implements search functionality by product name and category.

    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Read-only access for unauthenticated users
    queryset = Product.objects.all()  # Order by a specific field, e.g., 'id'
    serializer_class = ProductSerializer
    search_fields = ["name", "category"]  # Allows search by product name and category
    filterset_class = ProductFilter  # Apply product filter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

# --------------------
# ORDER VIEWSET
# --------------------
class OrderViewSet(viewsets.ModelViewSet):

    # Handles CRUD operations for orders. Only authenticated users can view or interact with their orders.
    # Admin users can view all orders.
    
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can perform any actions

    def get_queryset(self):
        """
        Allow users to see only their own orders. Admin users can see all orders.
        """
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

# --------------------
# REVIEW VIEWSET
# --------------------
class ReviewViewSet(viewsets.ModelViewSet):

    # Handles CRUD operations for reviews. Only authenticated users can post a review, and the user who created the review is automatically assigned.

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can perform actions

    def perform_create(self, serializer):
        """
        Automatically assign the user who created the review.
        """
        serializer.save(user=self.request.user)
