import sys
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
#quick_sort_2 = lambda array: array if len(array) <= 1 else quick_sort([item for item in array[1:] if item <= array[0]]) + [array[0]] + quick_sort([item for item in array[1:] if item > array[0]])

def quick_sort(array, start, end):
    if start > end:
        return
    left = start
    right = end
    mid = array[left]
    while left < right:
        while left < right and array[right] >= mid:
            right -= 1
        array[left] = array[right]
        while left < right and array[left] < mid:
            left += 1
        array[right] = array[left]
    array[left] = mid
    quick_sort(array, start, left - 1)
    quick_sort(array, left + 1, end)

if __name__ == '__main__':
    array = [1,3,4,2,5,6,7,2,3]
    quick_sort(array, 0, len(array) - 1)
    print array


