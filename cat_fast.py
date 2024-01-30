import spacy
import json 
import sys
import pprint
import random
from multiprocessing import Pool
from category_container import categorizator
from normalize import normalize_text
from cat_find import category_filter
global full_cat
full_cat = categorizator(category_filter("filter_v4_level_0.json"))


def cat(cats,trash_cats):
    for i in cats:
        if i in trash_cats:
            return False
    return True

def fsdo(obj):
    try:
        return [full_cat.find_categoryes(obj)[0],obj]
    except:
        pass

if __name__ == '__main__':
    trash_cats = ["Pens", "Jackets","T-shirts","Shirts","Polo"]
    k=int(sys.argv[1])
    m =int(sys.argv[2])
    with open("full_res_from_db_2.json","r",encoding="utf-8") as file:
        full_res = json.load(file)
    with Pool(12) as p:
        res = p.map(fsdo,full_res[k:m])

    with open("cat_multi.txt","w",encoding="utf-8") as file:
        for i in res:
            try:
                if not cat(i[0],trash_cats=trash_cats):
                    continue
                for key in i[1]:
                    file.write("{key}:{text}".format(key = key,text = i[1][key])+ '\n')
                file.write(str(i[0])+'\n')
                file.write("=============================="+ '\n')
            except:
                continue