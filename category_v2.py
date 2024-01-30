import json
from itertools import product
from itertools import chain
import itertools 



class category_filter:
    def __init__(self,path= None):
        if path != None:
            self.path_to_file = path
            with open(self.path_to_file,"r") as file:
                self.filter = json.load(file)
        else:
            self.path_to_file = None
            self.filter = {}

    def add_word_to_filter(self,category,words,anti_word = None):
        if category not in self.filter:
            raise Exception("No such category {}".format(category))
        new_word = {} 
        if not self.in_category(category,words) and category_filter._validate_word(words):
            new_word["content"] = words
            if anti_word!= None and category_filter._validate_word(words):
                new_word["anti_word"] = anti_word
        else: 
            raise Exception("{} already in filter".format(words))
        self.filter[category].append(new_word)

    def in_category(self,category,word):
        for word_in_filter in self.filter[category]:
            if word_in_filter["content"] == word:
                return True
        return False
    
    def delete_from_category(self,category,word):
        if category not in self.filter:
            raise Exception("No such category")
        for word_in_filter in self.filter[category]:
            if word_in_filter["content"] == word:
                self.filter[category].remove(word_in_filter)


    def add_new_category(self,category):
        if category in self.filter:
            raise Exception("{} already in the filter".format(category))
        else:
            self.filter[category] = []

    def _validate_word(word):
        if isinstance(word,str):
            if str.islower(word):
                return True
            else:
                raise Exception("The word-key must be in lowercase in {}".format(word))
        elif isinstance(word,list):
            for i in word:
                category_filter._validate_word(i)
            return True
        else:
            raise Exception("only str or list of strings")

    def add_anti_word(self,category,word,anti_word,typeUpdate = "single"):
        if category not in self.filter:
            raise Exception("No such category")
        if category_filter._validate_word(word) and category_filter._validate_word(anti_word):
            for item in self.filter[category]:
                if word == item["content"]:
                    if "anti_word" in item:
                        if isinstance(item["anti_word"],list):
                            if typeUpdate == "single":
                                item["anti_word"].append(anti_word)
                            elif typeUpdate == "many":
                                item["anti_word"] = item["anti_word"] + anti_word
                        else:
                            if typeUpdate == "single":
                                item["anti_word"] = [item["anti_word"],anti_word]
                            elif typeUpdate == "many":
                                item["anti_word"] = [item["anti_word"]] + anti_word
                    else:
                        item["anti_word"] = anti_word
                        
    def categoryes(self):
        return list(self.filter.keys())

    def words(self,category):
        if category not in self.filter:
            raise Exception("No such category")
        else: 
            return self.filter[category]["filter_words"]
            
    def remove_anti_word(self,filter,word,anti_word):
        pass
    def remove_all_anti_word(self,filter,word,anti_word):
        pass

    def delete_category(self,category):
        if category not in self.filter:
            raise Exception("No such category")
        else:
            self.filter.pop(category)
        
    def load_to_file(self,path=None):
        if [path,self.path_to_file]== [None,None]:
            raise Exception("no directory")
        elif path != None:
            with open(path,"w+") as file:
                json.dump(self.filter,file,indent=0)
        else:
            with open(self.path_to_file,"w+") as file:
                json.dump(self.filter,file,indent=0)
    
    def next_filter(self, category):
        return category_filter(self.filter[category]["next_filter"]) if "next_filter" in self.filter[category] else None


    def find_tag(self,text):
        pass
    
    def find_category(self,text):
        flags = []
        flat_text = text["full_text"]
        for category in self.categoryes():
            for word in self.words(category):
                if category_filter.find_antiword(text,word):
                    continue
                if isinstance(word["content"],list):
                    for noun_chunk in text["chunks"]:
                        flag = True 
                        for item in word["content"]:
                            if item not in noun_chunk:
                                flag = False
                                break
                        if flag:
                            flags.append({"category":category,"word":word,"score":len(word["content"])})
                        
                else:
                    for item in flat_text:
                        if item == word["content"]:
                            flags.append({"category":category,"word":word,"score":1})
        return flags       


    def decorator_function(func):
        def wrapper(arg1,arg2):
            if type(arg1) == list:
                return product(arg1,arg2)
            else:
                temp = list()
                temp.append(arg1)
                return product(temp,arg2)
        return wrapper
    
    def find_antiword(text,word):
        if "anti_word" in word:
            for anti_words in word["anti_word"]:
                if isinstance(anti_words,list):
                    for i in text["chunks"]:
                        flag = True
                        for anti_word in anti_words:
                            if anti_word not in i:
                                flag = False
                                break
                        if flag:
                            return True
                else:
                    decorated_product = category_filter.decorator_function(product)
                    for prod in decorated_product(word["anti_word"],text["full_text"]):
                        if prod[0] == prod[1]:
                            return True
        return False
    
    find_antiword.__code__.co_argcount