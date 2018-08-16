import re
from typing import Any
from typing import Set

from defeasible.domain.interpretation import Answer


class UncoveredClassException(Exception):
    pass


class Renderer:

    @staticmethod
    def comma(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import PUNCTUATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return ', '

        elif uncovered:
            return '%s, %s' % (UNCOVERED, RESET)

        else:
            return '%s, %s' % (PUNCTUATION, RESET)

    @staticmethod
    def colon(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return ' ; '

        elif uncovered:
            return '%s ; %s' % (UNCOVERED, RESET)

        else:
            return '%s ; %s' % (ARGUMENTATION, RESET)

    @staticmethod
    def empty(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '∅'

        elif uncovered:
            return '%s∅%s' % (UNCOVERED, RESET)

        else:
            return '%s∅%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def lcur(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '{'

        elif uncovered:
            return '%s{%s' % (UNCOVERED, RESET)

        else:
            return '%s{%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def rcur(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '}'

        elif uncovered:
            return '%s}%s' % (UNCOVERED, RESET)

        else:
            return '%s}%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def lpar(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import PUNCTUATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '('

        elif uncovered:
            return '%s(%s' % (UNCOVERED, RESET)

        else:
            return '%s(%s' % (PUNCTUATION, RESET)

    @staticmethod
    def rpar(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import PUNCTUATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return ')'

        elif uncovered:
            return '%s)%s' % (UNCOVERED, RESET)

        else:
            return '%s)%s' % (PUNCTUATION, RESET)

    @staticmethod
    def lang(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '<'

        elif uncovered:
            return '%s<%s' % (UNCOVERED, RESET)

        else:
            return '%s<%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def rang(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ARGUMENTATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '>'

        elif uncovered:
            return '%s>%s' % (UNCOVERED, RESET)

        else:
            return '%s>%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def stop(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import PUNCTUATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '.'

        elif uncovered:
            return '%s.%s' % (UNCOVERED, RESET)

        else:
            return '%s.%s' % (PUNCTUATION, RESET)

    @staticmethod
    def negate(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import NEGATION
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return '~'

        elif uncovered:
            return '%s~%s' % (UNCOVERED, RESET)

        else:
            return '%s~%s' % (NEGATION, RESET)

    @staticmethod
    def strict(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import STRICT
        from defeasible.domain.theme import RESET

        if blind:
            return ' <- '

        else:
            return '%s <- %s' % (STRICT, RESET)

    @staticmethod
    def defeasible(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import DEFEASIBLE
        from defeasible.domain.theme import RESET

        if blind:
            return ' -< '

        else:
            return '%s -< %s' % (DEFEASIBLE, RESET)

    @staticmethod
    def strictly(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import STRICT
        from defeasible.domain.theme import RESET

        if blind:
            return ' |- '

        else:
            return '%s |- %s' % (STRICT, RESET)

    @staticmethod
    def defeasibly(uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import DEFEASIBLE
        from defeasible.domain.theme import RESET

        if blind:
            return ' |~ '

        else:
            return '%s |~ %s' % (DEFEASIBLE, RESET)

    @classmethod
    def render(cls, obj: Any, uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import Program
        from defeasible.domain.definitions import Derivation
        from defeasible.domain.definitions import Structure

        if type(obj) in [bool, int, float, str]:
            return cls.render_term(obj, uncovered, blind)

        elif type(obj) is Atom:
            return cls.render_atom(obj, uncovered, blind)

        elif type(obj) is Literal:
            return cls.render_literal(obj, uncovered, blind)

        elif type(obj) is Rule:
            return cls.render_rule(obj, uncovered, blind)

        elif type(obj) is Program:
            return cls.render_program(obj, uncovered, blind)

        elif type(obj) is Derivation:
            return cls.render_derivation(obj, uncovered, blind)

        elif type(obj) is Structure:
            return cls.render_structure(obj, uncovered, blind)

        elif type(obj) is Answer:
            return cls.render_answer(obj, uncovered, blind)

        else:
            raise UncoveredClassException("Can't render a '%s'" % type(obj).__name__)

    @classmethod
    def render_term(cls, term: 'Term', uncovered: bool = False, blind: bool = False):
        from defeasible.domain.theme import MUTE_VARIABLE
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import STRING
        from defeasible.domain.theme import TERM
        from defeasible.domain.theme import UNCOVERED
        from defeasible.domain.theme import VALUE
        from defeasible.domain.theme import VARIABLE

        if blind:
            return term

        if uncovered:
            return '%s%s%s' % (UNCOVERED, term, RESET)

        elif type(term) in [bool, float, int]:
            return '%s%s%s' % (VALUE, term, RESET)

        elif type(term) is str and re.match(r'[_A-Z][a-z_0-9]*', term):
            style = MUTE_VARIABLE if term.startswith('_') else VARIABLE
            return '%s%s%s' % (style, term, RESET)

        else:
            style = STRING if term[0] in ["'", '"'] else TERM
            return '%s%s%s' % (style, term, RESET)

    @classmethod
    def render_atom(cls, atom: 'Atom', uncovered: bool = False, blind: bool = False) -> str:
        content = cls.render_functor(atom, uncovered, blind)
        if atom.terms:
            content += cls.lpar(uncovered, blind)
            content += cls.comma(uncovered, blind).join(cls.render_term(term, uncovered, blind) for term in atom.terms)
            content += cls.rpar(uncovered, blind)

        return content

    @classmethod
    def render_functor(cls, atom: 'Atom', uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import FUNCTOR
        from defeasible.domain.theme import RESET
        from defeasible.domain.theme import UNCOVERED

        if blind:
            return atom.functor

        elif uncovered:
            return '%s%s%s' % (UNCOVERED, atom.functor, RESET)

        else:
            return '%s%s%s' % (FUNCTOR, atom.functor, RESET)

    @classmethod
    def render_literal(cls, literal: 'Literal', uncovered: bool = False, blind: bool = False) -> str:
        content = cls.render_atom(literal.atom, uncovered, blind)
        if literal.negated:
            content = cls.negate(uncovered, blind) + content

        return content

    @classmethod
    def render_rule(cls, rule: 'Rule', uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.definitions import RuleType

        content = cls.render_literal(rule.head, uncovered, blind)
        if rule.body or rule.type == RuleType.DEFEASIBLE:
            if rule.type == RuleType.STRICT:
                content += cls.strict(uncovered, blind)
            else:
                content += cls.defeasible(uncovered, blind)
        if rule.body:
            content += cls.comma(uncovered, blind).join(cls.render_literal(lit, False, blind) for lit in rule.body)
        content += cls.stop(uncovered, blind)

        return content

    @classmethod
    def render_comment(cls, comment: str, uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import COMMENT
        from defeasible.domain.theme import RESET

        return '%s%s%s' % (COMMENT, comment, RESET)

    @classmethod
    def render_rules(cls, program: 'Program', rules: Set['Rule'], uncovered: bool = False, blind: bool = False) -> str:
        index = {}
        for rule in rules:
            key = rule.head.atom
            uncovered = program.is_ground() and not bool(program.get_derivation(rule.head))
            index.setdefault(key, {}).setdefault(rule, uncovered)

        return '\n'.join(
            cls.render_rule(rule, index[atom][rule], blind)
            for atom in sorted(index)
            for rule in sorted(index[atom]),
        )

    @classmethod
    def render_program(cls, program: 'Program', uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.definitions import RuleType

        stricts = cls.render_rules(program, program.get_rules(RuleType.STRICT), uncovered, blind)
        if stricts:
            stricts = cls.render_comment('# Strict rules') + '\n' + stricts
        facts = cls.render_rules(program, program.get_facts(), uncovered, blind)
        if facts:
            facts = cls.render_comment('# Facts') + '\n' + facts

        defeasibles = cls.render_rules(program, program.get_rules(RuleType.DEFEASIBLE), uncovered, blind)
        defeasibles += cls.render_rules(program, program.get_presumptions(), uncovered, blind)
        if defeasibles:
            defeasibles = cls.render_comment('# Defeasible knowledge') + '\n' + defeasibles

        return '\n\n'.join(part for part in [stricts, facts, defeasibles] if part)

    @classmethod
    def render_derivation(cls, derivation: 'Derivation', uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.definitions import RuleType

        if len(derivation.rules) == 0:
            return cls.empty(uncovered, blind)

        if len(derivation.rules) == 1:
            return repr(derivation.rules[0].head)

        sequence = ', '.join(cls.render_literal(rule.head, uncovered, blind) for rule in derivation.rules[:-1])
        conclusion = cls.render_literal(derivation.rules[-1].head, uncovered, blind)
        if derivation.type == RuleType.DEFEASIBLE:
            return '%s %s %s' % (sequence, cls.defeasibly(uncovered, blind), conclusion)

        return '%s %s %s' % (sequence, cls.strictly(uncovered, blind), conclusion)

    @classmethod
    def render_structure(cls, structure: 'Structure', uncovered: bool = False, blind: bool = False) -> str:
        content = cls.lang(uncovered, blind)
        if not structure.argument:
            content += cls.empty(uncovered, blind)
        else:
            content += cls.lcur(uncovered, blind)
            content += cls.colon(uncovered, blind).join(cls.render_rule(rule) for rule in structure.argument)
            content += cls.rcur(uncovered, blind)
        content += cls.comma(uncovered, blind)
        content += cls.render_literal(structure.conclusion, uncovered, blind)
        content += cls.rang(uncovered, blind)

        return content

    @classmethod
    def render_answer(cls, answer: Answer, uncovered: bool = False, blind: bool = False) -> str:
        from defeasible.domain.theme import ANSWER
        from defeasible.domain.theme import RESET

        if blind:
            return answer.name

        else:
            return '%s%s%s' % (ANSWER, answer.name, RESET)
