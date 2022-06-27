
    
Fetch the feeds periodically and parse them using the universal feedparser and store the entries somewhere.
    
Use ETags and IfModified headers when fetching feeds to avoid parsing feeds that have not changed since your last fetch. you'll have to maintain Etags and Ifmodified values recieved during last fetch of the feed.
    
To avoid duplication, each entry should be stored with its unique guid, then check whether an entry with the same guid is already stored or not. (fall back through entry_link, hash of title+feed url to uniquely identify the entry, in case the feed entries have no guid)
