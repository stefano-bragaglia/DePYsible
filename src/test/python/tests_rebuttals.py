from unittest import TestCase

from assertpy import assert_that

from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Program
from defeasible.domain.definitions import Rule
from defeasible.domain.interpretation import Derivation
from defeasible.domain.interpretation import Interpreter
from defeasible.domain.interpretation import disagree


class TestRebuttals(TestCase):
    def test__disagreement__0(self):
        literal1 = Literal.parse('a')
        literal2 = Literal.parse('~a')
        result = disagree(literal1, literal2, {})

        assert_that(result).is_true()

    def test__disagreement__1(self):
        literal1 = Literal.parse('a')
        literal2 = Literal.parse('b')
        program = Program.parse('~h <- b. h <- a.')
        result = disagree(literal1, literal2, program.rules)

        assert_that(result).is_true()

    def test__disagreement__2(self):
        literal1 = Literal.parse('a')
        literal2 = Literal.parse('c')
        program = Program.parse('~h <- b. h <- a.')
        result = disagree(literal1, literal2, program.rules)

        assert_that(result).is_false()

    def test__is_counter_argument_of__0(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tweety) <- penguin(tweety).'),
            Rule.parse('penguin(tweety).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()

        assert_that(s1.is_counter_argument_of(s2, s2)).is_false()
        assert_that(s2.is_counter_argument_of(s1, s1)).is_false()

    def test__is_counter_argument_of__1(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        result = s1.is_counter_argument_of(s2, s2)

        assert_that(result).is_true()

    def test__is_counter_argument_of__2(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        result = s2.is_counter_argument_of(s1, s1)

        assert_that(result).is_true()

    def test__is_counter_argument_of__3(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s1.is_counter_argument_of(s2, s3)

        assert_that(result).is_true()

    def test__is_counter_argument_of__4(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s1.is_counter_argument_of(s3, s2)

        assert_that(result).is_false()

    def test__is_counter_argument_of__5(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s2.is_counter_argument_of(s1, s3)

        assert_that(result).is_false()

    def test__is_counter_argument_of__6(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s2.is_counter_argument_of(s3, s1)

        assert_that(result).is_false()

    def test__is_counter_argument_of__7(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s3.is_counter_argument_of(s1, s2)

        assert_that(result).is_false()

    def test__is_counter_argument_of__8(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('nests_in_trees(tina) -< flies(tina).'),
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        d3 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s3 = d3.get_structure()
        result = s3.is_counter_argument_of(s2, s1)

        assert_that(result).is_false()

    def test__is_counter_argument_of__9(self):
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
        i = Interpreter(p)
        d1 = Derivation([
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s1 = d1.get_structure()
        result = s1.is_counter_argument_of(s1, s1)

        assert_that(result).is_false()
