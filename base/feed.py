import feedparser


"""
maj: image renvoie du code html 



"""
def get_source(parsed):
    articles = []
    feed = parsed['feed']
    for entry in feed:
        articles.append({
            'image': feed['image'],
            'title': feed['title'],
            'subtitle': feed['subtitle_detail'],
        })
    return articles
        
    

def get_articles(parsed):
    articles = []
    entries = parsed['entries']
    for entry in entries:
        articles.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'summary': entry['summary'],
            'published': entry['published_parsed'],
            'media' : entry['media_content'],
        })
    return articles