import json
from cat_find import category_filter
from node import Node
class categorizator:
         
    def __init__(self,filter: category_filter):
        self.root = Node(filter)

    def convert(product):
        obj = {}
        obj["ID"] = product['articul']
        obj["TITLE"] = product["name"]
        obj["DESCRIPTION"] = product["description"]
        obj["MATERIALS"] = product["materials"]
        return obj
    

    def mask(self,category = None,pattern = None,prev = None):
        if pattern == None:
            to_add = dict()
            pattrn = {"EN":None}
            for cat in self.root.filter.categoryes():
                if not self.root.has_next(cat):
                    to_add.setdefault(cat,{"products":[]})
                else:
                    to_add[cat] = None
                    to_add[cat] = self.mask(category=self.root.next(cat),prev = cat,pattern = to_add)
            pattrn["EN"] = to_add
            with open("pattern.json","w+",encoding="utf-8") as file:
                json.dump(pattrn,file)
                
        else:
            next_pattern = {}
            pattern[prev] = next_pattern
            for cat in category.filter.categoryes():
                if category.has_next(cat):
                    next_pattern.setdefault(cat,{"products":[]})
                else:
                    next_pattern[cat] = None
                    next_pattern[cat] = self.mask(category.next(cat),pattern=next_pattern,prev=cat)


    def find_categoryes(self,obj):
        info = []
        level = 0
        fil = self.root
        res = list()
        while True:
            cat_obj = fil.filter.find_category(obj)
            cat = cat_obj["category"]
            res.append(cat)
            info.append({"level":level,"tags":cat_obj})
            if fil.has_next(cat):
                fil = fil.next(cat)
                level = level+1
            else: 
                break
        return [res,info ]

        
        

    

