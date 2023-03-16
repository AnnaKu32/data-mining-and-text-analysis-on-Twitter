import pandas as pd
import matplotlib.pyplot as plt
import functions as fun

from sklearn.linear_model import LogisticRegression

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score

path_to_database = r"./files/Reddit_Data.csv"

class Model:

    def __init__(self, all_tweets):
        self.all_tweets = all_tweets
        self.tfidf = TfidfVectorizer(smooth_idf=True)
        self.model = LogisticRegression(max_iter=1000)

    def creatingModel(self):
        df = pd.read_csv(path_to_database)
        df.dropna(inplace=True)

        df['clean_comment'].apply(fun.cleaning)
        df['clean_comment'].apply(fun.preprocessing)

        X = self.tfidf.fit_transform(df['clean_comment'])
        y = df['category']

        # my_dict = {'neutral': 0, 'positive': 1, 'negative': -1}
        # y = [my_dict[zi] for zi in df['category']]

        X_train, X_test, y_train, y_test=train_test_split(X, y, stratify=y, test_size=0.25, random_state=1)

        self.model.fit(X_train, y_train)
        predicted = self.model.predict(X_test)

        accuracy_score = metrics.accuracy_score(predicted, y_test)
        print('Model accuracy is', str('{:04.2f}'.format(accuracy_score*100))+'%')
        print('------------------------------------------------')
        print('Confusion Matrix:')
        print(pd.DataFrame(confusion_matrix(y_test, predicted)))
        print('------------------------------------------------')
        print('Classification Report:')
        print(classification_report(y_test, predicted))

        # --------------------------------------------------------------------------------------------------------

    def classification(self):

        all_tweets = list(self.all_tweets)
        tweet_vector = self.tfidf.transform(list(zip(*all_tweets))[0])
        predict_ = self.model.predict(tweet_vector)

        return predict_










