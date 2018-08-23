from unittest import TestCase

from assertpy import assert_that

from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Program
from defeasible.domain.definitions import Rule
from defeasible.domain.interpretation import Derivation
from defeasible.domain.interpretation import Interpreter
from defeasible.domain.interpretation import Structure


class TestArgumentation(TestCase):
    def test__get_structure__bird_tina__strict(self):
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
        d = Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)
        expected = Structure(set(), Literal.parse('bird(tina)'), d)
        result = d.get_structure()

        assert_that(result).is_equal_to(expected)
        assert_that(result.is_strict()).is_true()

    def test__get_structure__not_flies_tina__not_strict(self):
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
        d = Derivation([Rule.parse('~flies(tina) -< chicken(tina).'), Rule.parse('chicken(tina).')], i)
        expected = Structure({Rule.parse('~flies(tina) -< chicken(tina).')}, Literal.parse('~flies(tina)'), d)
        result = d.get_structure()

        assert_that(result).is_equal_to(expected)
        assert_that(result.is_strict()).is_false()

    def test__get_structure__flies_tina_1__not_strict(self):
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
        d = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        expected = Structure({Rule.parse('flies(tina) -< bird(tina).')}, Literal.parse('flies(tina)'), d)
        result = d.get_structure()

        assert_that(result).is_equal_to(expected)
        assert_that(result.is_strict()).is_false()

    def test__get_structure__flies_tina_2__not_strict(self):
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
        d = Derivation([
            Rule.parse('flies(tina) -< chicken(tina), scared(tina).'),
            Rule.parse('chicken(tina).'),
            Rule.parse('scared(tina).'),
        ], i)
        expected = Structure({Rule.parse('flies(tina) -< chicken(tina), scared(tina).')}, Literal.parse('flies(tina)'),
                             d)
        result = d.get_structure()

        assert_that(result).is_equal_to(expected)
        assert_that(result.is_strict()).is_false()

    def test__is_subargument_of__min_max(self):
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
        d1 = Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)
        s1 = Structure(set(), Literal.parse('bird(tina)'), d1)
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = Structure({Rule.parse('flies(tina) -< bird(tina).')}, Literal.parse('flies(tina)'), d2)
        expected = True
        result = s1.is_subargument_of(s2)

        assert_that(result).is_equal_to(expected)

    def test__is_subargument_of__max_min(self):
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
        d1 = Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)
        s1 = Structure(set(), Literal.parse('bird(tina)'), d1)
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = Structure({Rule.parse('flies(tina) -< bird(tina).')}, Literal.parse('flies(tina)'), d2)
        expected = False
        result = s2.is_subargument_of(s1)

        assert_that(result).is_equal_to(expected)

    def test__is_subargument_of__max_max(self):
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
        d1 = Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)
        s1 = Structure(set(), Literal.parse('bird(tina)'), d1)
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = Structure({Rule.parse('flies(tina) -< bird(tina).')}, Literal.parse('flies(tina)'), d2)
        expected = True
        result = s2.is_subargument_of(s2)

        assert_that(result).is_equal_to(expected)

    def test__is_subargument_of__min_min(self):
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
        d1 = Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)
        s1 = Structure(set(), Literal.parse('bird(tina)'), d1)
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = Structure({Rule.parse('flies(tina) -< bird(tina).')}, Literal.parse('flies(tina)'), d2)
        expected = True
        result = s1.is_subargument_of(s1)

        assert_that(result).is_equal_to(expected)
