import functions as fun
import classificationAlgorithm
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import mysql.connector
import re

from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

path_ = None

def main():

    # ---------------   connecting to MySQL database  --------------- #

    cnx = mysql.connector.connect(user='', password='',
                                  host='',
                                  database='')

    cursor = cnx.cursor(buffered=True)
    query = "SELECT Tweet FROM tweets"
    cursor.execute(query)

    all_tweets = []
    for (text) in cursor:
        all_tweets.append(text)


    # ---------------   classification  --------------- #

    b = classificationAlgorithm.Model(all_tweets)
    b.creatingModel()
    result = b.classification()

    cursor.execute("SELECT Id, Sentiment FROM tweets")
    i = 0
    for row in cursor.fetchall():
         query = "UPDATE tweets SET Sentiment = {} WHERE Id = {};".format(int(result[i]), row[0])
         cursor.execute(query)
         cnx.commit()
         i = i + 1


    # ---------------   wordmap  --------------- #

    list_w = []
    for sentance in all_tweets:
        sentance = str(sentance)
        sentance = fun.cleaning(sentance)
        sentance = fun.preprocessing(sentance)
        list_w.append(sentance)

    flat_list = []
    for sublist in list_w:
        for item in sublist:
            flat_list.append(item)

    flat_list = list(filter(None, flat_list))
    top_words = fun.top_words(flat_list)

    wordmap_words = []
    for wordcount in top_words:
        wordmap_words.append(wordcount[0])

    x,y,c = zip(*np.random.rand(30,3)*4-2)
    norm=plt.Normalize(-2,2)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#00ACEE","#008BC0","#E66C37"])

    wordcloud = WordCloud(width=800, height=400, max_font_size=100, background_color="white", colormap = cmap).generate(str(wordmap_words))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


    # ---------------   classification result  --------------- #

     count_result = Counter(result).most_common(3)
     df3 = pd.DataFrame(count_result, columns=['opinion', 'quantity'])
     axes_ = df3.plot(x='opinion', y='quantity', legend=False, rot=0, kind='bar')
     axes_.set_ylabel('quantity', fontsize=15, labelpad=30)
     axes_.set_xlabel('opinion', fontsize=15, labelpad=30)
     axes_.set_title('classification')
     plt.show()

if __name__ == "__main__":
    main()

