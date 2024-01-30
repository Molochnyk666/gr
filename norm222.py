import json
from itertools import product
from itertools import chain
import itertools 
import spacy
from normalize import normalize_text
from sentence_transformers import SentenceTransformer, util
import numpy
from color import Color
from material import Material




class category_filter:
    materialDetect = Material("materials.json")
    colorDetect = Color("clear_respons_35.json")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    normalizer = normalize_text()
    nlp = spacy.load('en_core_web_lg')

    def __init__(self,path= None):
        if path != None:
            self.path_to_file = path
            try:
                with open(self.path_to_file,"r") as file:
                    self.filter = json.load(file)
            except Exception as e:
                print(self.path_to_file)
                print(e.with_traceback())
        else:
            self.path_to_file = None
            self.filter = {}

    def add_word_to_filter(self,category,words,anti_word = None):
        if category not in self.filter:
            raise Exception("No such category {}".format(category))
        new_word = {} 
        if not self.word_in_category(category,words) and category_filter._validate_word(words):
            new_word["content"] = words
            if anti_word!= None and category_filter._validate_word(words):
                new_word["anti_word"] = anti_word
        else: 
            raise Exception("{} already in filter".format(words))
        self.filter[category]["filter_words"].append(new_word)

    def in_category(self,category,word):
        try:
            for word_in_filter in self.filter[category]["filter_words"]:
                if word_in_filter["content"] == word:
                    return True
            return False
        except Exception as e:
            print(e)
            print(word_in_filter)

    def word_in_category(self,category,word):
        for word_in_filter in self.filter[category]["filter_words"]:
            if type(word_in_filter["content"]) == type(word):
                if type(word_in_filter["content"]) == list:
                    if len(word_in_filter["content"]) == len(word):
                        for temp in word_in_filter["content"]:
                            if temp not in word:
                                return False
                        return True
                    else:
                        return False
                else:
                    if word_in_filter["content"] == word:
                        return True
            else:
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
            if word == "%" or word == "-" or word =="'":
                return True
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
    
    def all_next_filters(self):
        res = list()
        for cat in self.categoryes():
            if  "next_filter" in self.filter[cat]:
                res.append((cat,category_filter(self.filter[cat]["next_filter"])))
        return res


    def metrick(flgs):
        res= {}
        total = 0 
        for item in flgs:
            if item["category"] in res:
                res[item["category"]] += item["score"]
            else:
                res[item["category"]] = item["score"]
            total += item["score"]

        for key in res: 
            res[key] = res[key]/total
        return res

    # def merge_metrics(title_metrick,desc_metrick):
    #     temp = filter(title_metrick,lambda x: x[1] == title_metrick[0][1])
    #     res = list()
    #     for item in temp:
    #         res.append([item[0],item[1] + sum([i[1] for i in filter(lambda x: x[0] == item[0],desc_metrick)])/3])
    #     return res

    


    def find_category(self,obj):
        norm = category_filter.normalizer.normalize(obj)
        title_tags = self.find_tags(norm,"TITLE")
        desc_tags = self.find_tags(norm,"DESCRIPTION")
        for tag in desc_tags:
            tag["score"] = tag["score"]/3
        title_metrick = list(category_filter.metrick(title_tags).items())
        desc_metrick = list(category_filter.metrick(desc_tags).items())
        if len(title_metrick) == 0:
            if len(desc_metrick) == 0:
                vector_tags_title = self.vectors2(norm,"TITLE")
                if vector_tags_title["score"] < 0.1:
                    return self.vectors2(norm,"DESCRIPTION")
                else:
                    return vector_tags_title
            else:
                desc_metrick.sort(key= lambda x: x[1],reverse=True)
                return {"category":desc_metrick[0][0],"title_tags":title_tags,"desc_tags":desc_tags,"type":"custom"}
        elif len(title_metrick)>1:
            title_metrick.sort(key= lambda x: x[1],reverse=True)
            if title_metrick[0][1] == title_metrick[1][1]:
                merge_metrick = list(category_filter.metrick(title_tags + desc_tags).items())
                merge_metrick.sort(key= lambda x: x[1],reverse=True)
                return {"category":merge_metrick[0][0],"title_tags":title_tags,"desc_tags":desc_tags,"type":"custom"}
            else:
                return {"category":title_metrick[0][0],"title_tags":title_tags,"desc_tags":desc_tags,"type":"custom"}
        else:
            return {"category":title_metrick[0][0],"title_tags":title_tags,"desc_tags":desc_tags,"type":"custom"}


    def vectors(self,text):

        res = {}
        flags = []
        for category in self.categoryes():
                for word in self.words(category):
                    if category_filter.find_antiword(text,word):
                        continue
                    if isinstance(word["content"],list):
                        doc1 = category_filter.nlp(" ".join(word["content"]))
                    else:
                        doc1 = category_filter.nlp(word["content"])
                    doc = category_filter.nlp(text["text"])
                    for chunk in doc.noun_chunks:
                        flags.append(tuple([category,chunk.similarity(doc1)**2]))
        flags = sorted(flags,key = lambda x: x[1],reverse=True)[0:8]
        for item in flags:
            if item[0] in res:
                res[item[0]] += item[1]
            else:
                res[item[0]] = item[1]
        return sorted(res.items(),key=lambda x: x[1],reverse = True)[0] 
        
                
    def vectors2(self,obj,key):
        text = obj[key]
        res = []
        for category in self.categoryes():

            #фильтр на материалы и цвет
            color_key = category_filter.colorDetect.detect(category)
            if color_key:
                if not category_filter.colorDetect.has_color(obj,color_key):
                    continue
                else:
                    res.append({"category":category,"word":color_key,"score":2,"type":"color"})
            material_key = category_filter.materialDetect.detect(category)
            if material_key:
                if not category_filter.materialDetect.has_material(obj,material_key):
                    continue
                else:
                    res.append({"category":category,"word":material_key,"score":2,"type":"material"})


            for word in self.words(category):
                if category_filter.find_antiword(text,word):
                    continue
                if isinstance(word["content"],list):
                    text1 = category_filter.nlp(" ".join(word["content"]))
                else:
                    text1 = category_filter.nlp(word["content"])
# Tokenize and encode the texts
            try:
                embeddings1 = category_filter.model.encode([text1], convert_to_tensor=True)
                embeddings2 = category_filter.model.encode([text["text"]], convert_to_tensor=True)
            except:
                print({"content":word["content"],"text":[text1]})

            
# Calculate the cosine similarity between the embeddings
            cosine_scores = util.cos_sim(embeddings1, embeddings2)
            res.append({"category":category,"word":word["content"],"score":cosine_scores,"type":"SBERTA"})
        try:
            return sorted(res,key=lambda x: x["score"],reverse = True)[0]
        except:
            if res == []:
                return {"category":"NO CAT","word":None,"score":1,"type":"SBERTA"}
            else:
                raise Exception
    


    # def find_category(self,obj):
    #     title_tags= []
    #     norm = category_filter.normalizer.normalize(obj)
    #     print(self.find_tags(norm.get("TITLE")))
    #     title_tags =[x.items() for x in category_filter.metrick(self.find_tags(norm.get("TITLE")))]
    #     if len(title_tags) == 0:
    #         return category_filter.vectors(norm["TITLE"])
    #     else:
    #         buf = sorted(title_tags,key = lambda x: x[1])
    #         if len(buf) == 1:
    #             return buf[0][0]
    #         else:
    #             if buf[0][1] == buf[1][1]:
    #                 desc_tags = [x.items() for x in category_filter.metrick(self.find_tags(norm.get("DESCRIPTION")))]
    #                 merge_mtric = category_filter.merge_metrics(title_tags,desc_tags)
    #                 return sorted(merge_mtric,lambda x: x[1],reverse=True)[0]
            


        # tags = {}
        # norm = category_filter.normalizer.normalize(obj)
        # for key in norm:
        #     tags.setdefault(key,category_filter.metrick(self.find_tags(norm.get(key))))
        #     if len(tags[key]) != 0: 
        #         buf = sorted(tags[key].items(),key = lambda x: x[1])
        #         if buf[0][1] != buf[1][1]:
        #             return buf[0][0]
                
        # return self.vectors(obj["TITLE"])


    # def vectors(self,text):

    #     res = {}
    #     flags = []
    #     for category in self.categoryes():
    #             for word in self.words(category):
    #                 if category_filter.find_antiword(text,word):
    #                     continue
    #                 if isinstance(word["content"],list):
    #                     doc1 = category_filter.nlp(" ".join(word["content"]))
    #                 else:
    #                     doc1 = category_filter.nlp(word["content"])
    #                 doc = category_filter.nlp(text["text"])
    #                 for chunk in doc.noun_chunks:
    #                     flags.append(tuple([category,chunk.similarity(doc1)**2]))
    #     flags = sorted(flags,key = lambda x: x[1],reverse=True)[0:8]
    #     for item in flags:
    #         if item[0] in res:
    #             res[item[0]] += item[1]
    #         else:
    #             res[item[0]] = item[1]
    #     return sorted(res.items(),key=lambda x: x[1],reverse = True)[0] 



    def find_tags(self,obj,key):
        text = obj[key]
        flags = []
        flat_text = text["full_text"]
        for category in self.categoryes():

            #фильтр на материалы и цвет
            color_key = category_filter.colorDetect.detect(category)
            if color_key:
                if not category_filter.colorDetect.has_color(obj,color_key):
                    continue
                else:
                    flags.append({"category":category,"word":color_key,"score":2,"type":"color"})
            material_key = category_filter.materialDetect.detect(category)
            if material_key:
                if not category_filter.materialDetect.has_material(obj,material_key):
                    continue
                else:
                    flags.append({"category":category,"word":material_key,"score":2,"type":"material"})



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