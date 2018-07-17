#!/usr/bin/python2
# coding=utf-8
# @Date: 7/16/18
# @Author: HZH
"""

"""
import feedparser
from flask import Flask
from flask import render_template


app = Flask(__name__)
RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': 'https://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
