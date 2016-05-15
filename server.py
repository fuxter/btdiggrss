#! /usr/bin/env python

from urlparse import urlparse, parse_qs

import lxml.html
import requests
import web
from feedgen.feed import FeedGenerator


BTDIGG = 'https://btdigg.org'


urls = (
    '/(.+)/', 'search'
)


class search:
    def GET(self, query):
        url = '{}/search?q={}'.format(BTDIGG, query)
        response = requests.get(url)
        document = lxml.html.document_fromstring(response.text, base_url=BTDIGG)
        document.make_links_absolute()

        feed = FeedGenerator()
        feed.title(query)
        feed.link(href=url)
        feed.description(query)

        for torrent in document.xpath('//table')[2].xpath('./tr'):
            url = torrent.xpath('.//a')[0].get('href')
            if url == BTDIGG:
                continue
            entry = feed.add_entry()
            entry.id(parse_qs(urlparse(url).query)['info_hash'][0])
            entry.title(torrent.xpath('.//a')[0].text)
            entry.link(href=url)

        web.header('Content-Type','application/rss+xml')
        return feed.rss_str()


if __name__ == "__main__":
    import os, sys
    sys.argv += (os.environ.get('PORT', 8080),)
    app = web.application(urls, globals())
    app.run()
