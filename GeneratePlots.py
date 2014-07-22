import numpy as np
import matplotlib.pyplot as plt

def generate(data_set):
    fans = [data_set[v]['fans'] for v in sorted(data_set)]
    fans_normalized = [float(v)/max(fans) for v in fans]
    popularity = [data_set[v]['popularity'] for v in sorted(data_set)]

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

    autolabel(rects1)
    autolabel(rects2)

    plt.show()