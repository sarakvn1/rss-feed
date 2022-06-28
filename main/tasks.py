from loguru import logger

from digikalaRssScraperTask import celery_app
from main.feed_parser import FeedParser
from main.models import Source


@celery_app.task()
def do_feed_parse_with_retry():
    try:

        source_list = Source.objects.all().values('id', 'url', 'last_modified', 'etag', 'user')
        for source in source_list:
            fp = FeedParser(source=source)
            modified = source.get('last_modified')
            etag = source.get('etag')
            feed_result = fp.get_feed_result(modified=modified, etag=etag)
            fp.update_source(feed_result=feed_result)
            fp.set_feed_entries(feed_result=feed_result)

    except Exception as e:
        logger.info(e.args)
        logger.exception(e)

