# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:16:31 2020

@author: NgoWi
"""
import string
from bs4 import BeautifulSoup
from bs4.element import Comment
from spiders.indexer import Indexer
from rank_bm25 import BM25Okapi

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
    # line = txtfile.readline()
    
    # lines_arr = []
    # while line:
    #     if not line.startswith("\n"):
    #         lines_arr.append(line.strip())
    #     line = txtfile.readline()
        
    # print(lines_arr)


# filename = "page_0.txt"
# with open(filename, "r") as txtfile:
#     line = txtfile.read()
#     # t = text_from_html(line)
#     l = line.split()
#     print(l)
doc_id = 2
id_tf = "hello", 34
d = {"hello":[(0, 5), (1, 4), (2, 5)],
     "fe":[(0, 5), (1, 4), (2, 5)],
     "de":[(0, 5), (1, 4), (2, 5)],
     "dw":[(0, 5), (1, 4), (2, 5)],
     "sq":[(0, 5), (1, 4), (2, 5)]}
# print(d)
itf = d["hello"]
# new_tf = itf[doc_id][1] + 1
# new_tup = (doc_id, new_tf)
# d["hello"][doc_id] = new_tup

# if doc_id >= len(itf):
#     print("N")
# else:
#     print("Y")
# mystr = "{\n"
# for item in d:
#     mystr += "\t" + item + " : " + str(d[item]) + "\n"
    
# mystr += "}"
# print(mystr)
# doc_id = 10
# s = [(0, 6), (1, 15), (3, 5), (7, 5), (2, 1), (4, 41), (5, 6), (8, 46), (9, 67), (6, 1)]
# se = sorted(s, key=lambda tup: tup[1], reverse=True)
# # print(se)
# seen = [x for x, y in enumerate(s) if y[0] == doc_id]
# if seen:
    # print("Y")

# s = "page_0.txt"
# print(s[5:-4])


corpus = [
    "Hello there windy windy windy good man!",
    "It is quite windy in London",
    "How is the london london weather today?"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]
# print(tokenized_corpus)
bm25 = BM25Okapi(tokenized_corpus)

query = ("windy london").split()

doc = list(bm25.get_scores(query))

top_15 = []
for i in range(3):
    index = doc.index(max(doc))
    top_15.append(doc.pop(index))
print(top_15)
print(doc)

# index = Indexer()
# index.create_index()
# index.write_to_file()

# s = 4,5
# s[1] += 1
# print(s)
# def is_a_but_not_in_footer(tag):
#     return tag.name == ' "footer" in tag.parents

# with open("../test_sites/test_site_1.html", "r") as testsite:
#     mysoup = BeautifulSoup(testsite, "html.parser")
#     links = mysoup.select('a[href]')
#     clean_links = ['http://example.com/elsie']
#     # for link in links:
#     #     if not link.find_parent("footer"):
#     #         url = link["href"]
#     #         if url not in clean_links:
#     #             clean_links.append(url)
#     print(links)










