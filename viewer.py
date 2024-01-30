import pprint
import os
import json
import random
from tkinter import W
from pick import pick
from category_v2 import category_filter

def category_finder(text_dict,arg2 = None):
    filter = category_filter(r"C:\Users\stank\cat_v2\filters_v3.json")
    toUpdate = list()
    res = []
    for text in text_dict:
        text["title_flg"] = filter.find_category(text["title_norm"])
        for item in text["title_flg"]:
            item["score"] = int(item["score"])*3
        text["desc_flg"] = filter.find_category(text["desc_norm"])
        text["metrick"] = metrick(text)
        res.append([text["ID"],text["Title"],text["Description"],text["title_norm"],text["desc_norm"],text["desc_flg"],text["title_flg"],text["metrick"]])
        flag = False
        for flg in text["title_flg"]+ text["desc_flg"]:
            if flg["word"]["content"] in ["keyre","keyring",["key","ring"]]:
                flag = True
                break
        if flag:
            for flg in text["title_flg"]+ text["desc_flg"]:
                if flg["word"]["content"] not in ["keyre","keyring",["key","ring"],["key", "chain"],"keychain"] and flg["word"]["content"] not in toUpdate:
                    toUpdate.append(flg["word"]["content"])
    with open("toUpdate.json","w+",encoding="utf-8") as file:
        json.dump(toUpdate,file)
    return res

def update(filter,upadateFile,anti_words,ignore=None):
    with open(upadateFile,"r") as file:
        toUpgdate = json.load(file)
    for cat in filter.categoryes():
        if type(ignore) == list:
            if cat in ignore:
                continue
        else:
            if ignore == cat:
                continue
        for item in toUpgdate:
            if filter.in_category(cat,item):
                filter.add_anti_word(cat, item, anti_words,typeUpdate = "many")
    filter.load_to_file("filters_v3.json")

def metrick(text):
    total = 0
    flags = dict()
    for item in text["desc_flg"]:
        total  = total + item["score"]
        if item["category"] in flags:
            flags[item["category"]] = flags[item["category"]] + item["score"]
        else:
            flags[item["category"]] = item["score"]
    for item in text["title_flg"]:
        total  = total + item["score"]
        if item["category"] in flags:
            flags[item["category"]] = flags[item["category"]] + item["score"]
        else:
            flags[item["category"]] = item["score"]
    
    for flag in flags:
        flags[flag] = flags[flag]/total
    return flags
 
def view(res):
    random.shuffle(res)
    pp = pprint.PrettyPrinter(indent=2, width= 140,compact=True)
    i = 0
    while(True):
            title = pp.pformat([res[i],len(res)])
            print("\n")
            if (i == 0):
                options = ["Next","Quit"]
                option, index = pick(options,title)
                if option == "Next":
                    i +=1
                else:
                    return 0
            elif (i == len(res)-1):
                options = ["Prev","Quit"]
                option, index = pick(options,title)
                if option == "Prev":
                    i -=1
                else:
                    return 0    
            else:
                options = ["Prev","Next","Quit"]
                option, index = pick(options,title)
                if option == "Prev":
                    i -=1
                elif option == "Next":
                    i += 1
                else:
                    return 0
            os.system("cls")

def find_no_flgs(text_dict):
    return [i for i in text_dict if not len(i[5]) and not len(i[6])]

def with_flg(text_dict):
    return [i for i in text_dict if (len(i[5])) or (len(i[6]))]


def low_metrick(text_dict):
    return [i for i in text_dict if len(i[7])>0 and (sorted(list(i[7].values()),reverse=True)[0] < 0.51)]

def is_word_in_text(text,word):
    for item in text["norm"]:
        for temp in item["chunk"]:
            if word in temp:
                return True
                
def find_by_word(text_dict,word):
    words = word.split()
    texts = list()
    if len(words) > 1:
        for item in text_dict:
            flag = True
            temp = item["desc_norm"]["chunks"] + item["title_norm"]["chunks"]
            for chunk in temp:
                for word_item in words:
                    if word_item not in chunk:
                        flag = False
                        break 
                if flag:
                    texts.append(item)
                    break
    else:
        for item in text_dict:
            if word in item["title_norm"]["full_text"] or word in item["desc_norm"]["full_text"]:
                texts.append(item)
    return texts

def main():

    # filter = category_filter(r"C:\Users\stank\cat_v2\filters_v2.json")
    # update(filter=filter,upadateFile="toUpdate.json",anti_words=["keyre","keyring",["key","ring"],["key", "chain"],"keychain"],ignore="Promo souvenirs")
    with open(r"C:\Users\stank\cat_v2\result_v2.json","r",encoding = "utf-8") as file:
        text_dict = json.load(file)
    print(len(text_dict))
    

    options1 = ["Category","Find by word","Quit"]
    while(True):
        option,index = pick(options1)
        if option == "Find by word":
            while(True):
                t = input("Write word:").strip().lower()
                if t == "quit":
                    break 
                else:
                    view(find_by_word(text_dict,t))
        elif option == "Category":
            option1,index = pick(["All","Without flg","With flg","Low metrick"])
            if option1  == "All":
                view(category_finder(text_dict))    
            elif option1 == "Without flg":
                view(find_no_flgs(category_finder(text_dict)))
            elif option1 == "With flg":
                view(with_flg(category_finder(text_dict)))
            else:
                view(low_metrick(category_finder(text_dict)))
        else:
            break

if __name__ == "__main__":
    main()