from django.urls import path, include
from main.views import (
    TestView, FeedView,
    CreateUserView, UpdateUserView,
    SourceView, SourceListView, CategoryListView,
    CategoryView, CommentView, UserFeedView, UserFeedListView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('test', TestView.as_view()),
    path('feed/<int:source>', FeedView.as_view()),
    path('sources/<int:pk>', SourceListView.as_view()),
    path('category/<int:pk>', CategoryView.as_view()),
    path('category', CategoryView.as_view()),
    path('categories', CategoryListView.as_view()),
    path('comment', CommentView.as_view()),
    path('comment/<int:pk>', CommentView.as_view()),
    path('userfeed', UserFeedView.as_view()),
    path('userfeeds', UserFeedListView.as_view()),
    path('userfeed/<int:pk>', UserFeedView.as_view()),
    path('source/<int:pk>', SourceView.as_view()),
    path('source', SourceView.as_view()),
    path('user', CreateUserView.as_view()),
    path('resetpassword', UpdateUserView.as_view()),
    path('token', obtain_auth_token, name='api_token_auth'),
]
