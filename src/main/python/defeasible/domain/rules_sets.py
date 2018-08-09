from enum import Enum
from typing import Dict, Iterable, List, Optional, Set

from dataclasses import dataclass

from defeasible.domain.definitions import RuleType


class Mark(Enum):
    UNDEFEATED = 0
    DEFEATED = 1


@dataclass(init=True, repr=False, eq=True, order=True)
class DialecticalNode:
    content: 'CounterArgument'
    parent: 'DialecticalNode' = None
    _concordance: 'RuleSet' = None
    _children: Set['DialecticalNode'] = None

    @staticmethod
    def create(root: 'Structure'):
        argument = CounterArgument(root)
        tree = DialecticalNode(argument)
        tree._build()

        return tree

    def __init__(self, argument: 'CounterArgument', parent: 'DialecticalNode' = None):
        self.content = argument
        self.parent = parent
        self._concordance = {
            *argument.subject.derivation.source.strict,
            *argument.subject.derivation.source.facts,
            *argument.subject.argument,
        } if not self.parent or not self.parent.parent else {
            *self.parent.parent._concordance,
            *argument.attacker.argument,
        }
        self._children = set()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return self._describe()

    def _describe(self, indent: int = 0) -> str:
        if not self.content.attacker:
            content = '\t' * indent + repr(self.content.subject)
        else:
            content = '\t' * indent + repr(self.content)
        for child in self._children:
            content += '\n' + child._describe(indent + 1)
        return content

    @property
    def children(self) -> Set['DialecticalNode']:
        return self._children

    @property
    def structure(self) -> 'Structure':
        if self.content.attacker:
            return self.content.attacker

        return self.content.subject

    def _build(self):
        for argument in self.structure.get_counter_arguments():
            if self.is_acceptable(argument) and argument.is_defeater():
                self.append(argument)

    def is_acceptable(self, other: 'CounterArgument'):
        if not self._is_concordant(other):
            return False

        if self._is_subargument(other):
            return False

        return self._is_not_chain_or_defeated(other)

    def _is_concordant(self, other: 'CounterArgument') -> bool:
        if other.attacker.derivation.source != self.structure.derivation.source:
            return False

        if not self.parent:
            return True

        return not RuleSet({*self.parent._concordance, *other.attacker.argument}).is_contradictory()

    def _is_subargument(self, other: 'CounterArgument') -> bool:
        if self.structure.contain(other.attacker):
            return True

        if not self.parent:
            return False

        return self.parent._is_subargument(other)

    def _is_not_chain_or_defeated(self, other: 'CounterArgument') -> bool:
        if not self.parent:
            return True

        if not self.content.is_blocking_defeater():
            return True

        return other.is_proper_defeater()

    def append(self, other: 'CounterArgument') -> Optional['DialecticalNode']:
        node = DialecticalNode(other, self)
        node._build()
        self._children.add(node)

        return node

    def mark(self) -> Mark:
        if not self._children:
            return Mark.UNDEFEATED

        for child in self.children:
            if child.mark() == Mark.UNDEFEATED:
                return Mark.DEFEATED

        return Mark.DEFEATED


@dataclass(init=True, repr=False, eq=True, order=True)
class CounterArgument:
    subject: 'Structure'  # <A2,h2>
    attacker: 'Structure' = None  # <A1,h1>
    disagreement: 'Structure' = None  # <A,h>

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return '%s   ->   %s   @   %s' % (repr(self.attacker), repr(self.subject), repr(self.disagreement))

    def is_direct(self) -> bool:
        return self.attacker.conclusion == self.disagreement.conclusion

    def is_self_defeater(self) -> bool:
        return self.attacker.conclusion == self.disagreement.conclusion == self.subject.conclusion

    def is_reciprocal_defeater(self, other: 'CounterArgument') -> bool:
        return self.disagreement.conclusion == other.attacker.conclusion \
               and self.attacker.conclusion == other.disagreement.conclusion

    def is_proper_defeater(self) -> bool:
        # <A1,h1> >> <A,h>
        return self.attacker.defeat(self.disagreement)

    def is_blocking_defeater(self) -> bool:
        if self.attacker.defeat(self.disagreement):
            return False

        if self.disagreement.defeat(self.attacker):
            return False

        return True

    def is_defeater(self) -> bool:
        return self.is_proper_defeater() or self.is_blocking_defeater()


@dataclass(init=True, repr=False, eq=True, order=True)
class Structure:
    argument: Set['Rule']
    conclusion: 'Literal'
    derivation: 'Derivation'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        if not self.argument:
            return '<∅, %s>' % repr(self.conclusion)

        return '<{%s}, %s>' % (' ; '.join(repr(rule) for rule in self.argument), repr(self.conclusion))

    def is_strict(self) -> bool:
        return not self.argument

    def contain(self, other: 'Structure') -> bool:
        return type(other) is Structure and all(rule in self.argument for rule in other.argument)

    def get_subarguments(self) -> Set['Structure']:
        if self.is_strict():
            return set()

        subarguments = set()
        for literal in self.derivation.source.get_literals():
            derivations = self.derivation.source.get_derivations(literal)
            if derivations:
                for derivation in derivations:
                    structure = derivation.get_structure()
                    if not self.contain(structure):  # contains itself
                        continue

                    subarguments.add(structure)

        return subarguments

    def get_counter_arguments(self) -> Set['CounterArgument']:
        if not self.argument:
            return set()

        counter_arguments = set()
        subarguments = self.get_subarguments()  # all the possible <A,h>
        for disagreement in subarguments:
            if not disagreement.is_strict():
                for structure in {disagreement.conclusion, disagreement.conclusion.get_complement()}:
                    derivations = self.derivation.source.get_derivations(structure)
                    if derivations:
                        for derivation in derivations:
                            attacker = derivation.get_structure()
                            if not attacker.argument or attacker == self:
                                continue

                            if self.derivation.source.disagree(disagreement.conclusion, attacker.conclusion):
                                counter_argument = CounterArgument(self, attacker, disagreement)
                                counter_arguments.add(counter_argument)

        # literals = {rule.head for rule in self.argument}
        # literals = self.derivation.source.get_literals()
        # subarguments = self.get_subarguments()  # all the possible <A,h>
        # for literal in literals:
        #     derivations = self.derivation.source.get_derivations(literal)
        #     if derivations:
        #         for derivation in derivations:
        #             attacker = derivation.get_structure()
        #             if not attacker.argument or attacker == self:
        #                 continue
        #
        #             for disagreement in subarguments:
        #                 # if disagreement.conclusion == attacker.conclusion:
        #                     if self.derivation.source.disagree(disagreement.conclusion, attacker.conclusion):
        #                         counter_argument = CounterArgument(self, attacker, disagreement)
        #                         counter_arguments.add(counter_argument)

        return counter_arguments

    def is_strictly_more_specific_than(self, other: 'Structure') -> bool:
        more_specific = False
        for literal in self.derivation.source.get_literals():
            strict = RuleSet({*self.derivation.source.strict, literal.as_fact()}) \
                         .get_derivations(other.conclusion) or False
            defeasible1 = RuleSet({*self.derivation.source.strict, literal.as_fact(), *self.argument}) \
                              .get_derivations(self.conclusion) or False
            defeasible2 = RuleSet({*self.derivation.source.strict, literal.as_fact(), *other.argument}) \
                              .get_derivations(other.conclusion) or False
            more_specific |= defeasible2 and not strict and not defeasible1
            if defeasible1 and not strict:
                if not defeasible2:
                    return False

        return more_specific

    def is_equi_specific_to(self, other: 'Structure') -> bool:
        if self.argument is not other.argument:
            return False

        rules = RuleSet({*self.derivation.source.strict, *self.derivation.source.facts, self.conclusion.as_fact()})
        if not rules.get_derivations(other.conclusion):
            return False

        rules = RuleSet({*self.derivation.source.strict, *self.derivation.source.facts, other.conclusion.as_fact()})
        if not rules.get_derivations(self.conclusion):
            return False

        return True

    def is_preferable_to(self, other: 'Structure') -> bool:
        preferable = False
        for rule1 in self.argument:
            for rule2 in other.argument:
                if not (rule1.salience < rule2.salience):
                    return False

                preferable |= rule1.salience > rule2.salience

        return preferable

    def defeat(self, other: 'Structure'):
        if self.is_equi_specific_to(other):
            return self.is_preferable_to(other)

        return self.is_strictly_more_specific_than(other)


@dataclass(init=True, repr=False, eq=True, order=True)
class Derivation:
    rules: List['Rule']
    source: 'RuleSet'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        explanation = ', '.join(repr(rule.head) for rule in reversed(self.rules)) if self.rules else '∅'
        symbol = '|~' if any(rule.type == RuleType.DEFEASIBLE for rule in self.rules) else '|-'
        derivable = self.rules[0].head

        return '%s %s %s' % (explanation, symbol, derivable)

    def union(self, other: 'Derivation') -> Optional['Derivation']:
        if type(other) is not Derivation or self.source != other.source:
            return None

        rules = [*self.rules]
        for rule in other.rules:
            if rule not in rules:
                rules.append(rule)

        return Derivation(rules, self.source)

    def get_structure(self) -> Structure:
        return Structure({rule for rule in self.rules if rule.type == RuleType.DEFEASIBLE}, self.rules[0].head, self)


@dataclass(init=True, repr=False, eq=True, order=True)
class RuleSet:
    facts: Set['Rule']
    strict: Set['Rule']
    defeasible: Set['Rule']
    _index: Dict['Literal', Set['Rule']]

    def __init__(self, rules: Iterable['Rule']):
        self.facts = set()
        self.strict = set()
        self.defeasible = set()
        self._index = dict()
        for rule in rules:
            if rule.type == RuleType.DEFEASIBLE:
                self.defeasible.add(rule)
            elif not rule.body:
                self.facts.add(rule)
            else:
                self.strict.add(rule)
            self._index.setdefault(rule.head, set()).add(rule)

    def get_literals(self) -> Set['Literal']:
        return set(self._index.keys())

    def get_derivations(self, literal: 'Literal') -> Optional[Set[Derivation]]:
        if not self.facts or literal not in self._index:
            return None

        derivations = set()
        for rule in self._index[literal]:
            partials = {Derivation([rule], self)}
            for body_literal in rule.body:
                completions = self.get_derivations(body_literal)
                if not completions:
                    partials = None
                    break

                temporary = set()
                for partial in partials:
                    for completion in completions:
                        derivation = partial.union(completion)
                        temporary.add(derivation)
                partials = temporary
            if partials:
                derivations.update(partials)

        return derivations or None

    def is_contradictory(self) -> bool:
        for literal in self._index:
            if self.get_derivations(literal):
                complement = literal.get_complement()
                if self.get_derivations(complement):
                    return True

        return False

    def disagree(self, literal1: 'Literal', literal2: 'Literal') -> bool:
        if literal1.get_complement() is literal2:
            return True

        rules = {*self.strict}
        rules.update(self.facts)
        rules.add(literal1.as_fact())
        rules.add(literal2.as_fact())

        rule_set = RuleSet(rules)

        return rule_set.is_contradictory()


class Answer(Enum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    UNDECIDED = 2


@dataclass(init=True, repr=False, eq=True, order=True)
class Problem:
    rules: RuleSet

    def __init__(self, program: 'Program'):
        self.rules = RuleSet(program.get_ground_program().rules)

    def query(self, literal: 'Literal') -> Answer:
        if literal not in self.rules.get_literals():
            return Answer.UNKNOWN

        if self._proof(literal):
            return Answer.YES

        complement = literal.get_complement()
        if self._proof(complement):
            return Answer.NO

        return Answer.UNDECIDED

    def _proof(self, literal: 'Literal') -> bool:
        derivations = self.rules.get_derivations(literal)
        if derivations:
            for derivation in derivations:
                structure = derivation.get_structure()
                tree = DialecticalNode.create(structure)
                print(tree)
                mark = tree.mark()
                if mark == Mark.UNDEFEATED:
                    return True

        return False

if __name__ == '__main__':
    from defeasible.domain.definitions import Program, Literal

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
    # p = Program.parse("""
    #     volatile(X) <- pollo(X).
    #     volatile(X) <- pinguino(X).
    #     ~vola(X) <- pinguino(X).
    #     pollo(tina).
    #     pinguino(titti).
    #     spaventato(tina).
    #     vola(X) -< volatile(X).
    #     vola(X) -< pollo(X), spaventato(X).
    #     nidifica_sugli_alberi(X) -< vola(X).
    #     ~vola(X) -< pollo(X).
    # """)
    # print(p)
    # print()
    # print('-' * 120)
    p = p.get_ground_program()
    print(p)
    print()
    print('-' * 120)

    # rs = RuleSet(p.rules)
    # for literal in sorted(rs.get_literals()):
    #     print(literal)
    #     derivations = rs.get_derivations(literal)
    #     if derivations is None:
    #         print('\t', 'impossible')
    #     elif not derivations:
    #         print('\t', 'empty')
    #     else:
    #         for derivation in sorted(derivations):
    #             print('\t', derivation)
    #             argument = derivation.get_structure()
    #             print('\t\t', argument)
    #             for counter_argument in argument.get_counter_arguments():
    #                 print('\t\t\t', counter_argument)
    #     print()
    #
    # print('-' * 120)
    #
    # print('Contradictory?', rs.is_contradictory())
    # print('Disagree:', Literal.parse('flies(tina)'), '&', Literal.parse('~flies(tina)'), '?',
    #       rs.disagree(Literal.parse('flies(tina)'), Literal.parse('~flies(tina)')))
    # print()
    # print('-' * 120)

    problem = Problem(p)

    literal = Literal.parse('penguin(tina)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('flies(tina)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('~flies(tina)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('flies(tweety)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('~flies(tweety)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('nests_in_trees(tina)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')

    literal = Literal.parse('~nests_in_trees(tina)')
    result = problem.query(literal)
    print('?-', literal, '\n', result.name, '\n')
"""

~flies(tweety) <- penguin(tweety).
bird(tina) <- chicken(tina).
bird(tweety) <- penguin(tweety).

chicken(tina).
scared(tina).
penguin(tweety).



"""
