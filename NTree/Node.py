class Node:
    def __init__(self, key, parent):
        self.key = key
        self.parent = parent
        self.children = []

    def appendChild(self, child):
        self.children.append(child)