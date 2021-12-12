class Node:
    king = None

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
        if Node.king == self:
            Node.king = None
        else:
            self.visited = False

    def may_visit(self):
        if self.visited and Node.king is None:
            Node.king = self
            return True

        return not self.visited


class Start(Node):
    def may_visit(self):
        return False


class Big(Node):
    def may_visit(self):
        return True


class NodeRegistry:
    def __init__(self):
        self.nodes = {}
        self.nodes["start"] = Start()

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
