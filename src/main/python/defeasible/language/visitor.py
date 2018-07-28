import json
import re
from typing import List, Union

from arpeggio import NonTerminal, PTNodeVisitor, Terminal

from defeasible import Program
from defeasible.domain.definitions import RuleType, Rule
from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Atom

Node = Union[Terminal, NonTerminal]


# noinspection PyMethodMayBeStatic
class DefeasibleVisitor(PTNodeVisitor):
    def visit_comment(self, node: Node, children: List) -> str:
        return node.value

    def visit_program(self, node: Node, children: List) -> Program:
        return Program(children)

    def visit_rule(self, node: Node, children: List) -> Rule:
        return children[0]

    def visit_defeasible(self, node: Node, children: List) -> Rule:
        try:
            return Rule(children[0], RuleType.DEFEASIBLE, children[1])
        except IndexError:
            return Rule(children[0], RuleType.DEFEASIBLE, [])

    def visit_strict(self, node: Node, children: List) -> Rule:
        try:
            return Rule(children[0], RuleType.STRICT, children[1])
        except IndexError:
            return Rule(children[0], RuleType.STRICT, [])

    def visit_literals(self, node: Node, children: List) -> List[Literal]:
        return [child for child in children]

    def visit_literal(self, node: Node, children: List) -> Literal:
        try:
            return Literal(children[0], children[1])
        except IndexError:
            return Literal(False, children[0])

    def visit_negation(self, node: Node, children: List) -> bool:
        return True if len(children) % 2 == 1 else False

    def visit_atom(self, node: Node, children: List) -> Atom:
        try:
            return Atom(children[0], children[1])
        except IndexError:
            return Atom(children[0], [])

    # noinspection RegExpSingleCharAlternation
    def visit_functor(self, node: Node, children: List) -> bool:
        if re.match(r'("|\')[a-z][a-z_0-9]*\1', children[0]):
            return children[0][1:-1]

        return children[0]

    def visit_terms(self, node: Node, children: List) -> List[Union[bool, int, float, str]]:
        return [child for child in children]

    def visit_term(self, node: Node, children: List) -> Union[bool, int, float, str]:
        return children[0]

    def visit_boolean(self, node: Node, children: List) -> bool:
        return children[0]

    def visit_false(self, node: Node, children: List) -> bool:
        return False

    def visit_true(self, node: Node, children: List) -> bool:
        return True

    def visit_number(self, node: Node, children: List) -> Union[int, float]:
        return children[0]

    def visit_real(self, node: Node, children: List) -> float:
        return float(node.value)

    def visit_integer(self, node: Node, children: List) -> int:
        return int(node.value)

    def visit_string(self, node: Node, children: List) -> str:
        return children[0]

    def visit_double_quote(self, node: Node, children: List) -> str:
        return json.dumps(children[0])

    def visit_single_quote(self, node: Node, children: List) -> str:
        return json.dumps(children[0])

    def visit_identifier(self, node: Node, children: List) -> str:
        return str(node.value)

    def visit_variable(self, node: Node, children: List) -> str:
        return str(node.value)
