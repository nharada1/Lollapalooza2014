import numpy as np
import matplotlib.pyplot as plt
import json

from collections import Counter

def generate_bar_popularity(data_set):
    '''Look at the fans added popularity to echonest's internal rankings'''
    fans = [data_set[v]['fans'] for v in sorted(data_set)]
    fans_normalized = [float(v)/max(fans) for v in fans]
    popularity = [data_set[v]['hotttnesss'] for v in sorted(data_set)]

    def normpop(val):
        if val is None:
            return 0
        return float(val)/max(popularity)

    popularity_normalized = [normpop(v) for v in popularity]
    artists = [v for v in sorted(data_set)]

    N = 10

    ind = np.arange(N)  # the x locations for the groups
    width = 0.4         # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, fans_normalized[0:10], width, color='r')
    rects2 = ax.bar(ind+width, popularity_normalized[0:10], width, color='y')

    # add some
    ax.set_ylabel('Artist')
    ax.set_title('Popularity')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( artists, rotation=80 )

    ax.legend( (rects1[0], rects2[0]), ('Fans', 'Popularity') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%f'%height,
                    ha='center', va='bottom', rotation=90)

    #autolabel(rects1)
    #autolabel(rects2)

    plt.tight_layout()
    plt.show()

def generate_genre_plot(data_set):
    # Combine the tags into one big string to process via wordcloud
    big_string = ""
    big_terms = []
    for datum in data_set:
        cur_terms = data_set[datum]['terms']
        if cur_terms:
            str_terms = " ".join(cur_terms)
            big_string = big_string + ' ' + str_terms
            for term in cur_terms:
                big_terms.append(term)
    with open('outputs/wordcloud.txt', 'w') as f:
        f.write(big_string)

    # We want to count how many of each genre
    genre_count = Counter(big_terms).most_common()
    genre_usable = [v for v in genre_count if v[1] > 1]
    with open('genres.json') as f:
        genre_list = json.load(f)
    with open('outputs/genres_thisyear.txt', 'w') as f:
        f.write("subgenre,number,genre,\n")
        for genre in genre_usable:
            try:
                subgenres = genre_list[genre[0]]
                if len(subgenres) == 1:
                    f.write("{0},{1},{2},\n".format(genre[0], int(genre[1])*2, subgenres[0]))
                elif len(subgenres) == 2:
                    f.write("{0},{1},{2},\n".format(genre[0], int(genre[1]), subgenres[0]))
                    f.write("{0},{1},{2},\n".format(genre[0], int(genre[1]), subgenres[1]))
            except:
                pass

def generate(data_set):
    generate_bar_popularity(data_set)
    generate_genre_plot(data_set)