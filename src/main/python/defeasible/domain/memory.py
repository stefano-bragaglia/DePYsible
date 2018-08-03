from collections import namedtuple
from typing import Dict, List, Optional, Set

from dataclasses import dataclass

from defeasible.domain.definitions import RuleType, Structure

OrderedLiteral = namedtuple('OrderedLiteral', 'position literal')
Trace = Set[OrderedLiteral]
Derivation = List['Rule']


@dataclass(init=True, repr=False, eq=True, order=True)
class Derivation:
    rules: List['Rule']
    _type: RuleType = None

    @property
    def type(self) -> RuleType:
        if self._type is not None:
            return self._type

        self._type = RuleType.STRICT
        for rule in self.rules:
            if rule.type == RuleType.DEFEASIBLE:
                self._type = RuleType.DEFEASIBLE

        return self._type

    @property
    def conclusion(self) -> 'Literal':
        return self.rules[-1].head

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        if len(self.rules) == 0:
            return '∅'

        if len(self.rules) == 1:
            return repr(self.rules[0].head)

        return '%s = %s' % (', '.join(repr(rule.head) for rule in self.rules[:-1]), repr(self.rules[-1].head))

    def get_argument(self) -> 'Structure':
        return Structure(self.rules[-1].head, {rule for rule in self.rules if rule.type == RuleType.DEFEASIBLE})


class NotGroundLiteralException(Exception):
    pass


class Memory:
    def __init__(self, program: 'Program'):
        self._facts = set()
        self._stricts = dict()
        self._rules = dict()
        self._program = program.get_ground_program()
        for rule in self._program.rules:
            if rule.is_fact():
                self._facts.add(rule)
            self._rules.setdefault(rule.head, set()).add(rule)
            if rule.type == RuleType.STRICT:
                self._stricts.setdefault(rule.head, set()).add(rule)
        self._defeasible_derivations = {}
        self._strict_derivations = {}
        self._defeasibly_contradictory = None
        self._strictly_contradictory = None

    def get_derivation(self, literal: 'Literal', type: RuleType = RuleType.DEFEASIBLE) -> Optional[Set[Derivation]]:
        if not self._facts:
            return None

        if type == RuleType.DEFEASIBLE and literal in self._defeasible_derivations:
            return self._defeasible_derivations[literal]

        if type == RuleType.STRICT and literal in self._strict_derivations:
            return self._strict_derivations[literal]

        rules = self._rules if type == RuleType.DEFEASIBLE else self._stricts
        sets_of_rules = get_supporting_sets_of_rules(literal, rules)
        if not sets_of_rules:
            if type == RuleType.DEFEASIBLE:
                return self._defeasible_derivations.setdefault(literal, None)

            else:
                return self._strict_derivations.setdefault(literal, None)

        derivations = {Derivation(set_of_rules) for set_of_rules in sets_of_rules if set_of_rules}
        if type == RuleType.DEFEASIBLE:
            return self._defeasible_derivations.setdefault(literal, derivations)
        else:
            return self._strict_derivations.setdefault(literal, derivations)

    def is_contradictory(self, type: RuleType = RuleType.DEFEASIBLE) -> bool:
        if type == RuleType.DEFEASIBLE and self._defeasibly_contradictory is not None:
            return self._defeasibly_contradictory

        if type == RuleType.STRICT and self._strictly_contradictory is not None:
            return self._strictly_contradictory

        contradictory = False
        for literal in self._program.as_literals():
            if self.get_derivation(literal, type) and self.get_derivation(literal.get_complement(), type):
                contradictory = True
                break

        if type == RuleType.DEFEASIBLE:
            self._defeasibly_contradictory = contradictory
        else:
            self._strictly_contradictory = contradictory

        return contradictory


def get_supporting_sets_of_rules(literal: 'Literal', index: Dict['Literal', Set['Rule']]) -> Optional[List['Rule']]:
    if not literal.is_ground():
        raise NotGroundLiteralException("Ground literal expected, but '%s' found" % literal)

    if literal not in index:
        return None

    rules = []
    for rule in index[literal]:
        complete = True
        partials = [[]]
        for body in rule.body:
            completions = get_supporting_sets_of_rules(body, index)
            if completions is None:
                complete = False
                break

            temporary = []
            for partial in partials:
                for completion in completions:
                    current = combine(partial, completion)
                    if current and current not in temporary:
                        temporary.append(current)
            partials = temporary

        if complete:
            for partial in partials:
                if not any(rule.head == current.head for current in partial):
                    partial.append(rule)
                rules.append(partial)

    return rules


def combine(left: list, right: list) -> list:
    result = []
    size = max(len(left), len(right))
    for i in range(-size, 0):
        for lst in [left, right]:
            try:
                item = lst[i]
            except IndexError:
                pass
            else:
                if item not in result:
                    result.append(item)

    return result


if __name__ == '__main__':
    from defeasible.domain.definitions import Program

    p = Program.parse("""
        bird(X) <- chicken(X).
        bird(X) <- penguin(X).
        ~flies(X) <- penguin(X).
        chicken(tina).
        penguin(tweety).
        scared(tina).
        flies(X) -< bird(X).
        flies(X) -< chicken(X), scared(X).
        nests_in_trees(X) -< flies(X).
        ~flies(X) -< chicken(X).
    """)
    m = Memory(p)
    p = p.get_ground_program()
    print(p)
    print()
    print('-' * 120)

    for literal in sorted(p.as_literals()):
        print(literal)
        derivations = m.get_derivation(literal)
        if derivations is None:
            print('\t', 'impossible')
        elif not derivations:
            print('\t', 'empty')
        else:
            for derivation in sorted(derivations):
                print('\t', derivation)
                print('\t\t', derivation.get_argument())
        print()
    print('-' * 120)

    print('Contradictory?', m.is_contradictory())
    print('Contradictory?', m.is_contradictory(RuleType.STRICT))

    # p = p.get_ground_program()
    # for literal in sorted(p.as_literals()):
    #     print(Renderer.render(literal))
    #     arguments = p.get_arguments(literal)
    #     if not arguments:
    #         print('\t', '-')
    #     else:
    #         for argument in sorted(arguments):
    #             print('\t', Renderer.render(argument))

    # p = p.get_ground_program()
    # arguments = {arg for lit in p.as_literals() for arg in p.get_arguments(lit)}
    # for arg in arguments:
    #     print(Renderer.render(arg))
    #     for other in arguments:
    #         if other != arg and other.is_substructure(arg):
    #             print('\t', Renderer.render(other))
    #     print()
