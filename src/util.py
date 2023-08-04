# -*- coding: utf-8 -*-

class Rect:

    def __init__(self, top = 0, left = 0, bottom = 0, right = 0):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def __eq__(self, other):
        if type(other) != Rect:
            return False
        return self.top == other.top and \
            self.left == other.left and \
            self.bottom == other.bottom and \
            self.right == other.right

    def __str__(self):
        return "Rect(top={}, left={}, bottom={}, right={})".format(self.top, self.left, self.bottom, self.right)
