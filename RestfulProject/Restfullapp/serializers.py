from .models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class EmplyeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')


        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], password=validated_data['password'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'])
            return user

