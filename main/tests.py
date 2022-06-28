import json

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from loguru import logger


@pytest.mark.django_db
def test_create_source_should_pass():
    baker.make('User', id=1)
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi"
    }

    regular_header = {
        'HTTP_AUTHORIZATION': 'Token 6ba6306c66f232c42011a62fbce81c4bdef972d3',
    }
    client.credentials(**regular_header)
    response = client.post('/console/app', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_source_should_fail():
    baker.make('User', id=1)
    client = APIClient()
    data = {
        "url": "https://jadi.net/rss",
        "name": "jadi"
    }

    regular_header = {
        'HTTP_AUTHORIZATION': '6ba6306c66f232c42011a62fbce81c4bdef972d3',
    }
    client.credentials(**regular_header)
    response = client.post('/console/app', data=json.dumps(data), content_type='application/json')
    logger.info(response.content)
    assert response.status_code == 401