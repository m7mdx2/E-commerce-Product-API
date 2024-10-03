from rest_framework import serializers
from .models import Product , Order , Review , Category 
from django.contrib.auth.models import User
class ProductSerializer(serializers.ModelSerializer): # this serializer class inhernet from ModelSerializer
    class Meta:
        model = Product
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Overriding the create method to hash the password
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    # Overriding the update method to hash the password
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the new password
        instance.save()
        return instance
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        # The stock quantity reduction will happen in the save method of the model
        return Order.objects.create(**validated_data)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'