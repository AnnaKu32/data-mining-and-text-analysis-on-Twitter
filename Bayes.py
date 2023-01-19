import pandas as pd
import matplotlib.pyplot as plt
import functions as fun

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, roc_curve


class BayesModel:

    def __init__(self, all_tweets):
        self.all_tweets = all_tweets
        self.tfidf = TfidfVectorizer(smooth_idf=True)
        self.model = ComplementNB()

    def creatingBayesianmodel(self):
        df = pd.read_csv(r'path\IMDB Dataset.csv')

        # df = df.dropna()
        # df=df.astype(str)
        # df.fillna('', inplace=True)

        # drop out highly correlated features
        # cor_matrix = df.corr().abs()
        # upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(bool))
        # to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
        # df1 = df.drop(df.columns[to_drop], axis=1)

        dt = df['text'].apply(fun.cleaning)
        dt = df['text'].apply(fun.preprocessing)

        X = self.tfidf.fit_transform(df['text'])
        y = df['sentiment']

        my_dict = {'neutral': 0, 'positive': 1, 'negative': -1}
        y = [my_dict[zi] for zi in df['sentiment']]

        X_train, X_test, y_train, y_test=train_test_split(X, y, stratify=y, test_size=0.25, random_state=1)

        self.model.fit(X_train, y_train)
        predicted = self.model.predict(X_test)

        accuracy_score = metrics.accuracy_score(predicted, y_test)
        print('ComplementNB model accuracy is', str('{:04.2f}'.format(accuracy_score*100))+'%')
        print('------------------------------------------------')
        print('Confusion Matrix:')
        print(pd.DataFrame(confusion_matrix(y_test, predicted)))
        print('------------------------------------------------')
        print('Classification Report:')
        print(classification_report(y_test, predicted))

        # --------------------------------------------------------------------------------------------------------

        ComplementNB_prob = self.model.predict_proba(X_test)
        fpr1, tpr1, thresh1 = roc_curve(y_test, ComplementNB_prob[:,1], pos_label=1)

        random_probs = [0 for i in range(len(y_test))]
        p_fpr, p_tpr, _ = roc_curve(y_test, random_probs, pos_label=1)

        from sklearn.metrics import roc_auc_score
        auc_CNB = roc_auc_score(y_test, ComplementNB_prob[:,1])

        # plot roc curves
        plt.plot(fpr1, tpr1, linestyle='--', color='red', label='CNB Model')
        plt.plot(p_fpr, p_tpr, linestyle='--', color='pink')

        plt.title('ROC curve')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive rate')

        plt.legend(loc='best')
        plt.show()

    def classification(self):

        all_tweets = list(self.all_tweets)
        tweet_vector = self.tfidf.transform(list(zip(*all_tweets))[0])
        predict_ = self.model.predict(tweet_vector)

        return predict_










