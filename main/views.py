from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import views, viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from main.serializers import UserSerializer, FeedSerializer, SourceSerializer, CategorySerializer, UserFeedSerializer, \
    CommentSerializer
from main.tasks import do_feed_parse_with_retry

from rest_framework.response import Response
from main.models import Feed, UserFeed, Source, Category, Comment
from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(views.APIView):
    def get(self, request):
        r = do_feed_parse_with_retry()
        print(r)


class CreateUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UpdateUserView(APIView):

    def post(self, request):
        user = User.objects.get(username=request.data.get('username'))
        user.set_password(request.data.get('password'))
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class FeedView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, source):
        user = request.user.id
        feeds = Feed.objects.filter(source_id=source, source__user__id=user)
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SourceView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        try:
            user = request.user.id
            feeds = Source.objects.get(user_id=user, id=pk)
            serializer = SourceSerializer(feeds)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Source.DoesNotExist:
            return Response("source not found", status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def post(request):
        user = request.user.id
        data = {"user": user}
        serializer = SourceSerializer(data={**data, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SourceListView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        user = request.user.id
        feeds = Source.objects.filter(user_id=user, category__id=pk)
        serializer = SourceSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = request.user.id
        feeds = Category.objects.filter(user_id=user)
        serializer = CategorySerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        try:
            user = request.user.id
            feeds = Category.objects.get(user_id=user, id=pk)
            serializer = CategorySerializer(feeds)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response("category not found", status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def post(request):
        user = request.user.id
        data = {"user": user}
        serializer = CategorySerializer(data={**data, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFeedView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        try:
            user = request.user.id
            feed = UserFeed.objects.get(user_id=user, id=pk)
            serializer = UserFeedSerializer(feed)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserFeed.DoesNotExist:
            return Response("user-feed not found", status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request, pk):
        try:
            user = request.user.id
            data = {"user": user}
            user_feed = UserFeed.objects.get(id=pk)
            serializer = UserFeedSerializer(user_feed, data={**data, **request.data}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserFeed.DoesNotExist:
            return Response("user-feed not found", status=status.HTTP_404_NOT_FOUND)


class UserFeedListView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = request.user.id
        feed = UserFeed.objects.filter(user_id=user)
        serializer = UserFeedSerializer(feed, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        feeds = Comment.objects.filter(feed_id=pk)
        serializer = CommentSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        user = request.user.id

        data = {"user": user}
        serializer = CommentSerializer(data={**data, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
