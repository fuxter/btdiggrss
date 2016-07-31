#! /usr/bin/env python

import os
import sys

import web
from feedgen.feed import FeedGenerator

from engines import DIGBTSearchEngine

web.config.debug = True

urls = (
    '/(.+)/', 'search'
)


class search:
    def GET(self, query):

        engine = DIGBTSearchEngine(query=query)

        feed = FeedGenerator()
        feed.title(query)
        feed.link(href=engine.url)
        feed.description(query)

        for torrent in engine.torrents:
            entry = feed.add_entry()
            entry.id(torrent['id'])
            entry.title(torrent['title'])
            entry.link(href=torrent['url'])

        web.header('Content-Type', 'application/rss+xml')
        return feed.rss_str()


if __name__ == "__main__":
    sys.argv += (os.environ.get('PORT', 8080),)
    app = web.application(urls, globals())
    app.run()
