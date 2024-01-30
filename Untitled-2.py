class categoryzator:
    class tree_filter:
        class Node:
            def __init__(self,filter,links = {}):
                self.ceil = filter
                self.links = links

            def next_by_key(self,key):
                return self.links[key] if key in self.links else None
            
            def next_all(self):
                return list(self.links.values())
            
            def add(self,filter,key):
                
                self.links[key] = filter


        def __init__(self):
            self.head = None
            self.next  = dict()

        def next()