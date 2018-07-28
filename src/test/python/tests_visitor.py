from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that


class TestDefeasibleVisitor(TestCase):
    @staticmethod
    def process(scope, content) -> dict:
        from defeasible.language.visitor import DefeasibleVisitor

        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, DefeasibleVisitor())

    def test__comment__0(self):
        from defeasible.language.grammar import comment

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(comment, '-other-') \
            .is_equal_to("Expected comment at position (1, 1) => '*-other-'.")

    def test__comment__1(self):
        from defeasible.language.grammar import comment

        assert_that(self.process(comment, "% comment")) \
            .is_equal_to('% comment')

    def test__program__0(self):
        from defeasible.language.grammar import program

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(program, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '~' or '\"' or ''' or identifier or EOF "
                         "at position (1, 1) => '*-other-'.")

    def test__program__1(self):
        from defeasible.domain.definitions import Program
        from defeasible.language.grammar import program

        expected = Program()
        assert_that(self.process(program, "")) \
            .is_equal_to(expected)

    def test__program__2(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Program
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import program

        expected = Program(
            Rule(
                Literal(False, Atom('fact', [])),
                RuleType.STRICT,
            )
        )
        assert_that(self.process(program, "fact.")) \
            .is_equal_to(expected)

    def test__program__3(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Program
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import program

        expected = Program(
            Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
            ),
            Rule(
                Literal(False, Atom('fact', [])),
                RuleType.STRICT,
            ),
        )
        assert_that(self.process(program, "fact.\nhead -< body.")) \
            .is_equal_to(expected)

    def test__program__4(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Program
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import program

        expected = Program(
            Rule(
                Literal(True, Atom('head', [])),
                RuleType.STRICT,
                Literal(False, Atom('body', [])),
            ),
            Rule(
                Literal(False, Atom('head', [])),
                RuleType.DEFEASIBLE,
                Literal(False, Atom('body', [])),
            ),
            Rule(
                Literal(False, Atom('fact', [])),
                RuleType.STRICT,
            ),
        )
        assert_that(self.process(program, "~head <- body. fact.\nhead -< body.")) \
            .is_equal_to(expected)

    def test__rule__00(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '~' or '\"' or ''' or identifier "
                         "at position (1, 1) => '*-other-'.")

    def test__rule__01(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head') \
            .is_equal_to("Expected '(' or '-<' or '(' or '<-' or '.' at position (1, 5) => 'head*'.")

    def test__rule__02(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
        )
        assert_that(self.process(rule, "head.")) \
            .is_equal_to(expected)

    def test__rule__03(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head -<') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '.' at position (1, 8) => 'head -<*'.")

    def test__rule__04(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head <-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '.' at position (1, 8) => 'head <-*'.")

    def test__rule__05(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
        )
        assert_that(self.process(rule, "head -< .")) \
            .is_equal_to(expected)

    def test__rule__06(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
        )
        assert_that(self.process(rule, "head <- .")) \
            .is_equal_to(expected)

    def test__rule__07(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head -< body_0') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 15) => ' -< body_0*'.")

    def test__rule__08(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head <- body_0') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 15) => ' <- body_0*'.")

    def test__rule__09(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
            Literal(False, Atom('body_0', [])),
        )
        assert_that(self.process(rule, "head -< body_0.")) \
            .is_equal_to(expected)

    def test__rule__10(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
            Literal(False, Atom('body_0', [])),
        )
        assert_that(self.process(rule, "head <- body_0.")) \
            .is_equal_to(expected)

    def test__rule__11(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head -< body_0, ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 17) => '< body_0, *'.")

    def test__rule__12(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head <- body_0, ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 17) => '- body_0, *'.")

    def test__rule__13(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head -< body_0, body_1') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 23) => '_0, body_1*'.")

    def test__rule__14(self):
        from defeasible.language.grammar import rule

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(rule, 'head <- body_0, body_1') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 23) => '_0, body_1*'.")

    def test__rule__15(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
            Literal(False, Atom('body_0', [])),
            Literal(False, Atom('body_1', [])),
        )
        assert_that(self.process(rule, "head -< body_0, body_1.")) \
            .is_equal_to(expected)

    def test__rule__16(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import rule

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
            Literal(False, Atom('body_0', [])),
            Literal(False, Atom('body_1', [])),
        )
        assert_that(self.process(rule, "head <- body_0, body_1.")) \
            .is_equal_to(expected)

    def test__defeasible__0(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__defeasible__1(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head') \
            .is_equal_to("Expected '(' or '-<' at position (1, 5) => 'head*'.")

    def test__defeasible__2(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head.') \
            .is_equal_to("Expected '(' or '-<' at position (1, 5) => 'head*.'.")

    def test__defeasible__3(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head -< ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '.' at position (1, 9) => 'head -< *'.")

    def test__defeasible__4(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import defeasible

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
        )
        assert_that(self.process(defeasible, "head -< .")) \
            .is_equal_to(expected)

    def test__defeasible__5(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head -< body_0') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 15) => ' -< body_0*'.")

    def test__defeasible__6(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import defeasible

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
            Literal(False, Atom('body_0', [])),
        )
        assert_that(self.process(defeasible, "head -< body_0.")) \
            .is_equal_to(expected)

    def test__defeasible__7(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head -< body_0, ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 17) => '< body_0, *'.")

    def test__defeasible__8(self):
        from defeasible.language.grammar import defeasible

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(defeasible, 'head -< body_0, body_1') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 23) => '_0, body_1*'.")

    def test__defeasible__9(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import defeasible

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.DEFEASIBLE,
            Literal(False, Atom('body_0', [])),
            Literal(False, Atom('body_1', [])),
        )
        assert_that(self.process(defeasible, "head -< body_0, body_1.")) \
            .is_equal_to(expected)

    def test__strict__0(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__strict__1(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, 'head') \
            .is_equal_to("Expected '(' or '<-' or '.' at position (1, 5) => 'head*'.")

    def test__strict__2(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import strict

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
        )
        assert_that(self.process(strict, "head.")) \
            .is_equal_to(expected)

    def test__strict__3(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, 'head <- ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier or '.' at position (1, 9) => 'head <- *'.")

    def test__strict__4(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import strict

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
        )
        assert_that(self.process(strict, "head <- .")) \
            .is_equal_to(expected)

    def test__strict__5(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, 'head <- body_0') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 15) => ' <- body_0*'.")

    def test__strict__6(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import strict

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
            Literal(False, Atom('body_0', [])),
        )
        assert_that(self.process(strict, "head <- body_0.")) \
            .is_equal_to(expected)

    def test__strict__7(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, 'head <- body_0, ') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 17) => '- body_0, *'.")

    def test__strict__8(self):
        from defeasible.language.grammar import strict

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(strict, 'head <- body_0, body_1') \
            .is_equal_to("Expected '(' or ',' or '.' at position (1, 23) => '_0, body_1*'.")

    def test__strict__9(self):
        from defeasible.domain.definitions import Atom
        from defeasible.domain.definitions import Literal
        from defeasible.domain.definitions import Rule
        from defeasible.domain.definitions import RuleType
        from defeasible.language.grammar import strict

        expected = Rule(
            Literal(False, Atom('head', [])),
            RuleType.STRICT,
            Literal(False, Atom('body_0', [])),
            Literal(False, Atom('body_1', [])),
        )
        assert_that(self.process(strict, "head <- body_0, body_1.")) \
            .is_equal_to(expected)

    def test__literals__00(self):
        from defeasible.language.grammar import literals

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(literals, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__literals__01(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literals

        expected = [
            Literal(False, Atom('"string"', [])),
        ]
        assert_that(
            self.process(literals, "\"string\"")) \
            .is_equal_to(expected)

    def test__literals__02(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literals

        expected = [
            Literal(False, Atom('"string"', [])),
            Literal(True, Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"'])),
        ]
        assert_that(
            self.process(literals, "\"string\", "
                                   "~identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__00(self):
        from defeasible.language.grammar import literal

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(literal, '-other-') \
            .is_equal_to("Expected '~' or '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__literal__01(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', []))
        assert_that(self.process(literal, "'string'")) \
            .is_equal_to(expected)

    def test__literal__02(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', []))
        assert_that(self.process(literal, "'string'()")) \
            .is_equal_to(expected)

    def test__literal__03(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "'string'(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__04(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', []))
        assert_that(self.process(literal, "identifier")) \
            .is_equal_to(expected)

    def test__literal__05(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', []))
        assert_that(self.process(literal, "identifier()")) \
            .is_equal_to(expected)

    def test__literal__06(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__07(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', []))
        assert_that(self.process(literal, "~'string'")) \
            .is_equal_to(expected)

    def test__literal__08(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', []))
        assert_that(self.process(literal, "~'string'()")) \
            .is_equal_to(expected)

    def test__literal__09(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "~'string'(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__10(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', []))
        assert_that(self.process(literal, "~identifier")) \
            .is_equal_to(expected)

    def test__literal__11(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', []))
        assert_that(self.process(literal, "~identifier()")) \
            .is_equal_to(expected)

    def test__literal__12(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "~identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__13(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', []))
        assert_that(self.process(literal, "~~'string'")) \
            .is_equal_to(expected)

    def test__literal__14(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', []))
        assert_that(self.process(literal, "~~'string'()")) \
            .is_equal_to(expected)

    def test__literal__15(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('"string"', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "~~'string'(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__16(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', []))
        assert_that(self.process(literal, "~~identifier")) \
            .is_equal_to(expected)

    def test__literal__17(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', []))
        assert_that(self.process(literal, "~~identifier()")) \
            .is_equal_to(expected)

    def test__literal__18(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(False, Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(
            self.process(literal, "~~identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__19(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', []))
        assert_that(self.process(literal, "~~~'string'")) \
            .is_equal_to(expected)

    def test__literal__20(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', []))
        assert_that(self.process(literal, "~~~'string'()")) \
            .is_equal_to(expected)

    def test__literal__21(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('"string"', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(
            self.process(literal, "~~~'string'(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__literal__22(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', []))
        assert_that(self.process(literal, "~~~identifier")) \
            .is_equal_to(expected)

    def test__literal__23(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', []))
        assert_that(self.process(literal, "~~~identifier()")) \
            .is_equal_to(expected)

    def test__literal__24(self):
        from defeasible.domain.definitions import Atom, Literal
        from defeasible.language.grammar import literal

        expected = Literal(True, Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"']))
        assert_that(self.process(literal, "~~~identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__negation__0(self):
        from defeasible.language.grammar import negation

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(negation, '-other-') \
            .starts_with("Expected '~' at position (1, 1) => '*-other-'.")

    def test__negation__1(self):
        from defeasible.language.grammar import negation

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(negation, '') \
            .starts_with("Expected '~' at position (1, 1) => '*'.")

    def test__negation__2(self):
        from defeasible.language.grammar import negation

        assert_that(self.process(negation, '~')) \
            .is_true()

    def test__negation__3(self):
        from defeasible.language.grammar import negation

        assert_that(self.process(negation, '~~')) \
            .is_false()

    def test__negation__4(self):
        from defeasible.language.grammar import negation

        assert_that(self.process(negation, '~~~')) \
            .is_true()

    def test__atom__0(self):
        from defeasible.language.grammar import atom

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(atom, '-other-') \
            .is_equal_to("Expected '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__atom__1_0(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('"string"', [])
        assert_that(self.process(atom, "'String'")) \
            .is_equal_to(expected)

    def test__atom__2_0(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('"tring"', [])
        assert_that(self.process(atom, "'String'()")) \
            .is_equal_to(expected)

    def test__atom__1(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('"String"', [])
        assert_that(self.process(atom, "'String'")) \
            .is_equal_to(expected)

    def test__atom__2(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('"String"', [])
        assert_that(self.process(atom, "'String'()")) \
            .is_equal_to(expected)

    def test__atom__3(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('"string"', [True, False, 'identifier', 123, -0.012, '"double"', '"single"'])
        assert_that(self.process(atom, "'string'(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__atom__4(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('identifier', [])
        assert_that(self.process(atom, "identifier")) \
            .is_equal_to(expected)

    def test__atom__5(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('identifier', [])
        assert_that(self.process(atom, "identifier()")) \
            .is_equal_to(expected)

    def test__atom__6(self):
        from defeasible.domain.definitions import Atom
        from defeasible.language.grammar import atom

        expected = Atom('identifier', [True, False, 'identifier', 123, -0.012, '"double"', '"single"'])
        assert_that(self.process(atom, "identifier(True, False, identifier, 123, -1.2E-2, \"double\", 'single')")) \
            .is_equal_to(expected)

    def test__functor__0(self):
        from defeasible.language.grammar import functor

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(functor, '-other-') \
            .is_equal_to("Expected '\"' or ''' or identifier at position (1, 1) => '*-other-'.")

    def test__functor__1(self):
        from defeasible.language.grammar import functor

        assert_that(self.process(functor, 'double_quote"')) \
            .is_equal_to('double_quote')

    def test__functor__2(self):
        from defeasible.language.grammar import functor

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(functor, '"double_quote') \
            .is_equal_to("Expected '\"' at position (1, 14) => 'uble_quote*'.")

    def test__functor__3(self):
        from defeasible.language.grammar import functor

        assert_that(self.process(functor, '"double_quote"')) \
            .is_equal_to('"double_quote"')

    def test__functor__4(self):
        from defeasible.language.grammar import functor

        assert_that(self.process(functor, 'identifier')) \
            .is_equal_to('identifier')

    def test__functor__5(self):
        from defeasible.language.grammar import functor

        assert_that(self.process(functor, "single_quote'")) \
            .is_equal_to('single_quote')

    def test__functor__6(self):
        from defeasible.language.grammar import functor

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(functor, "'single_quote") \
            .is_equal_to("Expected ''' at position (1, 14) => 'ngle_quote*'.")

    def test__functor__7(self):
        from defeasible.language.grammar import functor

        assert_that(self.process(functor, "'single_quote'")) \
            .is_equal_to('"single_quote"')

    def test__terms__0(self):
        from defeasible.language.grammar import terms

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(terms, '-other-') \
            .starts_with("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*-other-'.")

    def test__terms__1(self):
        from defeasible.language.grammar import terms

        assert_that(self.process(terms, 'true, false, identifier_0, 123, -1.2E-2, \'single\', "double"')) \
            .contains_only(True, False, 'identifier_0', 123, -0.012, '"single"', '"double"') \
            .contains_sequence(True, False, 'identifier_0', 123, -0.012, '"single"', '"double"')

    def test__term__00(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '-other-') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*-other-'.")

    def test__term__01(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "FALSE")) \
            .is_false()

    def test__term__02(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "False")) \
            .is_false()

    def test__term__03(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "false")) \
            .is_false()

    def test__term__04(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "TRUE")) \
            .is_true()

    def test__term__05(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "True")) \
            .is_true()

    def test__term__06(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "true")) \
            .is_true()

    def test__term__07(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '_identifier') \
            .starts_with("Expected identifier at position (1, 1) => '*_identifie'.")

    def test__term__08(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, 'identifier')) \
            .is_equal_to('identifier')

    def test__term__09(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, 'identi_fier')) \
            .is_equal_to('identi_fier')

    def test__term__10(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, 'identifier_0')) \
            .is_equal_to('identifier_0')

    def test__term__11(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '123')) \
            .is_equal_to(123)

    def test__term__12(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-123')) \
            .is_equal_to(-123)

    def test__term__13(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '0123')) \
            .is_equal_to(123)

    def test__term__14(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--123') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--123'.")

    def test__term__15(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '123')) \
            .is_equal_to(123)

    def test__term__16(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '123.')) \
            .is_equal_to(123)

    def test__term__17(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '.123')) \
            .is_equal_to(0.123)

    def test__term__18(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-123')) \
            .is_equal_to(-123)

    def test__term__19(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-123.')) \
            .is_equal_to(-123)

    def test__term__20(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '.-123') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*.-123'.")

    def test__term__21(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-.123')) \
            .is_equal_to(-0.123)

    def test__term__22(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--123') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--123'.")

    def test__term__23(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--123.') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--123.'.")

    def test__term__24(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--.123') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--.123'.")

    def test__term__25(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '1.2E-2')) \
            .is_equal_to(0.012)

    def test__term__26(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '1.2E2')) \
            .is_equal_to(120.0)

    def test__term__27(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-1.2E-2')) \
            .is_equal_to(-0.012)

    def test__term__28(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '-1.2E2')) \
            .is_equal_to(-120.0)

    def test__term__29(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--1.2E-2') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--1.2E-2'.")

    def test__term__30(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '--1.2E2') \
            .is_equal_to("Expected false or true or real or integer or '\"' or ''' or identifier "
                         "at position (1, 1) => '*--1.2E2'.")

    def test__term__31(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, 'string"')) \
            .is_equal_to('string')

    def test__term__32(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, '"string') \
            .is_equal_to("Expected '\"' at position (1, 8) => '\"string*'.")

    def test__term__33(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, '"string"')) \
            .is_equal_to('"string"')

    def test__term__34(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "string'")) \
            .is_equal_to('string')

    def test__term__35(self):
        from defeasible.language.grammar import term

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(term, "'string") \
            .is_equal_to("Expected ''' at position (1, 8) => ''string*'.")

    def test__term__36(self):
        from defeasible.language.grammar import term

        assert_that(self.process(term, "'string'")) \
            .is_equal_to('"string"')

    def test__boolean__0(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(boolean, '-other-') \
            .is_equal_to("Expected false or true at position (1, 1) => '*-other-'.")

    def test__boolean__1(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "FALSE")) \
            .is_false()

    def test__boolean__2(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "False")) \
            .is_false()

    def test__boolean__3(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "false")) \
            .is_false()

    def test__boolean__4(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "TRUE")) \
            .is_true()

    def test__boolean__5(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "True")) \
            .is_true()

    def test__boolean__6(self):
        from defeasible.language.grammar import boolean

        assert_that(self.process(boolean, "true")) \
            .is_true()

    def test__false__0(self):
        from defeasible.language.grammar import false

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(false, '-other-') \
            .is_equal_to("Expected false at position (1, 1) => '*-other-'.")

    def test__false__1(self):
        from defeasible.language.grammar import false

        assert_that(self.process(false, "FALSE")) \
            .is_false()

    def test__false__2(self):
        from defeasible.language.grammar import false

        assert_that(self.process(false, "False")) \
            .is_false()

    def test__false__3(self):
        from defeasible.language.grammar import false

        assert_that(self.process(false, "false")) \
            .is_false()

    def test__true__0(self):
        from defeasible.language.grammar import true

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(true, '-other-') \
            .is_equal_to("Expected true at position (1, 1) => '*-other-'.")

    def test__true__1(self):
        from defeasible.language.grammar import true

        assert_that(self.process(true, "TRUE")) \
            .is_true()

    def test__true__2(self):
        from defeasible.language.grammar import true

        assert_that(self.process(true, "True")) \
            .is_true()

    def test__true__3(self):
        from defeasible.language.grammar import true

        assert_that(self.process(true, "true")) \
            .is_true()

    def test__number__00(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '-other-') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*-other-'.")

    def test__number__01(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '123')) \
            .is_equal_to(123)

    def test__number__02(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-123')) \
            .is_equal_to(-123)

    def test__number__03(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '0123')) \
            .is_equal_to(123)

    def test__number__04(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--123') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--123'.")

    def test__number__05(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '123')) \
            .is_equal_to(123)

    def test__number__06(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '123.')) \
            .is_equal_to(123)

    def test__number__07(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '.123')) \
            .is_equal_to(0.123)

    def test__number__08(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-123')) \
            .is_equal_to(-123)

    def test__number__09(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-123.')) \
            .is_equal_to(-123)

    def test__number__10(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '.-123') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*.-123'.")

    def test__number__11(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-.123')) \
            .is_equal_to(-0.123)

    def test__number__12(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--123') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--123'.")

    def test__number__13(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--123.') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--123.'.")

    def test__number__14(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--.123') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--.123'.")

    def test__number__15(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '1.2E-2')) \
            .is_equal_to(0.012)

    def test__number__16(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '1.2E2')) \
            .is_equal_to(120.0)

    def test__number__17(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-1.2E-2')) \
            .is_equal_to(-0.012)

    def test__number__18(self):
        from defeasible.language.grammar import number

        assert_that(self.process(number, '-1.2E2')) \
            .is_equal_to(-120.0)

    def test__number__19(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--1.2E-2') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--1.2E-2'.")

    def test__number__20(self):
        from defeasible.language.grammar import number

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(number, '--1.2E2') \
            .is_equal_to("Expected real or integer at position (1, 1) => '*--1.2E2'.")

    def test__real__00(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '-other-') \
            .is_equal_to("Expected real at position (1, 1) => '*-other-'.")

    def test__real__01(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '123') \
            .is_equal_to("Expected real at position (1, 1) => '*123'.")

    def test__real__02(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '123.') \
            .is_equal_to("Expected real at position (1, 1) => '*123.'.")

    def test__real__03(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '.123')) \
            .is_equal_to(0.123)

    def test__real__04(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '-123') \
            .is_equal_to("Expected real at position (1, 1) => '*-123'.")

    def test__real__05(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '-123.') \
            .is_equal_to("Expected real at position (1, 1) => '*-123.'.")

    def test__real__06(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '.-123') \
            .is_equal_to("Expected real at position (1, 1) => '*.-123'.")

    def test__real__07(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '-.123')) \
            .is_equal_to(-0.123)

    def test__real__08(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '--123') \
            .is_equal_to("Expected real at position (1, 1) => '*--123'.")

    def test__real__09(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '--123.') \
            .is_equal_to("Expected real at position (1, 1) => '*--123.'.")

    def test__real__10(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '--.123') \
            .is_equal_to("Expected real at position (1, 1) => '*--.123'.")

    def test__real__11(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '1.2E-2')) \
            .is_equal_to(0.012)

    def test__real__12(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '1.2E2')) \
            .is_equal_to(120.0)

    def test__real__13(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '-1.2E-2')) \
            .is_equal_to(-0.012)

    def test__real__14(self):
        from defeasible.language.grammar import real

        assert_that(self.process(real, '-1.2E2')) \
            .is_equal_to(-120.0)

    def test__real__15(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '--1.2E-2') \
            .is_equal_to("Expected real at position (1, 1) => '*--1.2E-2'.")

    def test__real__16(self):
        from defeasible.language.grammar import real

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(real, '--1.2E2') \
            .is_equal_to("Expected real at position (1, 1) => '*--1.2E2'.")

    def test__integer__0(self):
        from defeasible.language.grammar import integer

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(integer, '-other-') \
            .is_equal_to("Expected integer at position (1, 1) => '*-other-'.")

    def test__integer__1(self):
        from defeasible.language.grammar import integer

        assert_that(self.process(integer, '123')) \
            .is_equal_to(123)

    def test__integer__2(self):
        from defeasible.language.grammar import integer

        assert_that(self.process(integer, '-123')) \
            .is_equal_to(-123)

    def test__integer__3(self):
        from defeasible.language.grammar import integer

        assert_that(self.process(integer, '0123')) \
            .is_equal_to(123)

    def test__integer__4(self):
        from defeasible.language.grammar import integer

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(integer, '--123') \
            .is_equal_to("Expected integer at position (1, 1) => '*--123'.")

    def test__string__0(self):
        from defeasible.language.grammar import string

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(string, '-other-') \
            .is_equal_to("Expected '\"' or ''' at position (1, 1) => '*-other-'.")

    def test__string__1(self):
        from defeasible.language.grammar import string

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(string, 'string"') \
            .is_equal_to("Expected '\"' or ''' at position (1, 1) => '*string\"'.")

    def test__string__2(self):
        from defeasible.language.grammar import string

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(string, '"string') \
            .is_equal_to("Expected '\"' at position (1, 8) => '\"string*'.")

    def test__string__3(self):
        from defeasible.language.grammar import string

        assert_that(self.process(string, '"string"')) \
            .is_equal_to('"string"')

    def test__string__4(self):
        from defeasible.language.grammar import string

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(string, "string'") \
            .is_equal_to("Expected '\"' or ''' at position (1, 1) => '*string''.")

    def test__string__5(self):
        from defeasible.language.grammar import string

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(string, "'string") \
            .is_equal_to("Expected ''' at position (1, 8) => ''string*'.")

    def test__string__6(self):
        from defeasible.language.grammar import string

        assert_that(self.process(string, "'string'")) \
            .is_equal_to('"string"')

    def test__double_quote__0(self):
        from defeasible.language.grammar import double_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(double_quote, '-other-') \
            .is_equal_to("Expected '\"' at position (1, 1) => '*-other-'.")

    def test__double_quote__1(self):
        from defeasible.language.grammar import double_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(double_quote, 'double_quote"') \
            .is_equal_to("Expected '\"' at position (1, 1) => '*double_quo'.")

    def test__double_quote__2(self):
        from defeasible.language.grammar import double_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(double_quote, '"double_quote') \
            .is_equal_to("Expected '\"' at position (1, 14) => 'uble_quote*'.")

    def test__double_quote__3(self):
        from defeasible.language.grammar import double_quote

        assert_that(self.process(double_quote, '"double_quote"')) \
            .is_equal_to('"double_quote"')

    def test__single_quote__0(self):
        from defeasible.language.grammar import single_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(single_quote, '-other-') \
            .is_equal_to("Expected ''' at position (1, 1) => '*-other-'.")

    def test__single_quote__1(self):
        from defeasible.language.grammar import single_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(single_quote, "single_quote'") \
            .is_equal_to("Expected ''' at position (1, 1) => '*single_quo'.")

    def test__single_quote__2(self):
        from defeasible.language.grammar import single_quote

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(single_quote, "'single_quote") \
            .is_equal_to("Expected ''' at position (1, 14) => 'ngle_quote*'.")

    def test__single_quote__3(self):
        from defeasible.language.grammar import single_quote

        assert_that(self.process(single_quote, "'single_quote'")) \
            .is_equal_to('"single_quote"')

    def test__identifier__0(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '-other-') \
            .starts_with("Expected identifier at position (1, 1) => '*-other-'.")

    def test__identifier__1(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '_identifier') \
            .starts_with("Expected identifier at position (1, 1) => '*_identifie'.")

    def test__identifier__2(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process(identifier, 'identifier')) \
            .is_equal_to('identifier')

    def test__identifier__3(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process(identifier, 'identi_fier')) \
            .is_equal_to('identi_fier')

    def test__identifier__4(self):
        from defeasible.language.grammar import identifier

        assert_that(self.process(identifier, 'identifier_0')) \
            .is_equal_to('identifier_0')
