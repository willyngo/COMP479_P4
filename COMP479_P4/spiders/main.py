# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:06:18 2020

@author: NgoWi
"""

from indexer import Indexer
from concordia_spider import MyCrawler
import scrapy
from scrapy.crawler import CrawlerProcess
from query_machine import QueryMachine


def call_spider(limit):
    # polite crawling attributes
    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Concordia University - Concordia spider (wi_ng@concordia.live.ca)',
        'DOWNLOAD_DELAY': 2.0,
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPCACHE_ENABLED': True
        })
    
    # the int argument is the limit of pages to download
    process.crawl(MyCrawler, limit)
    
    # Code for the spider is in concordia_spider.py
    process.start()

def call_indexer():
    # once crawling is done, the extracted page are located in the 'downloaded_pages' folder
    # create index from downloaded pages
    index = Indexer()
    index.create_index()
    
    # final index located in outputs folder
    index.write_to_file()
    
    # query
    query_mach = QueryMachine(index.corpus, index.tfidf_corpus)
    
    
    # Change queries here as needed
    query_1 = "researcher research COVID-19 covid-19"
    query_2 = "department research environmental issue sustainability energy water conservation"
    
    challenge_query_1 = "water management sustainability Concordia"
    challenge_query_2 = "Concordia COVID-19 faculty"
    challenge_query_3 = "SARS-CoV Concordia faculty"
    
    # Function will print out list of top 15 doc ids
    # The doc ids correspond to the text files in the 'downloaded_pages' folders
    # for example: if list contains 43, this corresponds to page_43.txt.
    # The first line of the text file is the url of the webpage.
    query_mach.retrieve_doc(query_1)
    query_mach.retrieve_doc(query_2)
    
    query_mach.retrieve_doc(challenge_query_2)
    query_mach.retrieve_doc(challenge_query_2)
    query_mach.retrieve_doc(challenge_query_2)
    
    
    # I couldn't retrieve the document for tfidf but I can print the tf-idf calculations in this line below.
    # int input is doc id, uncomment line below to print tf-idf
    # query_mach.show_tfidf(0)



"""
IMPORTANT NOTE: 
If running main.py in the IDE, for some reason I can't run this the crawler more than once in one process.
To fix this, I restart the kernel of the IPython console and this allows me to run it again.
Altertivavely, running in it on the command line seems to work fine.
"""
def run():
    # num is the limit of document to download
    call_spider(100)
    call_indexer()


run()