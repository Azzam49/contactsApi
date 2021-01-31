from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib import auth
import jwt

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        #data the api submits is at request.data
        serializer = UserSerializer(data=request.data)

        #this is going to run the validate method 
        #on the serializer
        if serializer.is_valid():
            #save() method is going to run the create method
            serializer.save()

            #Reponse will return the data that is provided
            #in the fields of the serializer and will not
            #contain the fields that are defined as 
            #write_only as in our case is password field
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        #if validation is failed, we send 400 error
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        data = request.data
        username = data.get('username','')
        password = data.get('password','')
        user= auth.authenticate(username=username,password=password)
        
        if user:
            # generate a token for the user
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECERT_KEY,"HS256")


            serializer=UserSerializer(user)

            #json format
            data={
                'user': serializer.data,
                'token': auth_token,
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)