import requests

from digikalaRssScraperTask import celery_app
from main.models import Source


def check_rss_url():
    url = 'https://news.ycombinator.com/rss'
    try:
        r = requests.get(url)
        return r.status_code
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


@celery_app.task()
def do_scrapping_with_retry(url):
    print("hi")


def do_scrapping():
    urls = Source.objects.all().values_list('url', flat=True)
    for url in urls:
        do_scrapping_with_retry(url)
