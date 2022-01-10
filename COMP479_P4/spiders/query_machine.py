# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
from indexer import Indexer
import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

class QueryMachine:
    
    bm25 = None
    tfIdfVectorizer = None
    tfidf_list = []
    
    def __init__(self, corpus, tfidf_corpus):
        self.bm25 = BM25Okapi(corpus)
        self.tfIdfVectorizer = TfidfVectorizer(use_idf="True",stop_words= 'english')
        self.tfidf_list = self.tfIdfVectorizer.fit_transform(tfidf_corpus)
    
    """
    This method was an attempt to calculate tf-idf manually but I kept having problems
    so I decided to not to use it
    """
    def __get_tf_idf(self, query, indexer):
        tfidf_score = []
        tokenized_query = query.lower().split()
        corpus = indexer.corpus
        dictionary = indexer.index
        
        #initialize score table to 0
        for i in range(len(corpus)):
            tfidf_score.append(0)

        # If a doc is relevant to a query, an entry will update the tfidf_score list
        for token in tokenized_query:
            # entry = (df, [(doc_id, tf), (doc_id, tf), …])
            entry = dictionary[token]
            
            df = entry[0]
            idf = math.log(len(corpus)/float(df))
            
            # tf_list = [(doc_id, tf), (doc_id, tf), …]
            tf_list = entry[1]
            
            for item in tf_list:
                doc_id = item[0]
                corpus_select = corpus[doc_id]
                tf = item[1]
                
                total_words = len(corpus_select)
                tf_calc = tf/total_words
                
                tfidf = tf_calc * idf
                
                tfidf_score[doc_id] = tfidf
        
        return tfidf_score
    
    """
    I use the tfidf vectorizer class to calculate tf-idf properly
    The only problem was to find the 15 documents which I wasn't able to because
    I did not plan properly how to get it from using this library
    """
    def __get_top15_tfidf(self, query):
        
        # since I wasn't able to find the 15 documents for tf-idf, I just return
        # the list.
        return self.tfidf_list
        
    """
    Prints prints out the tf-idf for a given document. The index corresponds to the doc id
    """
    def show_tfidf(self, index):
        df = pd.DataFrame(self.tfidf_list[index].T.todense(), index=self.tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        print (df.head(15))
    
    """
    This function returns a list of document ids that are sorted by the highest bm25 score for 
    the given query.
    """
    def __get_top15_bm25(self, query):
        tokenized_query = query.lower().split()
        top_15 = []
        doc_1 = list(self.bm25.get_scores(tokenized_query))

        # grabs the index of the top 15 hits.
        # the index represents the pages
        for i in range(15):
            index = doc_1.index(max(doc_1))
            doc_1[index] = 0
            top_15.append(index)
        
        print("Top 15 pages for query using bm25: " + str(top_15))
    
    """
    This functions calls both function to return a list of doc_ids that have the highest score
    for the given query.
    
    I had initially planned on returning each list but I wasn't able to grab a list for the tf-idf so I
    ended up just printing the bm25 list
    """
    def retrieve_doc(self, query):
        top_15_bm25 = self.__get_top15_bm25(query)
        top_15_tfidf = self.__get_top15_tfidf(query)
        
        return top_15_bm25, top_15_tfidf
    