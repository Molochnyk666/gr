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


def norm_with_flg(text,nlp,key):
    text["norm"] = normalize_text(text[key],nlp)

def fast_normalize_text(text_dict):
    nlp = spacy.load('en_core_web_lg')
    with Pool(cpu_count()) as p:
        p.map(partial(norm_with_flg,nlp = nlp,key = "concat"),text_dict)


def main():
    with open(r"norm_text.json","r",encoding = "utf-8") as file:
        text_dict = json.load(file)
    start = time.time()
    fast_normalize_text(text_dict)
    end = time.time()
    print(end - start)
    with open("result.json","w+",encoding = "utf-8") as file:
        json.dump(text_dict,file)


if __name__ == "__main__":
    main()