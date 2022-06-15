# Comparison of TF-IDF and TF-IDF Group in Document Clustering Using FastText and Word2Vec

Document grouping is considered important in information retrieval that organizing, extracting features, and categorizing web documents according to their similarities. Determination of the similarity of the subject is done by looking at the shape and size of each word in the document. However, there are words in a document that appear many times but do not appear when the word is considered important. For that we need an approach that overcomes these problems, one of which is the use of the TF-IDF approach. 

## Method

### Dataset
Datasets that used on this experiments consist of two datasets:
1. Internet News Data with Readers Engagement
    This dataset contain articles from several well-known publishers and is listed based on popularity on the publisher's website
2. Wikipedia Movie Plots
    This dataset contains data on summary plot descriptions taken from Wikipedia.

### Data Preprocessing
Data will through process that can be used to convert raw data into an understandable format, namely through data preprocessing technique : 
1. Data cleaning 
    This process is used to address incomplete, imperfect or incorrect data. Data cleaning can be done in various ways, namely by identifying whether there are missing values so that they can be adjusted. Another technique is to delete duplicate data (the same value) or delete certain columns that are not needed.
2. Data reduction 
    This process is used to reduce the data held so that only the necessary data are obtained. One way that can be done to reduce data is to remove attributes that are not used in modeling.

### Text Preprocessing
Text Preprocessing is a stage that is used to process data, especially data in text form. Text preprocessing method that used on this experiment :
1. Case Folding. 
    This operation is used to convert all letters to lowercase. It aims to eliminate ambiguity between lowercase and uppercase letters in the text.
2. Stopwords Removal. 
    In communicating, especially through texts, certain words are often used to complete sentences, but if translated in a separate meaning, they do not have any meaning. These words are referred to as stopwords. Stopwords removal operations can be used to remove words that are included in stopwords so that it is possible to focus more on words that are more important and meaningful.
3. Tokenization. 
    The text to be studied needs to be broken down from sentences to word for word. The tokenization operation is needed to cut the text into smaller parts which are called tokens.
4. Lemmatization. 
    This operation is a process that is included in stemming but is based on a dictionary (dictionary) by utilizing the vocabulary of words to remove affixes from the text so that it can return to its basic form.

### TF-IDF
Term Frequency - Inverse Document Frequency or TF-IDF is a useful method for counting any commonly used words. The IDF method is a calcULation of how the terms are widely distributed in the collection of documents in question. In contrast to TF, where the frequency with which words appear, the higher the value, in IDF, the fewer the frequency with which words appear in the document, the greater the value

### Word Embedding
In the experiment for the TF-IDF Group, which on documents that have been clustered, it will require a vector of each word first to be used in making document clustering. The method used to convert words into vector representations is word embedding. Word embedding techniques that will be used on this research are FastText and Word2Vec.

### Document Clustering
Result from word embedding will give the result of each word that have been showed as vector. Each document have the vector of its words that have trained using Word2Vec and FastText model. To generate the vector out of them there are some approaches that can be used, one of them is using the average of the vectors that worked on short text. One method that can be used to form clusters is to use the K-Means clustering method.

## Experiment
The method used is divided into 3, namely: using the TF-IDF method, using the TF-IDF Group with Fast Text, and using the TF-IDF Group with Word2Vec. These three experiments has its characteristics and explanation and we can see the performance of TF-IDF on each methods by difference one from each other by there scenarios:
1. Using only TF-IDF
2. Using fast text and K-Means, where the results of the clustering of K-Means will be grouped using TF-IDF Group
3. Using Word2Vec and K-Means, where the results of the clustering of K-Means will be grouped using TF-IDF Group

## How to use code
For installation you need to Python 3.6 or later. To install this project on your local machine, 
you should run the following commands in the Terminal:

```sh
git clone https://github.com/letaresaragih/STBI-Project-1-1
cd Code
pip install .
```

##### Team & Member
Group Name
Anggota:
1. 12S18019 - Maria Puspita Sari Nababan   
2. 12S18064 - Letare Aiglien Saragih