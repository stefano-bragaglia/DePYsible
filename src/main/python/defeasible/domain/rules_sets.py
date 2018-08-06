from typing import Dict, Iterable, List, Optional, Set

from dataclasses import dataclass

from defeasible.domain.definitions import RuleType


@dataclass(init=True, repr=False, eq=True, order=True)
class CounterArgument:
    attacker: 'Structure'
    disagreement: 'Structure'
    subject: 'Structure'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return '%s   ->   %s   @   %s' % (repr(self.attacker), repr(self.subject), repr(self.disagreement.conclusion))


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
        return type(other) is Structure and all(rule in other.argument for rule in self.argument)

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
        for literal in self.derivation.source.get_literals():
            derivations = self.derivation.source.get_derivations(literal)
            if derivations:
                for derivation in derivations:
                    attacker = derivation.get_structure()
                    if not attacker.argument or attacker == self:
                        continue

                    for disagreement in subarguments:
                        if self.derivation.source.disagree(disagreement.conclusion, attacker.conclusion):
                            counter_argument = CounterArgument(attacker, disagreement, self)
                            counter_arguments.add(counter_argument)

        return counter_arguments


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
            if self.get_derivations(literal) and self.get_derivations(literal.get_complement()):
                return True

        return False

    def disagree(self, literal1: 'Literal', literal2: 'Literal') -> bool:
        if literal1.get_complement() is literal2:
            return True

        return RuleSet({
            *self.strict,
            *self.facts,
            literal1.as_fact(),
            literal2.as_fact(),
        }).is_contradictory()


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
    p = p.get_ground_program()
    print(p)
    print()
    print('-' * 120)

    rs = RuleSet(p.rules)
    for literal in sorted(rs.get_literals()):
        print(literal)
        derivations = rs.get_derivations(literal)
        if derivations is None:
            print('\t', 'impossible')
        elif not derivations:
            print('\t', 'empty')
        else:
            for derivation in sorted(derivations):
                print('\t', derivation)
                structure = derivation.get_structure()
                print('\t\t', structure)
                for counter_argument in structure.get_counter_arguments():
                    print('\t\t\t', counter_argument)
        print()

    print('-' * 120)

    print('Contradictory?', rs.is_contradictory())
    print('Disagree:', Literal.parse('flies(tina)'), '&', Literal.parse('~flies(tina)'), '?',
          rs.disagree(Literal.parse('flies(tina)'), Literal.parse('~flies(tina)')))
