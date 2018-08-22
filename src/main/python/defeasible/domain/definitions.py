import re
from enum import Enum
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Union

from dataclasses import dataclass

Value = Union[bool, int, float, str]
Variable = str
Term = Union[Value, Variable]
Substitutions = Dict[Variable, Term]


@dataclass(init=True, repr=False, eq=True, order=True)
class Atom:
    functor: str
    terms: List[Term]

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        if not self.terms:
            return self.functor

        return '%s(%s)' % (self.functor, ', '.join(str(term) for term in self.terms))

    def arity(self) -> int:
        return len(self.terms)

    def is_ground(self) -> bool:
        for term in self.terms:
            if self.is_variable(term):
                return False

        return True

    def unifies(self, ground: 'Atom') -> Optional[Substitutions]:
        if not isinstance(ground, Atom):
            return None

        if self.functor != ground.functor:
            return None

        if self.arity() != ground.arity():
            return None

        substitutions = {}
        for i, term in enumerate(self.terms):
            if self.is_variable(term):
                if term not in substitutions:
                    substitutions[term] = ground.terms[i]
                elif substitutions[term] != ground.terms[i]:
                    return None

            elif term != ground.terms[i]:
                return None

        return substitutions

    def substitutes(self, subs: Substitutions) -> 'Atom':
        return Atom(self.functor, [subs.get(term, '_') if self.is_variable(term) else term for term in self.terms])

    @classmethod
    def is_variable(cls, term: Term) -> bool:
        return type(term) is str and re.match(r'[_A-Z][a-z_0-9]*', term)


@dataclass(init=True, repr=False, eq=True, order=True)
class Literal:
    negated: bool
    atom: Atom

    @staticmethod
    def parse(content: str) -> 'Literal':
        from arpeggio import ParserPython
        from arpeggio import visit_parse_tree
        from defeasible.language.grammar import literal, comment
        from defeasible.language.visitor import DefeasibleVisitor

        parser = ParserPython(literal, comment_def=comment)
        parse_tree = parser.parse(content)

        return visit_parse_tree(parse_tree, DefeasibleVisitor())

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return ('~' if self.negated else '') + repr(self.atom)

    @property
    def functor(self) -> str:
        return self.atom.functor

    @property
    def terms(self) -> List[Term]:
        return self.atom.terms

    def arity(self) -> int:
        return self.atom.arity()

    def is_ground(self) -> bool:
        return self.atom.is_ground()

    def unifies(self, ground: 'Literal') -> Optional[Substitutions]:
        if not isinstance(ground, Literal):
            return None

        if self.negated != ground.negated:
            return None

        return self.atom.unifies(ground.atom)

    def substitutes(self, subs: Substitutions) -> 'Literal':
        return Literal(self.negated, self.atom.substitutes(subs))

    def get_complement(self):
        return Literal(not self.negated, self.atom)

    def as_fact(self) -> 'Rule':
        return Rule(self, RuleType.STRICT, [])

    def get_derivation(self):
        raise NotImplemented

    def get_arguments(self):
        raise NotImplemented


class RuleType(Enum):
    STRICT = 0
    DEFEASIBLE = 1


@dataclass(init=True, repr=False, eq=True, order=True)
class Rule:
    head: Literal
    type: RuleType
    body: List[Literal]
    salience: int = 0

    @staticmethod
    def parse(content: str) -> 'Rule':
        from arpeggio import ParserPython
        from arpeggio import visit_parse_tree
        from defeasible.language.grammar import rule, comment
        from defeasible.language.visitor import DefeasibleVisitor

        parser = ParserPython(rule, comment_def=comment)
        parse_tree = parser.parse(content)

        return visit_parse_tree(parse_tree, DefeasibleVisitor())

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        content = repr(self.head)
        if self.body or self.type == RuleType.DEFEASIBLE:
            content += ' <- ' if self.type == RuleType.STRICT else ' -< '
        if self.body:
            content += ', '.join(repr(l) for l in self.body)
        content += '.'
        return content

    def is_fact(self) -> bool:
        return self.type == RuleType.STRICT and not self.body

    def is_presumption(self) -> bool:
        return self.type == RuleType.DEFEASIBLE and not self.body

    def is_ground(self) -> bool:
        for literal in [self.head, *self.body]:
            if not literal.is_ground():
                return False

        return True

    def as_literals(self) -> Set[Literal]:
        return {self.head, *self.body}


@dataclass(init=True, repr=False, eq=True, order=True)
class Program:
    rules: List[Rule]
    _ground: 'Program' = None
    _parent: 'Program' = None
    _strict: Set[Rule] = None
    _defeasible: Set[Rule] = None

    @staticmethod
    def parse(content: str) -> 'Program':
        from arpeggio import ParserPython
        from arpeggio import visit_parse_tree
        from defeasible.language.grammar import program, comment
        from defeasible.language.visitor import DefeasibleVisitor

        parser = ParserPython(program, comment_def=comment)
        parse_tree = parser.parse(content)

        program = visit_parse_tree(parse_tree, DefeasibleVisitor())

        return program

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        parts = []

        stricts = {}
        for strict in self.get_rules(RuleType.STRICT):
            stricts.setdefault(strict.head.atom, set()).add(strict)
        if stricts:
            parts.append(
                '# Strict rules\n%s' %
                '\n'.join(repr(rule) for atom in sorted(stricts) for rule in sorted(stricts[atom]))
            )

        facts = {}
        for fact in self.get_facts():
            facts.setdefault(fact.head.atom, set()).add(fact)
        if facts:
            parts.append(
                '# Facts\n%s' %
                '\n'.join(repr(rule) for atom in sorted(facts) for rule in sorted(facts[atom]))
            )

        defeasibles = {}
        for defeasible in self.get_rules(RuleType.DEFEASIBLE):
            defeasibles.setdefault(defeasible.head.atom, set()).add(defeasible)
        presumptions = {}
        for presumption in self.get_presumptions():
            presumptions.setdefault(presumption.head.atom, set()).add(presumption)
        if defeasibles or presumptions:
            parts.append(
                '# Defeasible knowledge\n%s' %
                '\n'.join(part for part in [
                    '\n'.join(repr(rule) for atom in sorted(defeasibles) for rule in sorted(defeasibles[atom])),
                    '\n'.join(repr(rule) for atom in sorted(presumptions) for rule in sorted(presumptions[atom])),
                ] if part)
            )

        return '\n\n'.join(parts)

    def get_facts(self) -> Iterable[Rule]:
        return (rule for rule in self.rules if rule.is_fact())

    def get_presumptions(self) -> Iterable[Rule]:
        return (rule for rule in self.rules if rule.is_presumption())

    def get_rules(self, type: RuleType = None) -> Iterable[Rule]:
        return (rule for rule in self.rules
                if not (rule.is_fact() or rule.is_presumption() or type and rule.type != type))

    def get_strict(self) -> Set[Rule]:
        program = self.get_ground_program()

        program._strict, program._defeasible = set(), set()
        for rule in program.rules:
            if rule.type == RuleType.STRICT:
                program._strict.add(rule)
            else:
                program._defeasible.add(rule)

        return program._strict

    def get_defeasible(self) -> Set[Rule]:
        program = self.get_ground_program()

        if program._defeasible is None:
            program._strict, program._defeasible = set(), set()
            for rule in program.rules:
                if rule.type == RuleType.STRICT:
                    program._strict.add(rule)
                else:
                    program._defeasible.add(rule)

        return program._defeasible

    def as_literals(self) -> Iterable[Literal]:
        return (literal for literal in {literal for rule in self.rules for literal in {rule.head, *rule.body}})

    def is_ground(self) -> bool:
        for rule in self.rules:
            if not rule.is_ground():
                return False

        return True

    def get_ground_program(self) -> 'Program':
        from defeasible.domain.rete import fire_rules

        if self.is_ground():
            return self

        if not self._ground:
            self._ground = Program(fire_rules(self))
            self._ground._parent = self

        return self._ground
