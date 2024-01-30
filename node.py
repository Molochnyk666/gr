from cat_find import category_filter

class Node:
    def __init__(self,filter:category_filter):
        self.filter = filter
        self.child = {}
        temp = self.filter.all_next_filters()
        if len(temp) != 0:
            for item in temp:
                name = item[0]
                fil = Node(item[1])
                self.child.setdefault(name,fil)
        else: 
            self.child = None

    def next(self,category):
        return self.child[category]
        
    def has_next(self,category):
        if self.child == None or category not in self.child:
            return False
        else: 
            return True