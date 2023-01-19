import re
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import Counter

SYMBOLS = ' {}()[].,:;+-*/#&$...…|<>=~^!?”“’"'


def join_list(word_lists):
    all_words_list = []
    for sublist in word_lists:
        for item in sublist:
            all_words_list.append(item)
    return all_words_list


def preprocessing(text):
    tokenizer = TweetTokenizer()
    lm = WordNetLemmatizer()
    # ps = PorterStemmer()

    stop_words = set(stopwords.words('english'))

    text = re.sub(r'http\S+', '', text)
    text = tokenizer.tokenize(text.lower())
    text = [w for w in text if not w.lower() in stop_words]
    m = []
    for element in text:
        temp = ''
        for ch in element:
            if ch not in SYMBOLS:
                temp += ch
        m.append(temp)
    text = [lm.lemmatize(word) for word in m]
    # text = [ps.stem(word) for word in m]
    return text


def cleaning(text):
    text = text.lower()
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    text = re.sub("isn't", 'is not', text)
    text = re.sub("he's", 'he is', text)
    text = re.sub("wasn't", 'was not', text)
    text = re.sub("there's", 'there is', text)
    text = re.sub("couldn't", 'could not', text)
    text = re.sub("won't", 'will not', text)
    text = re.sub("they're", 'they are', text)
    text = re.sub("she's", 'she is', text)
    text = re.sub("There's", 'there is', text)
    text = re.sub("wouldn't", 'would not', text)
    text = re.sub("haven't", 'have not', text)
    text = re.sub("That's", 'That is', text)
    text = re.sub("you've", 'you have', text)
    text = re.sub("He's", 'He is', text)
    text = re.sub("what's", 'what is', text)
    text = re.sub("weren't", 'were not', text)
    text = re.sub("we're", 'we are', text)
    text = re.sub("hasn't", 'has not', text)
    text = re.sub("you'd", 'you would', text)
    text = re.sub("shouldn't", 'should not', text)
    text = re.sub("let's", 'let us', text)
    text = re.sub("they've", 'they have', text)
    text = re.sub("You'll", 'You will', text)
    text = re.sub("i'm", 'i am', text)
    text = re.sub("im", 'i am', text)
    text = re.sub("we've", 'we have', text)
    text = re.sub("it's", 'it is', text)
    text = re.sub("don't", 'do not', text)
    text = re.sub("that´s", 'that is', text)
    text = re.sub("I´m", 'I am', text)
    text = re.sub("it’s", 'it is', text)
    text = re.sub("she´s", 'she is', text)
    text = re.sub("he’s'", 'he is', text)
    text = re.sub('I’m', 'I am', text)
    text = re.sub('I’d', 'I did', text)
    text = re.sub("he’s'", 'he is', text)
    text = re.sub('there’s', 'there is', text)

    return text


def top_words(data):
    top = Counter(data).most_common(20)
    return top

# def tokenizer(text): #check
#     tokenizer=TweetTokenizer()
#     text_tokenizer = tokenizer.tokenize(text.lower())
#     return text_tokenizer

# def stopWords(text): #check
#     stop_words = set(stopwords.words('english'))
#     text_stopwords = [w for w in text if not w.lower() in stop_words]
#     return text_stopwords

# def filtration(text): #check
#     m = []
#     for element in text:
#         temp = ''
#         for ch in element:
#             if ch not in SYMBOLS: 
#                 temp += ch
#         m.append(temp)
#     return m

# def deleteLink(text): #check
#     return re.sub(r'http\S+', '', text)

# def lemmatizer(text): #check
#     lm = WordNetLemmatizer()
#     text = [lm.lemmatize(word) for word in text]
#     return text

# def stemmer(text):
#     ps = PorterStemmer()
#     text = [ps.stem(word) for word in text]
#     return text
