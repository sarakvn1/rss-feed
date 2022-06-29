import json
import time
from types import SimpleNamespace
import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from loguru import logger

from main.tasks import do_feed_parse_with_retry
from feedparser.util import FeedParserDict
from main.models import UserFeed

@pytest.mark.django_db
def test_create_source_with_force_authentication_should_pass():
    user = baker.make('User', id=1, username="lauren")
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi"
    }
    client.force_authenticate(user=user)
    response = client.post('/source', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_source_with_token_should_pass():
    user = baker.make('User', id=1, username="lauren")
    token = baker.make('Token', user=user)
    baker.make('Category', id=1)
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi",
        "category": 1
    }
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
    response = client.post('/source', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_source_without_token_should_fail():
    baker.make('User', id=1)
    baker.make('Category', id=1)
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi",
        "category": 1
    }
    response = client.post('/source', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_source_should_fail():
    user = baker.make('User', id=1)
    baker.make('Category', id=1)
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi",
        "category": 2
    }
    client.force_authenticate(user=user)
    response = client.post('/source', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_source_list_with_force_authentication_should_pass():
    user = baker.make('User', id=1, username="lauren")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/sources', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_source_item_with_force_authentication_should_fail():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/source/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_source_item_with_force_authentication_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/source/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category_with_force_authentication_should_pass():
    user = baker.make('User', id=1, username="lauren")
    client = APIClient()
    data = {
        "name": "tech"
    }
    client.force_authenticate(user=user)
    response = client.post('/category', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category_without_token_should_fail():
    user = baker.make('User', id=1, username="lauren")
    client = APIClient()
    data = {
        "name": "tech"
    }
    response = client.post('/category', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_category_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Category', id=1, user_id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/category/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_category_with_wrong_id_should_fail():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Category', id=1, user_id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/category/2', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_category_should_fail():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Category', id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/category/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_category_list_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Category', id=1, user_id=1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/categories', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_feed_list_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    baker.make('Feed', source_id=1, _quantity=10)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/feed/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_feed_should_fail():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    baker.make('Feed', source_id=1, _quantity=10)
    client = APIClient()
    response = client.get('/feed/1', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_user_feed_list_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    baker.make('Feed', source_id=1, _quantity=10)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/userfeeds', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user_feed_list_should_fail():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    baker.make('Feed', source_id=1, _quantity=10)
    client = APIClient()
    # client.force_authenticate(user=user)
    response = client.get('/userfeeds', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_user_feed_should_pass():
    user = baker.make('User', id=1, username="lauren")
    baker.make('Source', id=1, user_id=1)
    baker.make('Feed', source_id=1, _quantity=10)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/userfeeds', content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_user_feed_should_pass():
    user = baker.make('User', id=1)
    baker.make('Category', id=1)
    baker.make('UserFeed', id=1)
    client = APIClient()
    data = {
        "is_starred": False,
        "is_bookmarked": True,
        "is_read": True
    }

    client.force_authenticate(user=user)
    response = client.put('/userfeed/1', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_user_feed_should_fail():
    user = baker.make('User', id=1)
    baker.make('Category', id=1)
    baker.make('UserFeed', id=2)
    client = APIClient()
    data = {
        "is_starred": False,
        "is_bookmarked": True,
        "is_read": True
    }

    client.force_authenticate(user=user)
    response = client.put('/userfeed/1', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_user_feed_without_token_should_fail():
    user = baker.make('User', id=1)
    baker.make('Category', id=1)
    baker.make('UserFeed', id=2)
    client = APIClient()
    data = {
        "is_starred": False,
        "is_bookmarked": True,
        "is_read": True
    }
    response = client.put('/userfeed/1', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_comment_on_feed_should_fail():
    user = baker.make('User', id=1)
    baker.make('Feed', id=2)
    client = APIClient()
    data = {
        "message": "really?",
        "feed": 1
    }

    client.force_authenticate(user=user)
    response = client.post('/comment', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_comment_on_feed_should_pass():
    user = baker.make('User', id=1)
    baker.make('Feed', id=1)
    client = APIClient()
    data = {
        "message": "really?",
        "feed": 1
    }

    client.force_authenticate(user=user)
    response = client.post('/comment', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_comment_on_feed_with_parent_should_pass():
    user = baker.make('User', id=1)
    baker.make('Feed', id=1)
    baker.make('Comment', id=1)
    client = APIClient()
    data = {
        "message": "really?",
        "feed": 1,
        "parent": 1
    }

    client.force_authenticate(user=user)
    response = client.post('/comment', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_comment_on_feed_with_parent_should_fail():
    user = baker.make('User', id=1)
    baker.make('Feed', id=1)
    baker.make('Comment', id=12)
    client = APIClient()
    data = {
        "message": "really?",
        "feed": 1,
        "parent": 1
    }

    client.force_authenticate(user=user)
    response = client.post('/comment', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 400


@pytest.mark.django_db
def test_feed_parser_should_pass(mocker):
    entry = {'title': 'S9:E8 - How to Introduce Coding to Your Kids',
                         'title_detail': {'type': 'text/plain', 'language': None,
                                          'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                          'value': 'S9:E8 - How to Introduce Coding to Your Kids'}, 'links': [
                            {'rel': 'alternate', 'type': 'text/html',
                             'href': 'https://devpods.herokuapp.com/podcasts/devdiscuss/episodes/274'},
                            {'length': '42332300', 'type': 'audio/mpeg',
                             'href': 'https://dts.podtrac.com/redirect.mp3/traffic.megaphone.fm/FOR6494492862.mp3?updated=1656502985',
                             'rel': 'enclosure'}],
                         'link': 'https://devpods.herokuapp.com/podcasts/devdiscuss/episodes/274',
                         'published': 'Wed, 29 Jun 2022 03:00:00 +0000',
                         'published_parsed': time.struct_time((2000,1,1,0,0,0,3,100,-1)),
                         'id': 'https://devpods.dev/podcasts/devdiscuss/73', 'guidislink': False,
                         'tags': [{'term': 'Podcast', 'scheme': None, 'label': None}],
                         'summary': 'Pete Ingram-Cauchi, CEO of ID Tech.',
                         'summary_detail': {'type': 'text/plain', 'language': None,
                                            'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                            'value': ' Pete Ingram-Cauchi, CEO of ID Tech.'},
                         'content': [{'type': 'text/html', 'language': None,
                                      'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                      'value': 'r></li and more.</p>'}],
                         'subtitle': "Learning to code young doesn't just prepare your child to just be a developer",
                         'subtitle_detail': {'type': 'text/plain', 'language': None,
                                             'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                             'value': "Learning to code young doesn't just"},
                         'authors': [{'name': 'DEV'}], 'author': 'DEV', 'author_detail': {'name': 'DEV'},
                         'itunes_explicit': False, 'itunes_duration': '44:06'}
    entry_value = FeedParserDict(entry)
    return_value = {"bozo": True,
                    "entries": [
                        entry_value
                    ],

                    "feed": {'title': 'DevDiscuss', 'title_detail': {'type': 'text/plain', 'language': None,
                                                                     'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                                                     'value': 'DevDiscuss'}, 'links': [
                        {'href': 'https://feeds.devpods.dev/devdiscuss_podcast.xml', 'rel': 'self',
                         'type': 'application/rss+xml'}, {'rel': 'alternate', 'type': 'text/html', 'href': ''}],
                             'link': '', 'subtitle': '', 'subtitle_detail': {'type': 'text/plain', 'language': None,
                                                                             'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                                                             'value': ''},
                             'updated': 'Wed, 29 Jun 2022 11:42:01 +0000',
                             'updated_parsed': time.struct_time((2000,1,1,0,0,0,3,100,-1)), 'language': 'en-US',
                             'sy_updateperiod': 'hourly', 'sy_updatefrequency': '1',
                             'generator_detail': {'name': 'https://wordpress.org/?v=4.6'},
                             'generator': 'https://wordpress.org/?v=4.6',
                             'summary': 'The show covers burning topics that.',
                             'summary_detail': {'type': 'text/plain', 'language': None,
                                                'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                                'value': 'DevDiscuss is the first original podcast from DEV,ounder.'},
                             'authors': [{'name': 'DevDiscuss', 'email': 'levi@dev.to'},
                                         {'name': 'DEV', 'email': 'levi@dev.to'}], 'author': 'levi@dev.to (DEV)',
                             'author_detail': {'name': 'DevDiscuss', 'email': 'levi@dev.to'}, 'itunes_explicit': False,
                             'image': {'href': 'https://dev-pods.s3.amazonaws.com/devdiscuss_cover_art.jpg',
                                       'title': 'DevDiscuss', 'title_detail': {'type': 'text/plain', 'language': None,
                                                                               'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                                                               'value': 'DevDiscuss'},
                                       'links': [{'rel': 'alternate', 'type': 'text/html', 'href': ''}], 'link': ''},
                             'publisher_detail': {'name': 'DevDiscuss', 'email': 'levi@dev.to'},
                             'rights': 'Copyright 2022 DEV', 'rights_detail': {'type': 'text/plain', 'language': None,
                                                                               'base': 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                                                                               'value': 'Copyright 2022 DEV'},
                             'tags': [{'term': 'Technology', 'scheme': 'http://www.itunes.com/', 'label': None},
                                      {'term': 'Tech News', 'scheme': 'http://www.itunes.com/', 'label': None}]},
                    "headers": {'date': 'Wed, 29 Jun 2022 12:18:08 GMT', 'content-type': 'text/xml',
                                'transfer-encoding': 'chunked', 'connection': 'close',
                                'last-modified': 'Wed, 29 Jun 2022 11:42:02 GMT', 'etag': 'W/"62bc3a8a-49bed"',
                                'cf-cache-status': 'DYNAMIC',
                                'expect-ct': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
                                'report-to': '{"endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report\\/v3?s=Thk5OgNHAsn9iI1f5kGd%2BHW9Th%2B9ThGCqu2r4RQi7PBwrrrjoXsB4yIVP6aBjEbp18jGrRVZpa6ZlnBNH11cJ%2BuXaal6kUYeQ49IyyKMQ%2FCS5kOZ9hWXrJppqflKul3tfuExlw%3D%3D"}],"group":"cf-nel","max_age":604800}',
                                'nel': '{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                                'server': 'cloudflare', 'cf-ray': '722e9a60baf2913d-FRA', 'content-encoding': 'gzip',
                                'alt-svc': 'h3=":443"; ma=86400, h3-29=":443"; ma=86400'},

                    "etag": 'W/"62bc3a8a-49bed"',
                    "updated": 'Wed, 29 Jun 2022 11:42:02 GMT',
                    "updated_parsed": time.struct_time((2000,1,1,0,0,0,3,100,-1)),
                    "href": 'https://feeds.devpods.dev/devdiscuss_podcast.xml',
                    "status": 200,
                    "encoding": 'utf-8',
                    "bozo_exception":
                        "CharacterEncodingOverride('document declared as us-ascii, but parsed as utf-8')",
                    "version": 'rss20',
                    "namespaces": {'content': 'http://purl.org/rss/1.0/modules/content/',
                                   'wfw': 'http://wellformedweb.org/CommentAPI/',
                                   'dc': 'http://purl.org/dc/elements/1.1/', '': 'http://www.w3.org/2005/Atom',
                                   'sy': 'http://purl.org/rss/1.0/modules/syndication/',
                                   'slash': 'http://purl.org/rss/1.0/modules/slash/',
                                   'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
                                   'rawvoice': 'http://www.rawvoice.com/rawvoiceRssModule/',
                                   'googleplay': 'http://www.google.com/schemas/play-podcasts/1.0/play-podcasts.xsd'}}

    return_v = FeedParserDict(return_value)
    source = baker.make('Source', id=1, url="https://jadi.net/rss", last_modified=None, etag=None)
    s = {"id": 1, "url": "https://jadi.net/rss", "user": 1, "etag": None, "last_modified": None}
    mocker.patch('main.feed_parser.FeedParser.get_feed_result',
                 return_value=return_v)
    user = baker.make('User', id=1)
    # c = baker.make('Category', id=1, user_id=1)

    parser = do_feed_parse_with_retry()
    user_feed = UserFeed.objects.count()

    assert user_feed == 1
