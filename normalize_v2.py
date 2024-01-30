import spacy
import json
from multiprocessing import Pool,cpu_count
from functools import partial
import time



def normalize_text(text,nlp):
    doc = nlp(text)
    chunks = []
    full_text = []
    for token in doc:
        if token.lower_ in ["lighter","lighters"]:
            full_text.append("lighter")
        else:
            word = token.lemma_.lower()
            if nlp.vocab[word].is_stop == False and token.pos_ not in  ("PUNCT",'SYM',"NUM"):
                full_text.append(word)
            
    for x in doc.noun_chunks:
        temp = []
        sub_doc = nlp(x.text)
        root = nlp(x.root.text)
        for token in sub_doc:
            word = token.lemma_.lower()
            if nlp.vocab[word].is_stop == False:
                temp.append(word )
        chunks.append(temp)
    return {"full_text":full_text,"chunks":chunks}

def short_text(text,nlp):
    text

def norm_with_flg(text,nlp,key):
    text["norm"] = normalize_text(text[key],nlp)
    return text

def norm_with_flg_v2(text,nlp):
    text["title_norm"] = normalize_text(text["Title"],nlp)
    text["desc_norm"] = normalize_text(text["Description"],nlp)
    return text

def fast_normalize_text(text_dict,func = norm_with_flg):
    nlp = spacy.load('en_core_web_lg')
    with Pool(cpu_count()) as p:
       res = p.map(partial(func,nlp = nlp),text_dict)
    return res




def main():
    with open(r"text_v2.json","r",encoding = "utf-8") as file:
        text_dict = json.load(file)
    start = time.time()
    res = fast_normalize_text(text_dict,norm_with_flg_v2)
    end = time.time()
    print(end - start)
    
    with open("result_v2.json","w+",encoding = "utf-8") as file:
        json.dump(res,file)





if __name__ == "__main__":
    main()

