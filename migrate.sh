#!/bin/bash

sudo docker exec -it rss-feed-worker bash -c "python3 manage.py migrate"
sudo docker exec -it rss-feed bash -c "python3 manage.py migrate"

sudo docker restart rss-feed-worker
sudo docker restart rss-feed

