import spacy
import json
class normalize_text:

    nlp = spacy.load("en_core_web_md")

    def __init__(self,path_to_cache):
        self.change = False
        self.path_to_cache = path_to_cache
        self.cache = normalize_text.load_cache(self.path_to_cache)

    def reload_cache(self,new_path):
        self.cache = normalize_text.load_cache(new_path)
        if self.change :
            self.dump_cache()
        self.path_to_cache = new_path
        self.change = False


    def get_from_cache(self,obj):
        return self.cache.get(obj["ID"])
    
    def add_to_cache(self,obj):
        self.cache.setdefault(obj["ID"],obj)

    def normalize(self,obj):
        res = {}
        temp = self.get_from_cache(obj["ID"])
        if temp:
            return temp 
        else:
            temp = {k: v for k, v in obj.items() if k != "ID"}
            for key in temp:
                doc = normalize_text.nlp(temp[key])
                chunks = []
                full_text = []
                for token in doc:
                    if token.lower_ in ["lighter","lighters"]:
                        full_text.append("lighter")
                    else:
                        word = token.lemma_.lower()
                        if normalize_text.nlp.vocab[word].is_stop == False and token.pos_ not in  ("PUNCT",'SYM',"NUM"):
                            full_text.append(word)
                        
                for x in doc.noun_chunks:
                    chunk = []
                    sub_doc = normalize_text.nlp(x.text)
                    root = normalize_text.nlp(x.root.text)
                    for token in sub_doc:
                        word = token.lemma_.lower()
                        if normalize_text.nlp.vocab[word].is_stop == False:
                            chunk.append(word )
                    chunks.append(chunk)
                res.setdefault(key,{"full_text":full_text,"chunks":chunks})
            self.add_to_cache(obj["ID"])
            return res

            
            
    def normalize_from_file(self,path_to_file):
        with open(path_to_file,"r",encoding="utf-8") as file:
            data = json.load(file)
        for obj in data:
            yield self.normalize(obj)

    def load_cache(path_to_cache):
        res = dict()
        with open(path_to_cache,"r",encoding="utf-8") as file:
            cache = json.load(file)
        for obj in cache:
            res[obj["ID"]]  = obj
        return res
            

    def dump_cache(self):
        pass

    def __del__():
        normalize_text.dump_cache()


