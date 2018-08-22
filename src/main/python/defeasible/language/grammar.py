from arpeggio import EOF, OneOrMore, Optional, RegExMatch, ZeroOrMore


def nothing():
    return EOF


def comment():
    return RegExMatch(r"%.*")


def program():
    return ZeroOrMore(rule), EOF


def rule():
    return [defeasible, strict]


def defeasible():
    return literal, '-<', Optional(literals), '.'


def strict():
    return literal, Optional('<-', Optional(literals)), '.'


def literals():
    return literal, ZeroOrMore(',', literal)


def literal():
    return Optional(negation), atom


def negation():
    return OneOrMore('~')


def atom():
    return functor, Optional('(', Optional(terms), ')')


def functor():
    return [double_quote, single_quote, identifier]


def terms():
    return term, ZeroOrMore(',', term)


def term():
    return [boolean, number, string, identifier, variable]


def boolean():
    return [false, true]


def false():
    return RegExMatch(r"FALSE", ignore_case=True)


def true():
    return RegExMatch(r"TRUE", ignore_case=True)


def number():
    return [real, integer]


def real():
    return RegExMatch(r"-?\d*\.\d+(E-?\d+)?")


def integer():
    return RegExMatch(r"-?\d+")


def string():
    return [double_quote, single_quote]


def double_quote():
    return '"', RegExMatch(r'[^"]*'), '"'


def single_quote():
    return "'", RegExMatch(r"[^']*"), "'"


def identifier():
    return RegExMatch(r'[a-z][a-zA-Z_0-9]*')


def variable():
    return RegExMatch(r'[_A-Z][a-zA-Z_0-9]*')
