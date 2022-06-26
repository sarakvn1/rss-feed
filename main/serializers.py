from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # we have to override tha create
    # method because the 'write_only' and
    # 'required' will store the password as
    # a normal field and will not hashed

    # it will hash the password and create user
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # it will create token automatically for each user
        token = Token.objects.create(user=user)
        return user