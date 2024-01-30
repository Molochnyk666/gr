import json
import time

with open(r"C:\Users\stank\fr.json") as file:
    categoryes = json.load(file)
    
def del_pos(item):
    if type(item) == dict:
        return list(item.keys())[0]
    else:
        return sorted([list(word.keys())[0] for word in item])

def time_of_function(func):
    def wrapper(arg1,arg2):
        start = time.time()
        res = func(arg1,arg2)
        end = time.time()
        print(end-start)
        return res
    return wrapper

# @time_of_function
def compare_lists(lists,list1):
    flag = True
    for listt in lists:
        if len(list1) == len(listt):
            flag = False
            for item1,item2 in zip(list1["content"],listt["content"]):
                if item1 != item2:
                    flag = True
                    break
            if not flag:
                res = combine_anti_words(listt,list1)
                if res:
                    listt["anti_word"] = res
                break
    if flag:
        lists.append(list1)
                



def combine_anti_words(item1,item2,key="anti_word"):
    res = set()
    for item in [item1,item2]:
        if key in item:
            temp = item[key]
            if type(temp) == list:
                res = res.union(set(temp))
            else:
                res.add(temp)
    return list(res)
    # if key in item1 and key in item2:
    #     if type(item[key]) == list:
    #     return list(set(item1[key] + item2[key]))
    # elif key in item1:
    #     return item1[key]
    # elif key in item2:
    #     return item2[key]
    # else: 
    #     return False 

def remove_copies(categoryes):
    
    for filter in categoryes:
        print(filter)
        print(len(categoryes[filter]))
        lists = []
        single_words = []
        for item in categoryes[filter]:
            if type(item["content"]) ==list :
                if len(lists) != 0:
                    compare_lists(lists,item)
                else:
                    lists.append(item)
            else:
                if len(single_words) == 0:
                    single_words.append(item)
                else:
                    flag = True
                    for word in single_words:
                        if word["content"] == item["content"]:
                            flag = False
                            res = combine_anti_words(item,word)
                            if res:
                                word["anti_word"] = res
                            break
                    
                    if flag:
                        single_words.append(item)
            categoryes[filter] = single_words+lists


for filter in categoryes:
    for item in categoryes[filter]:
        for x in item:
            item[x] = del_pos(item[x])
end = time.time()

# print(categoryes)
remove_copies(categoryes)

print(categoryes)

with open(r"C:\Users\stank\cat_v2\filters_v2.json","w+") as file:
    json.dump(categoryes,file)