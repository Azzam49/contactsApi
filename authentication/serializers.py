
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    #

    #write_only : makes the password isn't send back on the 
    #response of the request
    password = serializers.CharField(max_length=65,min_length=8,write_only=True)
    
    email = serializers.EmailField(max_length=255,min_length=4)

    first_name = serializers.CharField(max_length=255,min_length=2)

    last_name = serializers.CharField(max_length=255,min_length=2)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

    # we need to overwrite the validate method in order
    # to put our custom validation
    def validate(self,attrs):
        # making email optional
        email = attrs.get('email','')
        # custom validator for unique emails
        if User.objects.filter(email=email).exists():
            #if this error raising isn't used, our api will raise
            #a none error
            raise serializers.ValidationError(
                {'email':('Email is already in use.')}
                )
        return super().validate(attrs)

    # runs after the validate method
    def create(self,validated_data):
        #creates user the suitable way with the 
        #validated data by using create_user method
        #return User.objects.create_user(validated_data)
        #we need the ** to return the values formated
        #correctly to our response
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65,min_length=8,write_only=True)
    username = serializers.CharField(max_length=255,min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']