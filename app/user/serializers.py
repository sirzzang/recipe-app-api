from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''serializer for the users object'''

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        '''create a new user with encrypted password and return it'''
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    email = serializers.CharField()  # email input
    password = serializers.CharField(  # password input
        style={'input_type': 'password'},
        trim_whitespace=False  # possible to have white space
    )

    def validate(self, attrs):
        '''validate and authenticate the user'''

        # retrieve email and password fields
        email = attrs.get('email')
        password = attrs.get('password')

        # authenticate user
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # when not working, raise Error
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # set user object to user attribute
        attrs['user'] = user
        return attrs
