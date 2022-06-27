
    
Fetch the feeds periodically and parse them using the universal feedparser and store the entries somewhere.
    
Use ETags and IfModified headers when fetching feeds to avoid parsing feeds that have not changed since your last fetch. you'll have to maintain Etags and Ifmodified values recieved during last fetch of the feed.
    
To avoid duplication, each entry should be stored with its unique guid, then check whether an entry with the same guid is already stored or not. (fall back through entry_link, hash of title+feed url to uniquely identify the entry, in case the feed entries have no guid)

https://dev.to/mr_destructive/feedparser-python-package-for-reading-rss-feeds-5fnc
----------------------------------------------------------------------------------------
what is etag:Typically, the ETag value is a hash of the content, a hash of the last modification timestamp, or just a revision number.
usage of etag :Another typical use of the ETag header is to cache resources that are unchanged. If a user visits a given URL again (that has an ETag set), and it is stale (too old to be considered usable), the client will send the value of its ETag along in an If-None-Match header field and
With the help of the ETag and the If-Match headers, you can detect mid-air edit collisions. 
source :https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
--------------------------------------------------------------------------------------
if there is no etag and last_modified :https://stackoverflow.com/questions/22211795/python-feedparser-how-can-i-check-for-new-rss-data
------------------------------------------------
atomic transactions " You can't execute queries until the end of the 'atomic' block" problem : https://stackoverflow.com/questions/50866370/an-error-occurred-in-the-current-transaction-you-cant-execute-queries-until-th
--------------------------------------------
if there is no etag or modified information:


I would suggest using the Date in the header as a fallback if there is no etag or modified information in the feed.

Use feed['headers']['Date'] which can be used like this.

feedparser.parse(url, modified=feed['headers']['Date'])

Edit: But it looks like that some servers ignoring the modified parameter.
----------------------------------------------------------------------