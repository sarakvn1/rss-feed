from django.urls import path, include
from main.views import TestView

urlpatterns = [
    path('test', TestView.as_view())
]
