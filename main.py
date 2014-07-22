from LollaWebScraper import LollaWebScraper
from EchonestSupplement import EchonestSupplement
import GeneratePlots

import json, argparse

# TODO: We can inspect the headers of requests to get this automatically
RATE_LIMIT=120

def generate_first_round_data(arg):
    '''Get the first round of data: this is the data directly from Lolla's website'''
    full_data = {}

    if (arg.load):
        # Load a JSON file if we specify it
        with open(arg.load, 'rb') as fp:
            full_data = json.load(fp)
    else:
        # Otherwise we'll just get the thing now
        scraper = LollaWebScraper("http://www.lollapalooza.com/2014-artist-list/")

        for artist, data in scraper.scrape():
            full_data[artist] = data
            print(u"Processed round one {0}".format(artist))

    return full_data

def generate_second_round_data(first_round_data):
    '''Get the second round: this is supplementary data from the Echonest API'''
    echo = EchonestSupplement(RATE_LIMIT)
    for datum in first_round_data.keys():
        new_attributes = echo.get_from_artist(datum)
        for attr in new_attributes:
            first_round_data[datum][attr] = new_attributes[attr]

        print(u"Processed round two {0}".format(datum))

    return first_round_data

def main(arg):
    if (int(arg.dataround) < 2):
        first_round = generate_first_round_data(arg)
        second_round = generate_second_round_data(first_round)
        # Save what we have
        with open(arg.save, 'wb') as fp:
            json.dump(second_round, fp)

    else:
        # Load a JSON file if we specify it
        with open(arg.load, 'rb') as fp:
            second_round = json.load(fp)

    # Generate plots
    GeneratePlots.generate(second_round)

    #print([v[0] for v in sorted(second_round.items(), key=lambda (k,v): v['fans'])])

if __name__=="__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Lollapalooza data analysis')
    parser.add_argument('--load')
    parser.add_argument('--save')
    parser.add_argument('--dataround')

    arg = parser.parse_args()

    main(arg)
