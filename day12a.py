class Node:
    def __init__(self):
        self.neighbours = set()
        self.visited = False

    def connect(self, node):
        self.neighbours.add(node)
        node.neighbours.add(self)

    def trace(self, end):
        self.visited = True
        if self == end:
            yield 1
        else:
            for node in self.neighbours:
                if node.may_visit():
                    for result in node.trace(end):
                        yield result
        self.visited = False

    def may_visit(self):
        return not self.visited


class Big(Node):
    def may_visit(self):
        return True


class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def __getitem__(self, name):
        if name not in self.nodes:
            self.nodes[name] = Big() if name.isupper() else Node()

        return self.nodes[name]


with open("day12.txt") as file:
    nodes = NodeRegistry()

    for line in file.readlines():
        frm, to = line.strip().split('-')
        nodes[frm].connect(nodes[to])

    print sum(nodes["start"].trace(nodes["end"]))
