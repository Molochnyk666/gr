import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
class Color:

    lemmatizer = WordNetLemmatizer()

    def __init__(self,config_file):
        with open(config_file,"r",encoding="utf-8") as file:
            self.colors = json.load(file)
     
    def detect(self,category):
        word_tokens = word_tokenize(category)
        lemmatized_words = [Color.lemmatizer.lemmatize(word).lower() for word in word_tokens]
        for key in self.colors:
            if key in lemmatized_words:
                return key
        return ""
    
    def has_color(self,obj,key):
        if obj["COLOR"]["text"] == None or obj["COLOR"]["text"] == "":
            return False
        else: 
            
            for color in self.colors[key]:
                word_tokens = word_tokenize(color)
                lemmatized_words = [Color.lemmatizer.lemmatize(word).lower() for word in word_tokens]
                if len(lemmatized_words) == 1: 
                    if lemmatized_words[0] in obj["COLOR"]["full_text"]:
                        return True
                    else:
                        continue
                else:
                    flg = True
                    for lem_word in lemmatized_words:
                        if lem_word not in obj["COLOR"]["full_text"]:
                            flg = False
                            break
                    if flg:
                        return True
            return False