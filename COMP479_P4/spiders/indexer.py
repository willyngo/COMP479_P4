# -*- coding: utf-8 -*-

import glob
import os.path
import json


class Indexer():
    FILEPATH = '../downloaded_pages/'
    
    corpus = []
    tfidf_corpus = []
    tf_dict = {}
    df_dict = {}
    index = {}
    
    def __init__(self):
        tf_dict = {}
        df_dict = {}
        index = {}
        
    def put_in_final_index(self, term_list):
        # term : df, [(doc_id, tf), (doc_id, tf), (doc_id, tf), ...]
        for term in term_list:
            df = len(self.tf_dict[term])
            tf_list = self.tf_dict[term]
            sorted_tf = sorted(tf_list, key=lambda tup: tup[1], reverse=True)
            entry = df, sorted_tf
            
            self.index[term] = entry
                    
        # add to final index
    
    def put_in_tf(self, doc_id, term_list):
        for term in term_list:
            # if term is new, add to entry
            if term not in self.tf_dict:
                new_list = [(doc_id, 1)]
                self.tf_dict[term] = new_list
            else:
                # contains the list of tuples (doc_id, tf) for given term
                id_tf_list = self.tf_dict[term]

                # If term already exist but on new doc id, add new tuple
                seen = [x for x, y in enumerate(id_tf_list) if y[0] == doc_id]
                if not seen:
                    new_tup = (doc_id, 1)
                    id_tf_list.append(new_tup)
                    
                # else update existing tuple
                else:
                    # find index of tuple
                    index = [x for x, y in enumerate(id_tf_list) if y[0] == doc_id].pop(0)
                    
                    # increment tf
                    new_tf = id_tf_list[index][1] + 1
                    
                    # make new tuple and update tf because can't do item assignment on tuple
                    new_tup = (doc_id, new_tf)
                    id_tf_list[index] = new_tup
                
                self.tf_dict[term] = id_tf_list
    
    def put_in_df(self, term_list):
        # remove duplicates so that we don't overcount df
        no_dup_list = list(dict.fromkeys(term_list))
        
        for term in no_dup_list:
            if term not in self.df_dict:
                self.df_dict[term] = 1
            else:
                self.df_dict[term] += 1
            
    def create_index(self):
        for file_names in glob.glob(os.path.join(self.FILEPATH, "*.txt")):
            with open(file_names, 'r',  encoding="utf-8") as file:
                
                # consume first line which is the url
                file.readline()
                
                # rest of the file is the text of the web page
                # so grab every word and put in a list
                words = file.read()
                term_list = words.split()
                doc_id = int(file_names[25:-4])
                
                # calculate tf
                self.put_in_tf(doc_id, term_list)
                self.put_in_final_index(term_list)
                
                # create corpus for rankings
                # each file's text has been split into a list and added into corpus[]
                self.corpus.append(term_list) 
                self.tfidf_corpus.append(words) 
                
    def write_to_file(self):
        path = "../outputs/final_index.txt"
        with open(path, 'w', encoding="utf-8") as index_out:
            output = "{\n"
            for item in self.index:
                output += "\t\'" + item + "\' : " + str(self.index[item]) + "\n"
            output += "}"
            
            index_out.write(output)
        
    def __str__(self):
        print(self.index)