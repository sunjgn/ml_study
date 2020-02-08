# -*- coding:utf-8 -*-
class Stack:
    def __init__(self):
        self._elems = []
    def is_empty(self):
        return self._elems == []
    def push(self, elem):
        self._elems.append(elem)
    def pop(self):
        if self._elems == []:
            return
        return self._elems.pop()
    def top(self):
        if self._elems == []:
            return
        return self._elems[-1]
class Solution(object):

    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        # zip 用法
        # [(1,2,3), (4,5,6)]  -----> [(1,4), (2,5), (3,6)]
        ss = zip(*strs)
        # ss = list(map(set, zip(*strs)))
        res = ''
        for index, value in enumerate(ss):
            if len(set(value)) > 1:
                break
            res = res + value[0]
        return res

    def invalid_kuohao(self, s):
        stack = Stack()
        left = '({['
        right = ')}]'
        partens = {')': '(', ']': '[', '}': '{'}
        for i in s:
            if i in left:
                stack.push(i)
            elif i in right:
                if stack.is_empty():
                    return False
                if partens[i] != stack.pop():
                    return False
        if stack.is_empty():
            return True
        return False


if __name__ == '__main__':
    solution = Solution()
    result = solution.longestCommonPrefix(['abab', 'aba', 'aba', ''])
    print result