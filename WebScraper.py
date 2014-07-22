class WebScraper:
    '''Base WebScraper class, don't use directly'''
    def __init__(self):
        raise NotImplementedError()

    def scrape(self):
        '''This function is a generator that yields scraped data on each call'''
        raise NotImplementedError()