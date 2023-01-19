import functions as fun
import Bayes
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import mysql.connector
path_ = None


def main():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='tweetsdb')

    cursor = cnx.cursor(buffered=True)
    query = "SELECT Tweet FROM tweets"
    cursor.execute(query)

    all_tweets = []
    for (text) in cursor:
        all_tweets.append(text)

    b = Bayes.BayesModel(all_tweets)
    b.creatingBayesianmodel()
    result = b.classification()

    # -----------------------   CSV file  --------------------------------- #

    # df = pd.read_csv(r'path_' + 'test.csv', encoding="utf8")
    # all_words = df['tweet'].tolist()

    # ---------------   Preprocessing    --------------- #
    # words = []
    # for m in all_words:
    #     m = str(m)
    #     tmp = []
    #     list_of_symbols = ['[', "'", ']','rt']
    #     for s in list_of_symbols:
    #         m = str(m)
    #         m = m.replace(s,'')
    #     tmp = m.split(', ')
    #     tmp = list(filter(None,tmp))
    #     words.append(tmp)

    # -------------------------------------------------------- #

    all_words_list = fun.join_list(all_tweets)

    list_w = []
    for words in all_words_list:
        words = fun.cleaning(words)
        words = fun.preprocessing(words)
        list_w.append(words)

    flat_list = []
    for sublist in list_w:
        for item in sublist:
            flat_list.append(item)

    flat_list = list(filter(None, flat_list))
    top_words = fun.top_words(flat_list)
    top_words.remove(('ti', 24))
    top_words.remove(('ame', 24))
    top_words = top_words[1:19]
    print(top_words)

    colors = ['cornflowerblue', 'royalblue']

    df2 = pd.DataFrame(top_words, columns=['word', 'quantity'])
    axes_ = df2.plot(x='word', y='quantity', legend=False, rot=0, kind='bar', color=colors)
    axes_.set_ylabel('quantity', fontsize=15, labelpad=30)
    axes_.set_xlabel('word', fontsize=15, labelpad=30)
    axes_.set_title('top words')
    plt.show()

    # -------------------------------------------------------

    count_result = Counter(result).most_common(3)
    df3 = pd.DataFrame(count_result, columns=['opinion', 'quantity'])
    axes_ = df3.plot(x='opinion', y='quantity', legend=False, rot=0, kind='bar')
    axes_.set_ylabel('quantity', fontsize=15, labelpad=30)
    axes_.set_xlabel('opinion', fontsize=15, labelpad=30)
    axes_.set_title('classification')
    plt.show()
    print('finish')


if __name__ == "__main__":
    main()

