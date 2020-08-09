from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from  .models import User
from django.contrib import auth


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer) :
    # special handling for password field
    password = serializers.CharField(max_length=68, min_length=2, write_only=True) # write only won't be sent back to users

    class Meta:
        model = User
        fields=['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError("User name can only contain alpha numeric chars")

        # can do some other validations here as well
        return attrs


    def create(self, validate_data):
        # passing as **kwargs
        return User.objects.create_user(**validate_data)




class EmailVerificationSerializer(serializers.ModelSerializer) :
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields=['token']


class LoginSerializer(serializers.ModelSerializer) :
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=2, write_only=True) # write only won't be sent back to users
    username = serializers.CharField(max_length=68, min_length=2, read_only=True) # write only won't be sent back to users
    tokens = serializers.CharField(max_length=268, min_length=2, read_only=True) # write only won't be sent back to users

    class Meta: 
        model = User
        fields = ['email', 'password', 'username', 'tokens']
    # this validation will return a User instance if the password provided matches the 
    # hash of the password stored in the db
    # hash will be generated 
    def validate(self, attrs):
        email=attrs.get('email', '')
        password= attrs.get('password', '')

        # use auth to validate the email and password combo against db
        user = auth.authenticate(email=email, password=password)

        if not user : 
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active :
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified :
            raise AuthenticationFailed('Email is not verified')

        return {
            'email' : user.email,
            'username' : user.username,
            'tokens' : user.tokens()
        }


class ResetPasswordEmailRequestSerializer (serializers.Serializer) :
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields=['email']

# views and serializers work together
# to define the endpoint behavior
class SetNewPasswordSerializer (serializers.Serializer) :

    password = serializers.CharField(min_length=6, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta: 
        fields= ['password', 'token', 'uidb64']

    def validate(self, attrs) :
        try:
            password = attrs.get('password')
            token=attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token) :
                raise AuthenticationFailed('The reset link is invalid', 401)

            # now set the password
            user.set_password(password)
            user.save()
            

        except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)
