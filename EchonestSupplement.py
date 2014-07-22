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
        self.__block_until_callable()
        try:
            attributes = {}
            curart = artist.Artist(_artist)

            attributes['terms'] = [v['name'] for v in curart.terms[0:5]]
            attributes['hotttnesss'] = curart.hotttnesss
            attributes['familiarity'] = curart.familiarity

            return attributes
        except util.EchoNestAPIError: 
            # If the band is hipster enough echonest may not have it
            return None