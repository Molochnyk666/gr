import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class Material:

    lemmatizer = WordNetLemmatizer()

    def __init__(self,config_file):
        with open(config_file,"r",encoding="utf-8") as file:
            self.materials = json.load(file)
     
    def detect(self,category):
        if category in ['Paper clips','Advertising textiles','Kitchen textile sets','Silicone bracelets']:
            return False
        word_tokens = word_tokenize(category)
        lemmatized_words = [Material.lemmatizer.lemmatize(word).lower() for word in word_tokens]
        for key in self.materials:
            if key in lemmatized_words:
                return key
        return ""
    
    def has_material(self,obj,key):
        if obj["MATERIAL"]["text"] == None or obj["MATERIAL"]["text"] == "":
            return False
        else: 
            
            for material in self.materials[key]:
                word_tokens = word_tokenize(material)
                lemmatized_words = [Material.lemmatizer.lemmatize(word).lower() for word in word_tokens]
                if len(lemmatized_words) == 1: 
                    if lemmatized_words[0] in obj["MATERIAL"]["full_text"]  or lemmatized_words[0] in obj["TITLE"]["full_text"]:
                        return True
                    else:
                        continue
                else:
                    flg = True
                    for lem_word in lemmatized_words:
                        if lem_word not in obj["MATERIAL"]["full_text"] :
                            flg = False
                            break
                    if flg:
                        return True
                    
                    flg = True
                    for lem_word in lemmatized_words:
                        if lem_word not in obj["TITLE"]["full_text"] :
                            flg = False
                            break
                    if flg:
                        return True
            return False