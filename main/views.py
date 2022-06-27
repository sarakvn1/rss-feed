from django.shortcuts import render
from rest_framework import views
# Create your views here.
from main.feed_parser import do_feed_parse_with_retry


class TestView(views.APIView):
    def get(self,request):
        r = do_feed_parse_with_retry()
        print(r)