#5 
# update currency info
import json
import urllib
import urllib3
import requests
import feedparser
import pickle
from flask import Flask, render_template, request

DEFAULTS = {'publication': 'bbc',
           'city': 'London, UK',
           'currency_from':'GBP',
           'currency_to':'USD'}

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

with open('weather_appID', 'rb') as r:
    we_appID = pickle.load(r)
weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}"

with open('currency_appID', 'rb') as r:
    cu_appID = pickle.load(r)
currency_url = "https://openexchangerates.org/api/latest.json/?app_id={}".format(cu_appID)

@app.route("/")
def home():
    # get customized headlines
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    
    # get customized weather
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    
    #get customized currency
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
        
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    
    return render_template("home_mod1.html",
                           articles=articles,
                          weather=weather,
                          currency_from=currency_from,
                          currency_to=currency_to,
                          rate=rate,
                          currencies=sorted(currencies))    
    
# publication을 query로 받음
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

# cit를 query로 받음(그러나 query 문자를 변환하는 과정 필요함)
def get_weather(query):
    query = urllib.parse.quote(query)
    url = weather_url.format(query, we_appID)
    response = requests.get(url)
    data = response.content
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"DESC": parsed["weather"][0]["description"],
                  "temp": parsed["main"]["temp"],
                  "city": parsed["name"], 
                   "country": parsed['sys']['country']}
    return weather

def get_rate(frm, to):
    response = requests.get(currency_url)
    data = response.content
    parsed = json.loads(data).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())

if __name__ == '__main__':
    app.run(port=5000, debug=True)