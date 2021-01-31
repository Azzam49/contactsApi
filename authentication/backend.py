

import jwt
from rest_framework import authentication,exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):


    def authenticate(self,request):
        #handles the request auth data from header
        auth_data=authentication.get_authorization_header(request)

        #if user didn't provide the Autherization detials 
        #do nothing
        if not auth_data:
            return None
        
        #decodes the token to string format
        prefix,token = auth_data.decode('utf-8').split(' ')

        print()
        print()
        print(prefix)
        print(token)
        print()
        print()
        #validate the token
        try:
            payload=jwt.decode(token,settings.JWT_SECERT_KEY,"HS256",)
            
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login'
            )
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login'
            )
        return super().authenticate(request)