# -*- coding: utf-8 -*-
"""articles_data_word2vec_tf-idf group.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TJsPL-wGKNMpwKVyd4XQMDJ_DmAzYw5z

# Dataset 1: articles_dataset.csv

#### a. Import required libraries
"""

from google.colab import drive
drive.mount('/content/drive')

#import library
import os
import random
import re
import string

import nltk
import numpy as np
import pandas as pd

from gensim.models import Word2Vec

from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

from ds_utils.clustering import vectorize, mbkmeans_clusters
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score

nltk.download("stopwords")

SEED = 42
random.seed(SEED)
os.environ["PYTHONHASHSEED"] = str(SEED)
np.random.seed(SEED)

"""#### b. Data Preprocessing"""

import pandas as pd
df = pd.read_csv("./drive/MyDrive/STBI/Proyek/Dataset/articles_data.csv")
df.head()

df.shape

df.info()

# drop atribut 
df = df.drop(['Unnamed: 0', 'source_id', 'title', 'description', 'source_name', 'author', 'url', 'url_to_image', 'published_at', 'top_article', 'engagement_reaction_count', 'engagement_comment_count', 'engagement_share_count', 'engagement_comment_plugin_count'], axis = 1)

df.info()

# Checking duplicate value
print(str(df.describe(include=object)))

# remove duplicate value (text) in contenct attribute
df.drop_duplicates(subset=['content'], keep='last')

# Checking null value in attribute 
df.isna().sum()

#drop null value
df = df.dropna()

df

#saving the result
df.to_csv("./drive/MyDrive/STBI/Proyek/Dataset/clean_articles_data_word2vec.csv", index=True)

"""#### C. Text Preprocessing"""

# remove punctuation
def punctuation(txt):
  return re.sub(r"[^\w\s]","", str(txt))

df = df['content'].apply(punctuation)

import nltk
nltk.download('punkt')
# tokenization
def word_tokenize_wrapper(text):
  return word_tokenize(text)
df = df.apply(word_tokenize_wrapper)

#stopword removal
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
print(sw_nltk)
def stopword(text):
  words = [word for word in text if word.lower() not in sw_nltk]
  return words
df = df.apply(stopword)

#normalization
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
def lemma(text):
  lemmatizer = WordNetLemmatizer()
  Output= [lemmatizer.lemmatize(words_sent) for words_sent in text]
  return Output
df = df.apply(lemma)

#saving the rusult
df.to_csv("./drive/MyDrive/STBI/Proyek/Dataset/prepro_articles_data_word2vec.csv", index=True)

"""#### D. Word Embeding Using Word2Vec"""

# vocabulary
docs = df.values
tokenized_docs = df.values
vocab = Counter()
for token in tokenized_docs:
    vocab.update(token)

len(vocab)

vocab.most_common(10)

#word embedding with word2vec
model1 = Word2Vec(sentences=tokenized_docs, size = 100, workers=1, seed=42)

# test model
model1.wv.most_similar("moon", topn=5)

vectorized_docs = vectorize(df, model = model1, strategy="average")
len(vectorized_docs), len(vectorized_docs[0])

"""#### E. Generate and analyze clusters"""

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

clustering, cluster_labels = mbkmeans_clusters(X=vectorized_docs, k=50, print_silhouette_values=True)
df_clusters = pd.DataFrame({
    "text": docs,
    "tokens": [" ".join(text) for text in tokenized_docs],
    "cluster": cluster_labels
})

print("Top terms per cluster (based on centroids):")
for i in range(50):
    tokens_per_cluster = ""
    most_representative = model1.wv.most_similar(positive=[clustering.cluster_centers_[i]], topn=5)
    for t in most_representative:
        tokens_per_cluster += f"{t[0]} "
    print(f"Cluster {i}: {tokens_per_cluster}")

test_cluster = 48
most_representative_docs = np.argsort(
    np.linalg.norm(vectorized_docs - clustering.cluster_centers_[test_cluster], axis=1)
)
for d in most_representative_docs[:20]:
    print(docs[d])
    print("-------------")

docs

"""#### F. TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf(data):
    tfidf = TfidfVectorizer( stop_words='english',use_idf=True)
    tfidf_matrix = tfidf.fit_transform(data)
    return tfidf_matrix

# Let's create a matrix with tfidf for the column abstract
tfidf_matrix = tfidf(most_representative_docs.values.astype('U'))

# in order to explore which documents have more similar respresentaiton, consine simliartiy can be used
from sklearn.metrics.pairwise import linear_kernel
cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix).flatten()

# 10 most related documents indices
related_docs_indices = cosine_similarities.argsort()[:-11:-1]
print("Related Document:",related_docs_indices)

# Cosine Similarties of related documents
print("Cosine Similarites of related documents",cosine_similarities[related_docs_indices])

# Let's take a look at two most similar document
data.iloc[0]['content']

from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud = WordCloud().generate(data.iloc[0]['content'])
plt.imshow(wordcloud, interpolation="bilinear")
