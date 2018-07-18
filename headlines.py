#!/usr/bin/python2
# coding=utf-8
# @Date: 7/16/18
# @Author: HZH
"""

"""
import json, urllib, urllib2
import datetime
import feedparser
from flask import Flask
from flask import render_template, make_response
from flask import request


app = Flask(__name__)
RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': 'https://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }

DEFAULTS = {'publication': 'bbc',
            'city': 'London, UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=59f1d2440c5947d48f8d7e4f99670426"


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS.get(key)


@app.route("/")
def home():
    # get news
    publication = get_value_with_fallback("publication").lower()
    articles = get_news(publication)

    # get weather
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get exchange rate
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template("home.html", articles=articles, weather=weather, rate=rate, currencies=currencies,
                           currency_from=currency_from, currency_to=currency_to))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response





def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   "country": parsed['sys']['country']}
    return weather

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate, sorted(parsed.keys())




if __name__ == "__main__":
    app.run(host="0.0.0.0")
