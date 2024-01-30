import spacy
import json 
import sys
import pprint
import random
from multiprocessing import Pool
from category_container import categorizator
from normalize import normalize_text
from cat_find import category_filter
global filt
filt = category_filter("filter_v4_level_0.json")




def hui(obj):
    try:
        t = filt.find_category(obj)
        t["product"] = obj
        return t
    except:
        pass

if __name__ == '__main__':
    k=int(sys.argv[1])
    m =int(sys.argv[2])
    filt = category_filter("filter_v4_level_0.json")
    with open("full_res_from_db_2.json","r",encoding="utf-8") as file:
        full_res = json.load(file)
    random.shuffle(full_res)
    with Pool(4) as p:
        res = p.map(hui,full_res[k:m])
    
    with open("first_cat.json","w+",encoding="utf-8") as file:
        json.dump(list(filter(lambda x: x != None,res)),file)
    
