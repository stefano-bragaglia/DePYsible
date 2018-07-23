from enum import Enum
from typing import List


class Status(Enum):
    DEFEATED = 0
    UNDEFEATED = 1


class Node:
    @staticmethod
    def create(content: 'Structure', arguments: List['Structure']) -> 'Node':
        root = Node(content)
        return process(root, arguments)

    @staticmethod
    def process(current: 'Node', arguments: List['Structure']) -> 'Node':
        for argument in arguments:
            if argument.is_defeater_for(current.content):
                if not current.contains(current.content):  # undecidable?
                    node = Node(argument, current)
                    child = process(node, arguments)
                    current.children.add(child)

        return current

    def __init__(self, content: 'Structure', parent: 'Node' = None):
        self.content = content
        self.parent = parent
        self.children = set()
        self.status = None

    def contains(self, argument: 'Structure') -> bool:
        if argument == self.content:
            return True

        if not self.parent:
            return False

        return self.parent.contains(argument)

    def mark(self):
        if not self.status:
            if not self.children:
                self.status = Status.UNDEFEATED

            else:
                self.status = Status.UNDEFEATED
                for child in self.children:
                    if child.mark() == Status.UNDEFEATED:
                        self.status = Status.DEFEATED

        return self.status


        return self.status


def process(root: 'Structure', arguments: List['Structure']) -> Node:
    current = Node(root)
    for argument in arguments:
        if argument.is_defeater_for(current.content):
            if current.contains(current.content):
                pass



