# 快速排序
# 取第一个为中值，也可以用random()随机取中值

def qsort(list):
    if not list:
        return []
    else:
        pivot = list[0]
        less = [x for x in list if x <  pivot]
        more = [x for x in list[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(more)



