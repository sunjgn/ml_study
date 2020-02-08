'''
def sort(list):
    if len(list) <= 1:
        return list
    middle = len(list) / 2
    left = sort(list[:middle])
    right = sort(list[middle:])
    return merge(left, right)

def merge(left, right):
    c = []
    j = k = 0
    while j < len(left) and k < len(right):
        if left[j] < right[k]:
            c.append(left[j])
            j = j + 1
        else:
            c.append(right[k])
            k = k + 1
    if j == len(left):
        for temp in right[k:]:
            c.append(temp)
    else:
        for temp in left[j:]:
            c.append(temp)
    return c

if __name__ == "__main__":
    test = [3,5,1,2,6, 7, 0, 4]
    res = sort(test)
    print res
'''

def sort(list):
    if len(list) <= 1:
        return list
    mid = len(list) / 2
    left = sort(list[:mid])
    right = sort(list[mid:])
    return merge(left, right)

def merge(left, right):
    c = []
    j = k = 0
    while j < len(left) and k < len(right):
        if left[j] < right[k]:
            c.append(left[j])
            j += 1
        else:
            c.append(right[k])
            k += 1
    if j == len(left):
        for temp in right[k:]:
            c.append(temp)
    else:
        for temp in left[j:]:
            c.append(temp)
    return c


if __name__ == '__main__':
    #array = [3,5,1,2,6, 7, 0, 4]
    array = [1,2,3,4,5,4,3,6,5,4]
    res = sort(array)
    print res

