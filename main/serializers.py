from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from main.models import Feed, UserFeed, Source, Comment, Category


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

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
        extra_kwargs = {'etag': {'required': False}, 'last_modified': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {"parent": {'required': False}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserFeedSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    published_time = serializers.SerializerMethodField()

    class Meta:
        model = UserFeed
        fields = (
            "user", "feed", "content", "title", "published_time", "is_read", "is_bookmarked", "is_starred",
            "created_time", "updated_time"
        )
        extra_kwargs = {'is_read': {'required': False},
                        'is_bookmarked': {'required': False},
                        'is_starred': {'required': False}
                        }

    @staticmethod
    def get_content(instance):
        return instance.feed.content

    @staticmethod
    def get_title(instance):
        return instance.feed.title

    @staticmethod
    def get_published_time(instance):
        return instance.feed.published_time
