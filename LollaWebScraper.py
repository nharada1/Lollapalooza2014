from WebScraper import WebScraper
from bs4 import BeautifulSoup

import urllib2, re, dateutil.parser

class LollaWebScraper(WebScraper):
    '''LollaWebScraper class, scrapes from Lolla 2014\'s main site'''
    def __init__(self, base_address):
        self._base_address = base_address
        self._base_html = urllib2.urlopen(self._base_address).read()

        # Find the artist urls
        reg = "http://www\.lollapalooza\.com\/2014-artist\/[a-zA-Z\-]+\/"
        self._artist_urls = sorted(list(set(re.findall(reg, self._base_html))))

    def __get_artist(self, soup_object):
        '''Get this artists unicode name'''
        name_tags = soup_object.findAll(attrs={'class': 'js-artist-name'})
        # Get the only tag with this name
        name_tag = name_tags[0]
        name = name_tag.string

        return name

    def __get_stage(self, soup_object):
        '''Get stage name for this artist'''
        stage_tag = soup_object.findAll(attrs={'class': 'c--blue'})
        # There's only one possible stage, even for bands that play multiple times
        try:
            stage = stage_tag[0]
            stage_str = stage.string.strip()
            return stage_str
        except:
            # Some artists don't list a stage, somehow
            return None

    def __get_times(self, soup_object):
        '''Get start times and end times for artists'''
        times_tags = soup_object.findAll(attrs={'class': 'no-margin'})
        # Some artists play multiple times (mainly kid's stage)
        times_list = []
        for time_tag in times_tags:
            # Remove extra spaces by splitting on whitespace and joining
            dt_text = ' '.join(time_tag.string.split())
            date_text, time_text = dt_text.split('|')
            # We'll use our knowledge of the string format for this, but this is a fragile method
            # Remove the '-' and any extra spaces
            time_text = time_text.replace('-', '')
            time_text = time_text.strip()
            start_time, end_time, meridian = time_text.split()
            
            start_datetime = "{0}{1} {2}".format(date_text, start_time, meridian)
            end_datetime = "{0}{1} {2}".format(date_text, end_time, meridian)

            times_list.append((start_datetime, end_datetime))

        return times_list

    def __get_fans(self, soup_object):
        '''Get the number of fans for this artist'''
        fan_tag = soup_object.findAll(attrs={'class': 'count--fans'})
        # There can only be one fan count, so use that
        tag_str = fan_tag[0]

        # Potential trip-up here: BeautifulSoup is a mutable object, and as such the extract method we use
        # here will change the object for ALL future calls because objects are passed by assignment in Python.
        # We actually don't care about changing the DOM structure because it keeps our results the same anyway, but
        # if we did we'd have to properly clone the BeautifulSoup object, which it turns out we can't do using
        # copy.deepcopy and isn't supported at the time of writing. 
        # See: http://stackoverflow.com/questions/23057631/clone-element-with-beautifulsoup
        tag_str.span.extract()
        fans_tag = soup_object.findAll(attrs={'class': 'count--fans'})[0]
        fans = int(fans_tag.string.replace(',',''))

        return fans

    def scrape(self):
        '''This function is a generator that yields scraped data on each call'''
        for url in self._artist_urls:
            artist_dict = {}
            page_html = urllib2.urlopen(url).read()
            soup_object = BeautifulSoup(page_html)

            artist_dict['fans'] = self.__get_fans(soup_object)
            artist_dict['set_times'] = self.__get_times(soup_object)
            artist_dict['stage'] = self.__get_stage(soup_object)
            artist_name = self.__get_artist(soup_object)

            yield(artist_name, artist_dict)