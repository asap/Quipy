import os.path
import re
import urlparse

import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from quote.models import Quote

class Command(BaseCommand):

    args = 'movie-short-name'
    help = ('Populate the Quotes database by scraping The Movie Quotes Database\n\n'
            'The "movie-short-name" argument is the last part of the URL from\n'
            'any movie at http://www.moviequotedb.com/')

    URL_ROOT = 'http://www.moviequotedb.com/movies'

    def _massage_arg(self, movie_name):
        # the user might have given "http://.../foo.html"
        movie_name = urlparse.urlsplit(movie_name).path
        movie_name = os.path.split(movie_name)[-1]

        if movie_name.endswith('.html'):
            movie_name = movie_name[:-5]

        return movie_name

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('required arugment "short-movie-name" missing')

        movie_name = self._massage_arg(args[0])
        url = '%s/%s.html' % (self.URL_ROOT, movie_name)

        page = requests.get(url)
        soup = BeautifulSoup(page.text)

        def quote_div(tag):
            # Match divs whose id attribute looks like a quote
            return bool(re.match(r'quote_\d+', tag.get('id', '')))

        # Build a list of lists of dictionaries as:
        # {'speaker': 'Bob', 'text': 'Hello, world', 'source': 'http://...'}
        quotes = []
        for quote_wrapper in soup.find_all('div', 'quote'):
            quote = quote_wrapper.find(quote_div)
            source = '%s/%s/%s.html' % (self.URL_ROOT, movie_name, quote['id'])
            if quote.string:
                quotes.append([{
                    'speaker': None,
                    'text': quote.string,
                    'source': source,
                }])
            else:
                quote = u''.join(map(unicode, quote.contents))
                quote = quote.replace('<br/>', '')
                parts = []
                for match in re.finditer(r'<b>(?P<speaker>.*?)</b>:(?P<text>.*)', quote):
                    parts.append({
                        'speaker': match.group('speaker'),
                        'text': match.group('text').strip(),
                        'source': source,
                    })
                quotes.append(parts)

        # Roll up our expanded data structure to fit into
        # the current model. If in the future the model
        # accommodates individual speakers, we can handle
        # that with changes to this part only.
        for quote in quotes:
            source = quote[0]['source']
            if Quote.objects.filter(source=source).exists():
                continue

            text = []
            for line in quote:
                if line['speaker']:
                    text.append(
                        '<strong>%s:</strong> %s' % (line['speaker'], line['text']))
                else:
                    text.append(line['text'])
            text = '<br/>'.join(text)

            Quote(source=source, text=text).save()

