from Node import Node

nodes = {}

def addNode(key, parentKey, hasParent=True):
    if parentKey in nodes and hasParent == True:
        parent = nodes[parentKey]
        node = Node()
        node.key = key
        node.parent = parent
        parent.children.append(node)
        dic = {key : node}
        nodes.update(dic)
    if hasParent == False:
        node = Node()
        node.key = key
        dic = {key : node}
        nodes.update(dic)

def getTree():
    return nodes