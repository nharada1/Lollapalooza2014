from pyechonest import config
# REMOVE THIS WHEN DISTRIBUTING, DO NOT USE IN PRODUCTION
config.ECHO_NEST_API_KEY="OWUCZMOWGOJF7VQIX"

from pyechonest import util
from pyechonest import artist
import time

# We use a class here because we want a cohesive way to keep track of the rate limit
class EchonestSupplement:
    def __init__(self, ratelimit):
        self.__rate_limit = ratelimit
        self.__sec_between_calls = 60.0 / float(ratelimit)
        self.__last_api_call = time.time()
        self.__timing_epsilon = 0.2

    def __block_until_callable(self):
        elapsed_since_last = abs(time.time() - self.__last_api_call)
        if (elapsed_since_last < self.__sec_between_calls):
            waittime = abs(elapsed_since_last - self.__sec_between_calls)
            time.sleep(waittime + self.__timing_epsilon)
            self.__last_api_call = time.time()

    def get_from_artist(self, _artist):
        attributes = {}
        attributes['hotttnesss'] = 0
        attributes['familiarity'] = 0
        attributes['terms'] = None

        try:
            curart = artist.Artist(_artist)

            self.__block_until_callable()
            attributes['terms'] = [v['name'] for v in curart.terms[0:3]]
            self.__last_api_call = time.time()

            self.__block_until_callable()
            attributes['hotttnesss'] = curart.hotttnesss
            self.__last_api_call = time.time()

            self.__block_until_callable()
            attributes['familiarity'] = curart.familiarity
            self.__last_api_call = time.time()

        except util.EchoNestAPIError as e: 
            # If the band is hipster enough echonest may not have it, but we also
            # might have somehow hit our rate limit
            print("Error accessing artist data: {0}".format(e))
        
        finally:
            return attributes 