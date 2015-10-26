#! /usr/bin/env python


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
            entry = feed.add_entry()
            entry.id()
            entry.title(torrent.xpath('.//a')[0].text)
            entry.link(href=torrent.xpath('.//a')[0].get('href'))
        web.header('Content-Type','application/rss+xml')
        return feed.rss_str()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
