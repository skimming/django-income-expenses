from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from rest_framework.response  import Response

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse  # takes in a url name and give your the path

import jwt
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .renderers import UserRenderer


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site
from django.urls    import reverse

from .utils import Util



# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer, )  # must be a tuple

    def post(self, request):
        #get the data from the request
        user=request.data
        # main handler for this register request is its Serializer
        serializer = RegisterSerializer(data=user)
        # will call the "validate" method on the serializer class
        # built-in interfaces serizers like is_valid (calls validate) and save (calls create)
        serializer.is_valid(raise_exception=True)
        # will call "create" method on the serializer class
        serializer.save()
        # and save the object inside the serializer.data 

        # SERIALIZER is key to operation of Django
        user_data = serializer.data



        # now add support for JWT tokens handle tokens
        user = User.objects.get(email=user_data['email'])  # email is a unique key
        # how am i getting the access token?  Use RefreshToken i suppose...
        # this is using the user's information to create an access token.
        # this can be backwards interpretable to arrive at the user's info
        # that happens on the VerifyEmail method below
        token = RefreshToken.for_user(user).access_token
        # generate "date" for sending of email
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        absurl = "http://" + current_site + relative_link + "?token="+str(token)
        email_body = "Hi " + user.username + " Use the link below to verify your email \n" + absurl
        data =  {
            'email_body': email_body,
            'email_subject': 'verify your email',
            'email_to': user.email,
        }


        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView) :

    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Description of the aparam", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request) :
        # we're getting the token with the get
        # this link is sent to the user
        token = request.GET.get('token')

        try: 
            payload = jwt.decode(token, settings.SECRET_KEY)  # decoding happens with the SECRET_KEY of the Application
            user=User.objects.get(id=payload['user_id'])

            if not user.is_verified :
                user.is_verified = True
                user.save()

            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'activation link is expired'}, status=status.HTPP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView) : # when a genericAPIView is derived, you handle all the request by yourself
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request) :
   
        serializer = self.serializer_class(data = request.data)  # passing the data to this serializer
        serializer.is_valid()  # basic check for email format

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            
            # generate "date" for sending of email
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = "http://" + current_site + relative_link

            email_body = "Hello \n Use the link below to reset your password \n" + absurl
            data =  {
                'email_body': email_body,
                'email_subject': 'reset your password', 
                'email_to': user.email,
            }

            Util.send_email(data)
        return Response({'success' : "We have sent you a link to reset pwd"}, status = status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView) :
    # there is no need for serializers here because the URL contains all the info
    # but it is generating errors... so put in a dummy one
    serializer_class = SetNewPasswordSerializer

    def get (self, request, uidb64, token) :
        try: 
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token) :
                return Response({'error' : "Token is not valid, plase request a new one"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success' : True, 'message': 'Credential valid', 'uidb64': uidb64, 'token': token }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier: 
            return Response({'error' : "Token is not valid, plase request a new one"}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView) :
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):  # now we can set our serializer data here
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)

        return Response({'success':True, 'message': 'password is set'}, status = status.HTTP_200_OK)
