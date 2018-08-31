import re
from collections import namedtuple
from typing import Any
from typing import Set

from colorama import Back
from colorama import Fore
from colorama import Style

from depysible.domain.interpretation import Answer, Derivation, Structure

Format = namedtuple('Format', 'back fore style')

MAIN = Format(Back.RESET, Fore.BLUE, Style.NORMAL)
COMMAND = Format(Back.RESET, Fore.YELLOW, Style.NORMAL)
LOCATION = Format(Back.RESET, Fore.GREEN, Style.NORMAL)
PERSON = Format(Back.RESET, Fore.YELLOW, Style.NORMAL)
TITLE = Format(Back.RESET, Fore.BLUE, Style.NORMAL)
URL = Format(Back.RESET, Fore.RED, Style.NORMAL)
VALUE = Format(Back.RESET, Fore.CYAN, Style.NORMAL)
MUTED = Format(Back.RESET, Fore.LIGHTWHITE_EX, Style.DIM)


def render_as(content: Any, format: Format, blind: bool = False) -> str:
    if blind:
        return content

    return '%s%s%s%s%s%s%s' % (format.back, format.fore, format.style, content, Back.RESET, Fore.RESET, Style.RESET_ALL)


class Renderer:

    @staticmethod
    def comma(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return ', '

        else:
            return '%s, %s' % (PUNCTUATION, RESET)

    @staticmethod
    def colon(blind: bool = False) -> str:
        from depysible.domain.theme import ARGUMENTATION
        from depysible.domain.theme import RESET

        if blind:
            return ' ; '

        else:
            return '%s ; %s' % (ARGUMENTATION, RESET)

    @staticmethod
    def empty(blind: bool = False) -> str:
        from depysible.domain.theme import ARGUMENTATION
        from depysible.domain.theme import RESET

        if blind:
            return '∅'

        else:
            return '%s∅%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def lcur(blind: bool = False) -> str:
        from depysible.domain.theme import ARGUMENTATION
        from depysible.domain.theme import RESET

        if blind:
            return '{'

        else:
            return '%s{%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def rcur(blind: bool = False) -> str:
        from depysible.domain.theme import ARGUMENTATION
        from depysible.domain.theme import RESET

        if blind:
            return '}'

        else:
            return '%s}%s' % (ARGUMENTATION, RESET)

    @staticmethod
    def lpar(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return '('

        else:
            return '%s(%s' % (PUNCTUATION, RESET)

    @staticmethod
    def rpar(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return ')'

        else:
            return '%s)%s' % (PUNCTUATION, RESET)

    @staticmethod
    def lang(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return '<'

        else:
            return '%s<%s' % (PUNCTUATION, RESET)

    @staticmethod
    def rang(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return '>'

        else:
            return '%s>%s' % (PUNCTUATION, RESET)

    @staticmethod
    def stop(blind: bool = False) -> str:
        from depysible.domain.theme import PUNCTUATION
        from depysible.domain.theme import RESET

        if blind:
            return '.'

        else:
            return '%s.%s' % (PUNCTUATION, RESET)

    @staticmethod
    def negate(blind: bool = False) -> str:
        from depysible.domain.theme import NEGATION
        from depysible.domain.theme import RESET

        if blind:
            return '~'

        else:
            return '%s~%s' % (NEGATION, RESET)

    @staticmethod
    def strict(blind: bool = False) -> str:
        from depysible.domain.theme import STRICT
        from depysible.domain.theme import RESET

        if blind:
            return ' <- '

        else:
            return '%s <- %s' % (STRICT, RESET)

    @staticmethod
    def defeasible(blind: bool = False) -> str:
        from depysible.domain.theme import DEFEASIBLE
        from depysible.domain.theme import RESET

        if blind:
            return ' -< '

        else:
            return '%s -< %s' % (DEFEASIBLE, RESET)

    @staticmethod
    def strictly(blind: bool = False) -> str:
        from depysible.domain.theme import STRICT
        from depysible.domain.theme import RESET

        if blind:
            return ' |- '

        else:
            return '%s |- %s' % (STRICT, RESET)

    @staticmethod
    def defeasibly(blind: bool = False) -> str:
        from depysible.domain.theme import DEFEASIBLE
        from depysible.domain.theme import RESET

        if blind:
            return ' |~ '

        else:
            return '%s |~ %s' % (DEFEASIBLE, RESET)

    @classmethod
    def render(cls, obj: Any, blind: bool = False) -> str:
        from depysible.domain.definitions import Atom
        from depysible.domain.definitions import Literal
        from depysible.domain.definitions import Rule
        from depysible.domain.definitions import Program

        if type(obj) in [bool, int, float, str]:
            return cls.render_term(obj, blind)

        elif type(obj) is Atom:
            return cls.render_atom(obj, blind)

        elif type(obj) is Literal:
            return cls.render_literal(obj, blind)

        elif type(obj) is Rule:
            return cls.render_rule(obj, blind)

        elif type(obj) is Program:
            return cls.render_program(obj, blind)

        elif type(obj) is Derivation:
            return cls.render_derivation(obj, blind)

        elif type(obj) is Structure:
            return cls.render_structure(obj, blind)

        elif type(obj) is Answer:
            return cls.render_answer(obj, blind)

        else:
            raise ValueError("Can't render a '%s'" % type(obj).__name__)

    @classmethod
    def render_term(cls, term: 'Term', blind: bool = False):
        from depysible.domain.theme import MUTE_VARIABLE
        from depysible.domain.theme import RESET
        from depysible.domain.theme import STRING
        from depysible.domain.theme import TERM
        from depysible.domain.theme import VALUE
        from depysible.domain.theme import VARIABLE

        if blind:
            return term

        elif type(term) in [bool, float, int]:
            return '%s%s%s' % (VALUE, term, RESET)

        elif type(term) is str and re.match(r'[_A-Z][a-z_0-9]*', term):
            style = MUTE_VARIABLE if term.startswith('_') else VARIABLE
            return '%s%s%s' % (style, term, RESET)

        else:
            style = STRING if term[0] in ["'", '"'] else TERM
            return '%s%s%s' % (style, term, RESET)

    @classmethod
    def render_atom(cls, atom: 'Atom', blind: bool = False) -> str:
        content = cls.render_functor(atom, blind)
        if atom.terms:
            content += cls.lpar(blind)
            content += cls.comma(blind).join(cls.render_term(term, blind) for term in atom.terms)
            content += cls.rpar(blind)

        return content

    @classmethod
    def render_functor(cls, atom: 'Atom', blind: bool = False) -> str:
        from depysible.domain.theme import FUNCTOR
        from depysible.domain.theme import RESET

        if blind:
            return atom.functor

        else:
            return '%s%s%s' % (FUNCTOR, atom.functor, RESET)

    @classmethod
    def render_literal(cls, literal: 'Literal', blind: bool = False) -> str:
        content = cls.render_atom(literal.atom, blind)
        if literal.negated:
            content = cls.negate(blind) + content

        return content

    @classmethod
    def render_rule(cls, rule: 'Rule', blind: bool = False) -> str:
        from depysible.domain.definitions import RuleType

        content = cls.render_literal(rule.head, blind)
        if rule.body or rule.type == RuleType.DEFEASIBLE:
            if rule.type == RuleType.STRICT:
                content += cls.strict(blind)
            else:
                content += cls.defeasible(blind)
        if rule.body:
            content += cls.comma(blind).join(cls.render_literal(lit, blind) for lit in rule.body)
        content += cls.stop(blind)

        return content

    @classmethod
    def render_comment(cls, comment: str, blind: bool = False) -> str:
        from depysible.domain.theme import COMMENT
        from depysible.domain.theme import RESET

        return '%s%s%s' % (COMMENT, comment, RESET)

    @classmethod
    def render_rules(cls, program: 'Program', rules: Set['Rule'], blind: bool = False) -> str:
        return '\n'.join(cls.render_rule(rule, blind) for rule in sorted(rules))

    @classmethod
    def render_program(cls, program: 'Program', blind: bool = False) -> str:
        from depysible.domain.definitions import RuleType

        stricts = cls.render_rules(program, program.get_rules(RuleType.STRICT), blind)
        if stricts:
            stricts = cls.render_comment('# Strict rules') + '\n' + stricts
        facts = cls.render_rules(program, program.get_facts(), blind)
        if facts:
            facts = cls.render_comment('# Facts') + '\n' + facts

        defeasibles = cls.render_rules(program, program.get_rules(RuleType.DEFEASIBLE), blind)
        defeasibles += cls.render_rules(program, program.get_presumptions(), blind)
        if defeasibles:
            defeasibles = cls.render_comment('# Defeasible knowledge') + '\n' + defeasibles

        return '\n\n'.join(part for part in [stricts, facts, defeasibles] if part)

    @classmethod
    def render_derivation(cls, derivation: 'Derivation', blind: bool = False) -> str:
        from depysible.domain.definitions import RuleType

        explanation = cls.comma(blind=blind).join(
            cls.render_literal(rule.head, blind=blind)
            for rule in reversed(derivation.rules)
        )
        if any(rule.type == RuleType.DEFEASIBLE for rule in derivation.rules):
            symbol = cls.defeasibly(blind=blind)
        else:
            symbol = cls.strictly(blind=blind)
        derivable = cls.render_literal(derivation.rules[0].head, blind=blind)

        return '%s %s %s' % (explanation, symbol, derivable)

    @classmethod
    def render_structure(cls, structure: 'Structure', blind: bool = False) -> str:
        content = cls.lang(blind)
        if not structure.argument:
            content += cls.empty(blind)
        else:
            content += cls.lcur(blind)
            content += cls.colon(blind).join(cls.render_rule(rule) for rule in structure.argument)
            content += cls.rcur(blind)
        content += cls.comma(blind)
        content += cls.render_literal(structure.conclusion, blind)
        content += cls.rang(blind)

        return content

    @classmethod
    def render_answer(cls, answer: Answer, blind: bool = False) -> str:
        from depysible.domain.theme import ANSWER
        from depysible.domain.theme import RESET

        if blind:
            return answer.name

        else:
            return '%s%s%s' % (ANSWER, answer.name, RESET)
