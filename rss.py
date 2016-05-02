import feedparser
from flask import Flask
app = Flask(__name__)
FEEDS = {
             'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
             'CNN': 'http://rss.cnn.com/rss/edition.rss',
             'FOX': 'http://feeds.foxnews.com/foxnews/latest',
             'JAZ': 'http://www.aljazeera.net/aljazeerarss/3c66e3fb-a5e0-4790-91be-ddb05ec17198/4e9f594a-03af-4696-ab98-880c58cd6718',
             'STK': 'http://stackoverflow.com/feeds'
             }
@app.route("/")
# Using dynamic routes
@app.route("/<publisher>")

def get_news(publisher = 'BBC'):
    if publisher not in FEEDS:
        from flask import abort
        abort(404)
    
    feed = feedparser.parse(FEEDS[publisher])
    first_article = feed['entries'][0]
    return """
    <html>
    <head>
    <title>News</title>
    </head>
    <body>
    <h1>RSS News</h1>
    Published: {0}<br />
    <h3>{1}</h3>
    <p>{2}</p>
    </body>
    </html>
    
    """.format(first_article.get("published"), first_article.get("title"), first_article.get("summary"))

if __name__ == '__main__':
    app.run(port = 8000, debug = True)
