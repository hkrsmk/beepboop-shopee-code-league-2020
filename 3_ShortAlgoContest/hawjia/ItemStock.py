from enum import Enum
import math
import sys

class Type(Enum):
    DYANAMIC = 1
    STATIC = 2

class Node:
    def __init__(self, id, type, parent, ratio, stock):
        self.id = id
        self.parent = parent
        self.type = Type(type)
        self.ratio = ratio
        self.stock = stock
        self.children = []

    def __str__(self):
        return f"id: {self.id}\n" + \
            f"parent: {self.parent.id if self.parent else 'nil'}\n" + \
            f"type: {self.type}\n" + \
            f"ratio: {self.ratio}\n" + \
            f"stock: {self.stock}\n" + \
            f"children: {list(map(lambda x: x.id, self.children))}"

def parse_line(line):
    params = list(map(int, line.split()))
    type = Type(params[0])
    parent = params[1]
    ratio = params[2]
    if type == Type.DYANAMIC:
        return type, parent, ratio, None
    else:
        stock = params[3]
        return type, parent, ratio, stock

def redistribute_stock(node):
    for child in node.children:
        if child.type == Type.DYANAMIC:
            child.stock = math.floor(node.stock / child.ratio)
            redistribute_stock(child)

def get_first_fixed_node(node):
    current = node
    while current.type != Type.STATIC:
        current = current.parent
    return current

def get_multiplier(begin, end):
    multiplier = 1
    current = begin
    while current.id != end.id:
        multiplier = multiplier * current.ratio
        current = current.parent
    return multiplier

def main():
    [items, stock, ] = map(int, sys.stdin.readline().split())
    tree = Node(1, Type.STATIC, None, None, stock)    
    nodes = list(map(lambda x: None, range(items)))
    nodes[0] = tree

    for i in range(1, items):
        type, parent, ratio, stock = parse_line(sys.stdin.readline())
        current = Node(i + 1, type, nodes[parent - 1], ratio, stock)
        current.parent.children.append(current)
        nodes[i] = current
        parent = nodes[parent - 1]

        if current.type == Type.DYANAMIC:
            current.stock = math.floor(parent.stock / current.ratio)
            # print(f"Inserting dynamic item:\n{current}")
            # print(f"Current items:")
            # for j in range(i + 1):
            #     print(nodes[j])
            # print()
        else:
            source = get_first_fixed_node(parent)
            multiplier = get_multiplier(current, source)
            source.stock = source.stock - current.stock * multiplier
            redistribute_stock(source)
            # print(f"Inserting static item:\n{current}\n")
            # print(f"Current items:")
            # for j in range(i + 1):
            #     print(nodes[j])
            # print()
    
    for node in nodes:
        print(node.stock)

if __name__ == '__main__':
    main()
