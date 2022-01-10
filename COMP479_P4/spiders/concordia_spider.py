# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:44:45 2020

@author: NgoWi
"""

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from bs4.element import Comment


class MyCrawler(scrapy.Spider):
    name = "concordia_spider"
    start_urls = ["https://www.concordia.ca"]
    allowed_domains = ["concordia.ca"]
    
    ROBOTSTXT_OBEY = True
    USER_AGENT = 'Concordia University - Concordia spider (wi_ng@concordia.live.ca)'
    DOWNLOAD_DELAY = 5.0
    AUTOTHROTTLE_ENABLED = True
    HTTPCACHE_ENABLED = True
    
    DOC_LIMIT = 10 # limit of documents to be crawled/downloaded
    current_doc = 0 # current document number crawled
    already_crawled_urls = [] # list of urls of pages already crawled
    to_be_crawled_urls = [] # list of urls in queue to be crawled
    doc_id_url = []
    
    """
    Limit is how many pages to download before stopping
    """
    def __init__(self, limit):
        self.DOC_LIMIT = limit
        print("my limit: " + str(self.DOC_LIMIT))
    
    """
    SCRAPER
    filters so that crawler doesn't check the text and links in the footer and header
    """
    def __tag_visible(self, element):
        if element.find_parent("footer") or element.find_parent("header"):
            return False
        if element.parent.name in ['style', 'script', 'head', 'title', 'header', 'footer', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    """
    SCRAPER
    Grabs the text from html
    """
    def __text_from_html(self, soup):
        # soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.__tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)
    
    """
    CRAWLER
    Given the text body, writes the content to output file to be used by indexer later
    """
    def __download_page(self, soup, url):
        pagenum = self.current_doc
        filename = f'../downloaded_pages/page_{pagenum}.txt'
        
        clean_text = url + "\n"
        
        # removes newlines
        clean_text += self.__text_from_html(soup)
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(clean_text)
            
        self.current_doc += 1
    
    """
    SCRAPER
    Retrieves all links in a page but only limit to <a> links that are not in 
    the footer.
    """
    def __get_links(self, soup):
        links = soup.select("a[href]")
        
        for link in links:
            url = link["href"]
            if url.startswith("#") or url.startswith("http"):
                continue
            # do not put links from footer or header
            # print("LINK: " + str(link))
            if not link.find_parent("footer") or not link.find_parent("header"):
                
                # do not put url that already appears in the queues
                if url not in self.to_be_crawled_urls and url not in self.already_crawled_urls:
                    self.to_be_crawled_urls.append(url)
                    # print("ADDED to queue: " + url)
        
    """
    CRAWLER
    """
    def parse(self, response):
        if self.current_doc < self.DOC_LIMIT:
            print("processing: "+ response.url)
            
            # check if current url has already been crawled
            if response.url not in self.already_crawled_urls:
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # download body of web page             
                body = soup("body")[0]
                self.__download_page(soup, str(response.url))
                print("Successfully downloaded page: " + response.url)
                
                # add url to doc_id
                self.doc_id_url.append(str(response.url))
                
                # add to list of pages already crawled
                self.already_crawled_urls.append(response.url)
                
                # add <a> links to to crawl next
                self.__get_links(soup)
            
            # crawl next pages
            if len(self.to_be_crawled_urls) > 0:
                next_page = self.to_be_crawled_urls.pop(0)
                if next_page:
                    yield scrapy.Request(
                        response.urljoin(next_page),
                        callback=self.parse
                    )
