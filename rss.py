import feedparser
import json
import urllib
import requests


from flask import Flask
from flask import render_template
from flask import request
from flask.json import jsonify
app = Flask(__name__)
FEEDS = {
             'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
             'CNN': 'http://rss.cnn.com/rss/edition.rss',
             'FOX': 'http://feeds.foxnews.com/foxnews/latest',
             'JAZ': 'http://www.aljazeera.net/aljazeerarss/3c66e3fb-a5e0-4790-91be-ddb05ec17198/4e9f594a-03af-4696-ab98-880c58cd6718',
             'STK': 'http://stackoverflow.com/feeds'
             }
DEFAULTS = {
            'publisher': 'BBC',
            'city': 'London, UK',
            'currency_from': 'USD',
            'currency_to': 'EGP'
            }
currency_url = 'https://openexchangerates.org/api/latest.json?app_id=ff31a748274e42ef8b5560747926d2e0'

@app.route("/")
def home():
    publisher = request.args.get('publisher')
    if not publisher:
        publisher = DEFAULTS['publisher']
    articles = get_news(publisher)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template('home.html',
                            articles = articles,
                             weather = weather,
                             rate = rate,
                             currency_from = currency_from,
                             currency_from_f = "flags/"+currency_from[0:2].lower()+".png",
                             currency_to = currency_to,
                             currency_to_f = "flags/"+currency_to[0:2].lower()+".png",
                             currencies = sorted(currencies)
                             )


def get_rate(frm, to):
    response = requests.get(currency_url)
    jsonData = json.loads(response.text)
    rates = jsonData.get('rates')
    frm_rate = rates.get(frm.upper())
    to_rate = rates.get(to.upper())
    return (to_rate/frm_rate, rates.keys())
    
@app.route("/we/<query>")
def get_weather(query = 'london'):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ef7660bf4143740509342a6eaf86760c"
    query = urllib.request.quote(query)
    url = api_url.format(query)
    #response = urllib.request.urlopen(url)
    response = requests.get(url)
    jsonData = json.loads(response.text)
    
    #jsonData = jsonify(data=response)
    #return response.text
    '''
    return obj
    data = response.read()
    #data = json.loads(response.read())
    #return data
    #data = urllib.request.urlopen(url)
    return jsonify(data )
    
    jsonData = json.load(data)
    #jsonData = jsonify(data)
    #return jsonData
    '''
    weather = None
    if jsonData.get('weather'):
                    
        weather = {
                   "description": jsonData['weather'][0]['description'],
                   "icon": "http://openweathermap.org/img/w/"+jsonData['weather'][0]['icon']+".png",
                   "temprature": jsonData['main']['temp'],
                   "city": jsonData['name'],
                   "country": jsonData['sys']['country'],
                   "flag": 'flags/'+jsonData['sys']['country'].lower()+'.png'
                   }
    
    return weather
    

# Using dynamic routes
@app.route("/<publisher>")

def get_news(publisher = 'BBC'):
    publisher = publisher.upper()
    if publisher not in FEEDS:
        from flask import abort
        abort(404)
    
    try:
        
        feed = feedparser.parse(FEEDS[publisher])
        first_article = feed['entries'][0]
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
    #return render_template("home.html", articles = feed['entries'], weather = get_weather())
    return feed['entries']


    


if __name__ == '__main__':
    app.run(port = 8000, debug = True)
