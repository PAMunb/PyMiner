#test_list_annotation
from collections import Counter, defaultdict, deque
from typing import List


my_list: list[int] = []
        
#test_dict_annotation
my_dict: dict[str, int] = {}
   
#test_set_annotation
my_set: set[int] = set()

#test_tuple_annotation
my_tuple: tuple[int, int] = (1, 2)

#test_deque_annotation(self):
my_deque: deque[int] = deque()   

#test_counter_annotation(self)
my_counter: Counter[str] = Counter()

# test_defaultdict_annotation(self):
my_defaultdict: defaultdict[str, int] = defaultdict(int)

#test_old_typing_annotations
mlist:List[int] = []
    