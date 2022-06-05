# -*- coding: utf-8 -*-
"""Wikipedia Movie Plots-Grouping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rBCs_c7iQD5QBvZLRxIFj3SlwkUo2pQQ
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
# import numpy as np 
import re
import string 
import nltk
nltk.download('punkt')
# import word_tokenize & FreqDist from NLTK
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("./drive/MyDrive/Semester8/STBI/wiki_movie_plots_deduped.csv", index_col=0)

df.info

df.describe(include=object)

df.isna().sum()

result = df.drop(['Origin/Ethnicity', 'Director', 'Cast', 'Wiki Page'], axis = 1)

result

print(str(result.describe(include=object)))

result =result.drop_duplicates('Plot')
result.describe()

# remove number
def remove_number(text):
    return  re.sub(r"\[0-9]+", "", str(text))
 
result['Plot'] = result['Plot'].apply(remove_number)

# remove punctuation
def punctuation(txt):
  return re.sub(r"[^\w\s]","", str(txt))

result['Plot'] = result['Plot'].apply(punctuation)

# tokenization
def word_tokenize_wrapper(text):
  return word_tokenize(text)
result = result['Plot'].apply(word_tokenize_wrapper)

#stopword removal
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
print(sw_nltk)
def stopword(text):
  words = [word for word in text if word.lower() not in sw_nltk]
  return words
result = result.apply(stopword)

result

#normalization
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
def lemma(text):
  lemmatizer = WordNetLemmatizer()
  Output= [lemmatizer.lemmatize(words_sent) for words_sent in text]
  return Output
result = result.apply(lemma)

result.head()

from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf(data):
    tfidf = TfidfVectorizer( stop_words='english',use_idf=True)
    tfidf_matrix = tfidf.fit_transform(data)
    return tfidf_matrix

from sklearn.feature_extraction.text import TfidfVectorizer

# Create TfidfVectorizer object
vectorizer = TfidfVectorizer()

# Generate matrix of word vectors
tfidf_matrix = vectorizer.fit_transform(df['Plot'])

# Print the shape of tfidf_matrix
print(tfidf_matrix.shape)

# in order to explore which documents have more similar respresentaiton, consine simliartiy can be used
from sklearn.metrics.pairwise import linear_kernel
cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix).flatten()

from collections import Counter

# vocabulary
docs = df.values
tokenized_docs = df.values
vocab = Counter()
for token in tokenized_docs:
    vocab.update(token)

len(vocab)

#word embedding with word2vec
from gensim.models import Word2Vec

model1 = Word2Vec(sentences=result, workers=1, seed=42)

vectorized_docs = vectorize(df, model = model1, strategy="average")
len(vectorized_docs), len(vectorized_docs[0])

from ds_utils.clustering import vectorize, mbkmeans_clusters
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score

def mbkmeans_clusters(X, k, mb=500, print_silhouette_values=False):
    """Generate clusters.

    Args:
        X: Matrix of features.
        k: Number of clusters.
        mb: Size of mini-batches. Defaults to 500.
        print_silhouette_values: Print silhouette values per cluster.

    Returns:
        Trained clustering model and labels based on X.
    """
    km = MiniBatchKMeans(n_clusters=k, batch_size=mb).fit(X)
    print(f"For n_clusters = {k}")
    print(f"Silhouette coefficient: {silhouette_score(X, km.labels_):0.2f}")
    print(f"Inertia:{km.inertia_}")

    if print_silhouette_values:
        sample_silhouette_values = silhouette_samples(X, km.labels_)
        print(f"Silhouette values:")
        silhouette_values = []
        for i in range(k):
            cluster_silhouette_values = sample_silhouette_values[km.labels_ == i]
            silhouette_values.append(
                (
                    i,
                    cluster_silhouette_values.shape[0],
                    cluster_silhouette_values.mean(),
                    cluster_silhouette_values.min(),
                    cluster_silhouette_values.max(),
                )
            )
        silhouette_values = sorted(
            silhouette_values, key=lambda tup: tup[2], reverse=True
        )
        for s in silhouette_values:
            print(
                f"    Cluster {s[0]}: Size:{s[1]} | Avg:{s[2]:.2f} | Min:{s[3]:.2f} | Max: {s[4]:.2f}"
            )
    return km, km.labels_

clustering, cluster_labels = mbkmeans_clusters(X=vectorized_docs, k=7, print_silhouette_values=True)
df_clusters = pd.DataFrame({
    "text": docs,
    "tokens": [" ".join(text) for text in tokenized_docs],
    "cluster": cluster_labels
})

df.iloc[0]['Plot']

from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud = WordCloud().generate(df.iloc[0]['Plot'])
plt.imshow(wordcloud, interpolation="bilinear")