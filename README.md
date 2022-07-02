
# RSS FEED SCRAPER

simple RSS scraper which saves RSS feeds to a database and lets a
user view and manage his feeds via a simple API.

The API expose all the necessary functionality to view all feeds registered by the user, the amount of unread entries
in his feeds and the ability to comment on a feed item.




## Installation

Install my-project


```bash
  mv settings.env.test settings.env
  mv db.env.test db.env
  docker-compose up -d 
  chmode 775 ./migrate.sh
  ./migrate.sh
  
```
    


## API Reference

#### User account creation

```http
  POST /user
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**.  |
| `password` | `string` | **Required**.  |

#### User account login

```http
  POST /token
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**.  |
| `password` | `string` | **Required**.  |


#### User account reset password
```http
  POST /resetpassword
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**.  |
| `password` | `string` | **Required**.  |


#### Get feeds by source id
```http
  GET /feed/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**.  source id |

#### Get user-feed by feed-id
```http
  GET /userfeed/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**.  feed id |

#### Update user-feed by feed-id
```http
  PUT /userfeed/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**.  feed id |
| `is_bookmarked`      | `boolean` | **Required**.   |
| `is_starred`      | `boolean` | **Required**.   |
| `is_read`      | `string` | **Required**.   |

#### Get all user-feed 
```http
  GET /userfeeds
```


#### Comment creation

```http
  POST /comment
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | **Required**.  |
| `feed` | `string` | **Required**.  |
| `parent` | `int` | **Not Required**.  |

#### Get all comments by feed-id
```http
  GET /feed/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**.  feed id |



#### Category creation

```http
  POST /source
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**.  |

#### Get all categgories by user-id
```http
  GET /categories
```

#### Source creation

```http
  POST /source
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**.  |
| `name` | `string` | **Required**.  |
| `category` | `int` | **Required**.  |


#### Get a source by user-id
```http
  GET /source
```


#### Get all source by category-id
```http
  GET /sources/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**.  feed id |

## Appendix


Fetch the feeds periodically and parse them using the universal feedparser and store the entries somewhere.
    
Use ETags and IfModified headers when fetching feeds to avoid parsing feeds that have not changed since your last fetch. you'll have to maintain Etags and Ifmodified values recieved during last fetch of the feed.
    
To avoid duplication, each entry should be stored with its unique guid, then check whether an entry with the same guid is already stored or not. (fall back through entry_link, hash of title+feed url to uniquely identify the entry, in case the feed entries have no guid)

## etag:
Typically, the ETag value is a hash of the content, a hash of the last modification timestamp, or just a revision number.


Another typical use of the ETag header is to cache resources that are unchanged. If a user visits a given URL again (that has an ETag set), and it is stale (too old to be considered usable), the client will send the value of its ETag along in an If-None-Match header field and

With the help of the ETag and the If-Match headers, you can detect mid-air edit collisions. 
#### if there is no etag or modified information:
I used the Date in the header as a fallback if there is no etag or modified information in the feed.

Use feed['headers']['Date'] as a modified information

Use hash(f"{url}{link}{title}") as etag field

