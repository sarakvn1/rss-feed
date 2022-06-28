import feedparser
import requests
from django.db import transaction
from loguru import logger

from digikalaRssScraperTask import celery_app
from main.models import Source, Feed, UserFeed
from main.serializers import FeedSerializer, UserFeedSerializer
from datetime import datetime
from time import mktime


class FeedParser:
    def __init__(self, source):
        self.source = source

    @staticmethod
    def generate_custom_guid(url, link, title):
        hash_string = f"{url}{link}{title}"
        return hash(hash_string)

    def get_feed_result(self, modified=None, etag=None):

        if modified is not None:
            feed_result = feedparser.parse(self.source.get('url'), modified=modified)
        elif etag is not None:
            feed_result = feedparser.parse(self.source.get('url'), etag=etag)
        else:
            feed_result = feedparser.parse(self.source.get('url'))
        return feed_result

    def update_source(self, feed_result):
        modified = feed_result.get('modified')
        etag = feed_result.get('etag')
        source = Source.objects.filter(url=self.source.get('url'))
        source.update(etag=etag, last_modified=modified)

    def set_feed_entries(self, feed_result):
        try:
            if feed_result.status != 304:
                for entry in feed_result.entries:
                    guid = entry.get('id', entry.get('guid'))
                    if guid is None:
                        guid = self.generate_custom_guid(self.source.get('url'), entry.link, entry.title)

                    if 'image' in entry:
                        image_url = entry.image
                    else:
                        image_url = None
                    if len(entry.content) > 0:
                        dt = datetime.fromtimestamp(mktime(entry.get('published_parsed')))
                        feed_exist = Feed.objects.filter(guid=guid).exists()
                        if not feed_exist:
                            feed_data = {
                                "guid": guid,
                                "image": image_url,
                                "content": entry.content[0].get('value'),
                                "title": entry.title,
                                "source": self.source.get('id'),
                                "published_time": dt,
                                "url": entry.get('link')
                            }
                            feed_serializer = FeedSerializer(data=feed_data)
                            feed_serializer.is_valid(raise_exception=True)
                            feed_serializer.save()
                            feed_id = feed_serializer.data.get('id')
                            user_feed_data = {
                                "feed": feed_id,
                                "user": self.source.get('user')
                            }
                            user_feed_serializer = UserFeedSerializer(data=user_feed_data)
                            user_feed_serializer.is_valid(raise_exception=True)
                            user_feed_serializer.save()
                        else:
                            continue
            else:
                feeds = Feed.objects.filter(source__url=self.source.get('url')).values_list('id', flat=True)
                user = self.source.get('user')
                user_feeds = UserFeed.objects.filter(feed__in=feeds, user=user)
                if len(user_feeds) == feeds:
                    return
                if len(feeds) == 0:
                    self.retry()
                    feeds = Feed.objects.filter(source__url=self.source.get('url')).values_list('id', flat=True)

                user_feeds = [UserFeed(feed_id=f, user_id=user) for f in feeds]
                _ = UserFeed.objects.bulk_create(user_feeds)
        except Exception as e:
            logger.info(e.args)
            logger.exception(e)

    def retry(self):
        feed_result = self.get_feed_result()
        self.update_source(feed_result=feed_result)
        self.set_feed_entries(feed_result=feed_result)

