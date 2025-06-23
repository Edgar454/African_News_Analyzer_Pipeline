import json
import uuid
import feedparser

def parse_rss_feed(url):
    """
    Parses an RSS feed from the given URL and returns a list of dictionaries
    containing the feed's title, link, and description.
    
    Args:
        url (str): The URL of the RSS feed to parse.
        
    Returns:
        list: A list of dictionaries with keys 'title', 'link', and 'description'.
    """
    try:
        feed = feedparser.parse(url)
        parsed_items = []
        if not feed.entries:
            print(f"No entries found in the feed: {url}")
            return {
            "url": url,
            "status": "failure",
            "count": 0,
            "items": parsed_items
        }

        else:
            print(f"Found {len(feed.entries)} entries in the feed: {url}")
            for entry in feed.entries:
                item = {
                    'id': str(uuid.uuid4()),
                    'title': entry.title,
                    'link': entry.link,
                    'author': entry.get('author', '') or (entry.get('authors', [{}])[0].get('name', '') if entry.get('authors') else ''),
                    'description': entry.get('description', ''),
                    'pubDate': entry.get('published', ''),
                    'tags': [tag.term for tag in entry.get('tags', [])],
                    'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                }
                parsed_items.append(item)

        return {
            "url": url,
            "status": "ok",
            "count": len(parsed_items),
            "items": parsed_items
        }
        
    except Exception as e:
        print(f"Error parsing feed {url}: {e}")
        return {
            "url": url,
            "status": "failure",
            "count": 0,
            "items": []
        }


def parse_multiple_feeds(urls):
    """
    Parses multiple RSS feeds from a list of URLs.
    
    Args:
        urls (list): A list of URLs of the RSS feeds to parse.
        
    Returns:
        list: A list of dictionaries containing parsed feed items.
    """
    all_items = []
    for url in urls:
        items = parse_rss_feed(url)['items']
        all_items.extend({'id': item['id'], 'content': json.dumps(item, ensure_ascii=False)} for item in items)
    return all_items

if __name__ == "__main__":
    # Example usage
    urls = ["https://africapresse.com/feed/","https://feeds.feedburner.com/AfricaIntelligence"] 

    parsed_feed = parse_multiple_feeds(urls)
    print(f"Parsed {len(parsed_feed)} items from the feeds.")
    for feed in parsed_feed:
        item = json.loads(feed['content'])
        print(f"Title: {item['title']}\nLink: {item['link']}\nDescription: {item['description']}\nPublished: {item['pubDate']}\nTags: {', '.join(item['tags'])}\n")
        print(f"...\nAuthor: {item['author']}\n")
