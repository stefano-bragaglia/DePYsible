from unittest import TestCase

from arpeggio import NoMatch
from assertpy import assert_that, fail

from defeasible.definitions import Atom, Literal, Rule, RuleType


class TestAtom(TestCase):
    def test__atom___eq___0(self):
        assert_that(Atom('a', ['b', 5, True]) == None) \
            .is_false()

    def test__atom___eq___1(self):
        assert_that(Atom('a', ['b', 5, True]) == 'a(b, 5, True)') \
            .is_false()

    def test__atom___eq___2(self):
        assert_that(Atom('a', ['b', 5, True]) == Atom('a', [])) \
            .is_false()

    def test__atom___eq___3(self):
        assert_that(Atom('a', ['b', 5, True]) == Atom('a', [True, 5, 'b'])) \
            .is_false()

    def test__atom___eq___4(self):
        assert_that(Atom('a', ['b', 5, True]) == Atom('c', ['b', 5, True])) \
            .is_false()

    def test__atom___eq___5(self):
        assert_that(Atom('a', ['b', 5, True]) == Atom('a', ['b', 'b', 5, True])) \
            .is_false()

    def test__atom___eq___6(self):
        assert_that(Atom('a', ['b', 5, True]) == Atom('a', ['b', 5, True])) \
            .is_true()

    def test__atom___hash___00(self):
        assert_that(hash(Atom('a', ['b', 5, True]))) \
            .is_not_none()

    def test__atom___init___00(self):
        assert_that(Atom.__init__) \
            .raises(ValueError) \
            .when_called_with(Atom, None, ['b', 5, True]) \
            .is_equal_to("'functor' is none or empty")

    def test__atom___init___01(self):
        assert_that(Atom.__init__) \
            .raises(ValueError) \
            .when_called_with(Atom, ' ', ['b', 5, True]) \
            .is_equal_to("'functor' is none or empty")

    def test__atom___init___02(self):
        assert_that(Atom.__init__) \
            .raises(ValueError) \
            .when_called_with(Atom, 'a', None) \
            .is_equal_to("'terms' is none")

    def test__atom___init___03(self):
        atom = Atom('a', [])
        assert_that(atom.functor) \
            .is_equal_to('a')
        assert_that(atom.terms) \
            .is_empty()

    def test__atom___init___04(self):
        atom = Atom('a', ['b', 5, True])
        assert_that(atom.functor) \
            .is_equal_to('a')
        assert_that(atom.terms).contains_sequence('b', 5, True)

    def test__atom___lt___00(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = None
        try:
            result = item_1 < item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Atom() < NoneType()")

    def test__atom___lt___01(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = 'a(b, 5, True)'
        try:
            result = item_1 < item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Atom() < str()")

    def test__atom___lt___02(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', [])
        assert_that(item_1 < item_2) \
            .is_false()

    def test__atom___lt___03(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', [True, 5, 'b'])
        assert_that(item_1 < item_2) \
            .is_false()

    def test__atom___lt___04(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('c', ['b', 5, True])
        assert_that(item_1 < item_2) \
            .is_true()

    def test__atom___lt___05(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', ['b', 'b', 5, True])
        assert_that(item_1 < item_2) \
            .is_true()

    def test__atom___lt___06(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', ['b', 5, True])
        assert_that(item_1 < item_2) \
            .is_false()

    def test__atom___lt___07(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = None
        try:
            result = item_1 > item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Atom() > NoneType()")

    def test__atom___lt___08(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = 'a(b, 5, True)'
        try:
            result = item_1 > item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Atom() > str()")

    def test__atom___lt___09(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', [])
        assert_that(item_1 > item_2) \
            .is_true()

    def test__atom___lt___10(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', [True, 5, 'b'])
        assert_that(item_1 > item_2) \
            .is_true()

    def test__atom___lt___11(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('c', ['b', 5, True])
        assert_that(item_1 > item_2) \
            .is_false()

    def test__atom___lt___12(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', ['b', 'b', 5, True])
        assert_that(item_1 > item_2) \
            .is_false()

    def test__atom___lt___13(self):
        item_1 = Atom('a', ['b', 5, True])
        item_2 = Atom('a', ['b', 5, True])
        assert_that(item_1 > item_2) \
            .is_false()

    def test__atom___repr___0(self):
        atom = Atom('a', [])
        assert_that(repr(atom)) \
            .is_equal_to('a')

    def test__atom___repr___1(self):
        atom = Atom('a', ['b', 5, True])
        assert_that(repr(atom)) \
            .is_equal_to('a(b, 5, True)')


class TestLiteral(TestCase):
    def test__literal_parse__0(self):
        expected = Literal(False, Atom('a', []))
        assert_that(Literal.parse('a')) \
            .is_equal_to(expected)

    def test__literal_parse__1(self):
        expected = Literal(True, Atom('a', []))
        assert_that(Literal.parse('~a')) \
            .is_equal_to(expected)

    def test__literal_parse__2(self):
        expected = Literal(False, Atom('a', ['b', 5, True]))
        assert_that(Literal.parse('a(b, 5, True)')) \
            .is_equal_to(expected)

    def test__literal_parse__3(self):
        expected = Literal(True, Atom('a', ['b', 5, True]))
        assert_that(Literal.parse('~a(b, 5, True)')) \
            .is_equal_to(expected)

    def test__literal___eq___0(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == None) \
            .is_false()

    def test__literal___eq___1(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == 'a(b, 5, True)') \
            .is_false()

    def test__literal___eq___2(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(True, Atom('a', ['b', 5, True]))) \
            .is_false()

    def test__literal___eq___3(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('a', []))) \
            .is_false()

    def test__literal___eq___4(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('c', ['b', 5, True]))) \
            .is_false()

    def test__literal___eq___5(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('a', [5, True]))) \
            .is_false()

    def test__literal___eq___6(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('a', [True, 5, 'b']))) \
            .is_false()

    def test__literal___eq___7(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('a', ['b', 'b', 5, True]))) \
            .is_false()

    def test__literal___eq___8(self):
        assert_that(Literal(False, Atom('a', ['b', 5, True])) == Literal(False, Atom('a', ['b', 5, True]))) \
            .is_true()

    def test__literal___hash___00(self):
        assert_that(hash(Literal(False, Atom('a', ['b', 5, True])))) \
            .is_not_none()

    def test__literal___init___0(self):
        assert_that(Literal.__init__) \
            .raises(ValueError) \
            .when_called_with(Literal, None, Atom('a', ['b', 5, True])) \
            .is_equal_to("'negated' is none")

    def test__literal___init___1(self):
        assert_that(Literal.__init__) \
            .raises(ValueError) \
            .when_called_with(Literal, False, None) \
            .is_equal_to("'atom' is none")

    def test__literal___init___2(self):
        literal = Literal(False, Atom('a', ['b', 5, True]))
        assert_that(literal.negated) \
            .is_false()
        assert_that(literal.atom) \
            .is_equal_to(Atom('a', ['b', 5, True]))

    def test__literal___lt___00(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = None
        try:
            result = item_1 < item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() < NoneType()")

    def test__literal___lt___01(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Atom('a', ['b', 5, True])
        try:
            result = item_1 < item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() < Atom()")

    def test__literal___lt___02(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = 'a(b, 5, True)'
        try:
            result = item_1 < item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() < str()")

    def test__literal___lt___03(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(True, Atom('a', ['b', 5, True]))
        assert_that(item_1 < item_2) \
            .is_true()

    def test__literal___lt___04(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('c', ['b', 5, True]))
        assert_that(item_1 < item_2) \
            .is_true()

    def test__literal___lt___05(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', [5, True]))
        assert_that(item_1 < item_2) \
            .is_false()

    def test__literal___lt___06(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', ['b', 5, True]))
        assert_that(item_1 < item_2) \
            .is_false()

    def test__literal___lt___07(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', ['b', 'b', 5, True]))
        assert_that(item_1 < item_2) \
            .is_true()

    def test__literal___lt___08(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', [True, 5, 'b']))
        assert_that(item_1 < item_2) \
            .is_false()

    def test__literal___lt___09(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = None
        try:
            result = item_1 > item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() > NoneType()")

    def test__literal___lt___10(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Atom('a', ['b', 5, True])
        try:
            result = item_1 > item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() > Atom()")

    def test__literal___lt___11(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = 'a(b, 5, True)'
        try:
            result = item_1 > item_2
            fail('should have raised error')
        except TypeError as e:
            assert_that(str(e)) \
                .is_equal_to("unorderable types: Literal() > str()")

    def test__literal___lt___12(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(True, Atom('a', ['b', 5, True]))
        assert_that(item_1 > item_2) \
            .is_false()

    def test__literal___lt___13(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('c', ['b', 5, True]))
        assert_that(item_1 > item_2) \
            .is_false()

    def test__literal___lt___14(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', [5, True]))
        assert_that(item_1 > item_2) \
            .is_true()

    def test__literal___lt___15(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', ['b', 5, True]))
        assert_that(item_1 > item_2) \
            .is_false()

    def test__literal___lt___16(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', ['b', 'b', 5, True]))
        assert_that(item_1 > item_2) \
            .is_false()

    def test__literal___lt___17(self):
        item_1 = Literal(False, Atom('a', ['b', 5, True]))
        item_2 = Literal(False, Atom('a', [True, 5, 'b']))
        assert_that(item_1 > item_2) \
            .is_true()

    def test__literal___repr___0(self):
        literal = Literal(False, Atom('a', []))
        assert_that(repr(literal)) \
            .is_equal_to('a')

    def test__literal___repr___1(self):
        literal = Literal(True, Atom('a', []))
        assert_that(repr(literal)) \
            .is_equal_to('~a')

    def test__literal___repr___2(self):
        literal = Literal(False, Atom('a', ['b', 5, True]))
        assert_that(repr(literal)) \
            .is_equal_to('a(b, 5, True)')

    def test__literal___repr___3(self):
        literal = Literal(True, Atom('a', ['b', 5, True]))
        assert_that(repr(literal)) \
            .is_equal_to('~a(b, 5, True)')


class TestRule(TestCase):
    """
    none
    str

    head.
    head -< .
    ~head.
    ~head -< .
    head -< body.
    ~head -< body.
    head -< body, 'body'(b, 5, True).
    ~head -< body, 'body'(b, 5, True).

    head -< body, 'body'(b, 5, True), body.
    ~head -< body, 'body'(b, 5, True), body.
    """

    def test__rule__parse__failure(self):
        for content, expected in {
            '': "Expected comment or '~' or '\"' or ''' or identifier or '~' or '\"' or ''' or identifier "
                "at position (1, 1) => '*'.",
            'head': "Expected '(' or '-<' or '(' or '<-' or '.' at position (1, 5) => 'head*'.",
            'head <-': "Expected '~' or '\"' or ''' or identifier or '.' at position (1, 8) => 'head <-*'.",
            'head -<': "Expected '~' or '\"' or ''' or identifier or '.' at position (1, 8) => 'head -<*'.",
            'head <- body': "Expected '(' or ',' or '.' at position (1, 13) => 'ad <- body*'.",
            'head -< body': "Expected '(' or ',' or '.' at position (1, 13) => 'ad -< body*'.",
            'head <- body,': "Expected '~' or '\"' or ''' or identifier at position (1, 14) => 'd <- body,*'.",
            'head -< body,': "Expected '~' or '\"' or ''' or identifier at position (1, 14) => 'd -< body,*'.",
            'head <- body, ~"body"(b, 5, True)': "Expected ',' or '.' at position (1, 34) => ', 5, True)*'.",
            'head -< body, ~"body"(b, 5, True)': "Expected ',' or '.' at position (1, 34) => ', 5, True)*'.",
        }.items():
            with self.subTest(msg=content if content else '<empty>'):
                assert_that(Rule.parse) \
                    .raises(NoMatch) \
                    .when_called_with(content) \
                    .is_equal_to(expected)

    def test__rule_parse__success(self):
        for content, expected in {
            'head.': Rule(
                Literal(False, Atom('head', [])),
                RuleType.STRICT
            ),
            'head <- .': Rule(
                Literal(False, Atom('head', [])),
                RuleType.STRICT
            ),
            'head -< .': Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE
            ),
            'head <- body.': Rule(
                Literal(False, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
            ),
            'head -< body.': Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
            ),
            'head <- body, ~"body"(b, 5, True).': Rule(
                Literal(False, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            'head -< body, ~"body"(b, 5, True).': Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            'head <- body, body, ~"body"(b, 5, True).': Rule(
                Literal(False, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            'head -< body, body, ~"body"(b, 5, True).': Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            '~head.': Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT
            ),
            '~head <- .': Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT
            ),
            '~head -< .': Rule(
                Literal(True, Atom('head', [])),
                RuleType.DEFEASIBLE
            ),
            '~head <- body.': Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
            ),
            '~head -< body.': Rule(
                Literal(True, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
            ),
            '~head <- body, ~"body"(b, 5, True).': Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            '~head -< body, ~"body"(b, 5, True).': Rule(
                Literal(True, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            '~head <- body, body, ~"body"(b, 5, True).': Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
            '~head -< body, body, ~"body"(b, 5, True).': Rule(
                Literal(True, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
                Literal(True, Atom('body', ['b', 5, True])),
            ),
        }.items():
            with self.subTest(msg=content):
                assert_that(Rule.parse(content)) \
                    .described_as(content) \
                    .is_equal_to(expected)

    def test__rule___eq__00(self):
        item_1 = None
        item_2 = None
        assert_that(item_1 == item_2) \
            .is_true()

    def test__rule___eq__01(self):
        item_1 = None
        item_2 = "~head -< body, 'body'(b, 5, True)."
        assert_that(item_1 == item_2) \
            .is_true()
