from collections import namedtuple
from typing import Dict, List, Optional, Set

from defeasible.domain.definitions import RuleType

OrderedLiteral = namedtuple('OrderedLiteral', 'position literal')
Trace = Set[OrderedLiteral]
Derivation = List['Literal']


class NotGroundLiteralException(Exception):
    pass


class Memory:
    def __init__(self, program: 'Program'):
        self._facts = set()
        self._stricts = dict()
        self._defeasibles = dict()
        self._program = program.get_ground_program()
        for rule in self._program.rules:
            if rule.is_fact():
                self._facts.add(rule)
            self._defeasibles.setdefault(rule.head, set()).add(rule)
            if rule.type == RuleType.STRICT:
                self._stricts.setdefault(rule.head, set()).add(rule)
        self._strict_derivations = {}
        self._defeasibles_derivations = {}
        self._contradictory = None

    def derive(self, literal: 'Literal', type: RuleType = RuleType.DEFEASIBLE) -> Optional[List[Derivation]]:
        if not self._facts:
            return None

        if type == RuleType.DEFEASIBLE and literal in self._defeasibles_derivations:
            return self._defeasibles_derivations[literal]

        if type == RuleType.STRICT and literal in self._strict_derivations:
            return self._strict_derivations[literal]

        results = get_derivations(literal, self._defeasibles if type == RuleType.DEFEASIBLE else self._stricts)
        if type == RuleType.DEFEASIBLE:
            self._defeasibles_derivations[literal] = results
        else:
            self._strict_derivations[literal] = results

        return results

    def is_contradictory(self, type: RuleType = RuleType.DEFEASIBLE) -> bool:
        if self._contradictory is None:
            self._contradictory = False
            derivations = self._defeasibles_derivations if type == RuleType.DEFEASIBLE else self._strict_derivations
            for literal in self._program.as_literals():
                if literal in derivations and literal.get_complement() in derivations:
                    self._contradictory = True

        return self._contradictory


def get_derivations(literal: 'Literal', index: Dict['Literal', Set['Rule']]) -> Optional[List[Derivation]]:
    if not literal.is_ground():
        raise NotGroundLiteralException("Ground literal expected, but '%s' found" % literal)

    if literal not in index:
        return None

    derivations = []
    for rule in index[literal]:
        complete = True
        partials = [[]]
        for body in rule.body:
            completions = get_derivations(body, index)
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
                if rule.head not in partial:
                    partial.append(rule.head)
                derivations.append(partial)

    return derivations


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
    from defeasible.domain.rendering import Renderer
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
    print(Renderer.render(p))
    print()

    for literal in sorted(p.as_literals()):
        print(Renderer.render(literal))
        derivations = m.derive(literal)
        if derivations is None:
            print('\t', 'impossible')
        elif not derivations:
            print('\t', 'empty')
        else:
            for derivation in derivations:
                print('\t', ', '.join(Renderer.render(lit) for lit in derivation))
        print()
    print('-' * 120)

    for literal in sorted(p.as_literals()):
        print(Renderer.render(literal))
        derivations = m.derive(literal, type=RuleType.STRICT)
        if derivations is None:
            print('\t', 'impossible')
        elif not derivations:
            print('\t', 'empty')
        else:
            for derivation in derivations:
                print('\t', ', '.join(Renderer.render(lit) for lit in derivation))
        print()

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
