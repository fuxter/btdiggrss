from urlparse import urlparse, parse_qs

import lxml.html
import requests


class BaseSearchEngine(object):

    url = None

    @property
    def torrent(self):
        raise NotImplementedError()


class BTDIGGSearchEngine(BaseSearchEngine):

    root = 'https://btdigg.org'

    def __init__(self, query):
        self.url = '{}/search?q={}'.format(self.root, query)

    @property
    def _document(self):
        response = requests.get(self.url)
        document = lxml.html.document_fromstring(
            response.text, base_url=self.root)
        document.make_links_absolute()
        return document

    @property
    def _elements(self):
        return (element for element in self._document.xpath(
            '//table')[2].xpath('./tr'))

    @property
    def torrents(self):
        for torrent in self._elements:
            url = torrent.xpath('.//a')[0].get('href')
            if url == self.root:
                continue
            yield {
                'url': url,
                'id': parse_qs(urlparse(url).query)['info_hash'][0],
                'title': torrent.xpath('.//a')[0].text,
            }


class DIGBTSearchEngine(BaseSearchEngine):

    root = 'http://www.digbt.org'

    def __init__(self, query):
        self.url = '{}/search/{}/'.format(self.root, query)

    @property
    def _document(self):
        response = requests.get(self.url)
        document = lxml.html.document_fromstring(
            response.text, base_url=self.root)
        document.make_links_absolute()
        return document

    @property
    def _elements(self):
        return (element for element in self._document.xpath('//tr'))

    @property
    def torrents(self):
        for torrent in self._elements:
            yield {
                'url': torrent.xpath('.//a/@href')[0],
                'id': parse_qs(torrent.xpath( './/a/@href')[1])['magnet:?xt'][0].split(':')[-1],
                'title': torrent.xpath('.//a/text()')[0],
            }
