from Node import Node
import codecs

nodes = {}

def addNode(key, parentKey, hasParent=True):
    if key in nodes:
        return

    if parentKey in nodes and hasParent == True:
        parent = nodes[parentKey]
        node = Node(key, parent)
        parent.appendChild(node)
        dic = {key : node}
        nodes.update(dic)
        return

    if hasParent == False:
        node = Node(key, None)
        dic = {key : node}
        nodes.update(dic)

def getTree():
    return nodes

def initTree():
    f = codecs.open("categorieStrings.txt","r", "utf-8") 
    
    for line in f:
        vals = line.split('>')
        for i in range(0, len(vals)):
            if i == 0:
                addNode(vals[i], '', False)
            else:
                addNode(vals[i], vals[i-1])
                
def getTree():
    initTree()
    return nodes
