from unittest import TestCase

from assertpy import assert_that

from depysible.domain.definitions import Program
from depysible.domain.definitions import Rule
from depysible.domain.interpretation import Derivation
from depysible.domain.interpretation import Interpreter


class TestComparing(TestCase):
    def test__is_strictly_more_specific__0(self):
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
        d1 = Derivation([Rule.parse('~flies(tina) -< chicken(tina).'), Rule.parse('chicken(tina).')], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('flies(tina) -< bird(tina).'),
            Rule.parse('bird(tina) <- chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        result = s1.is_strictly_more_specific_than(s2)

        assert_that(result).is_true()

    def test__is_strictly_more_specific__1(self):
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
        result = s2.is_strictly_more_specific_than(s1)

        assert_that(result).is_false()

    def test__is_strictly_more_specific__2(self):
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
            Rule.parse('flies(tina) -< chicken(tina), scared(tina).'),
            Rule.parse('chicken(tina).'),
            Rule.parse('scared(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        result = s2.is_strictly_more_specific_than(s1)

        assert_that(result).is_false()

    def test__is_strictly_more_specific__3(self):
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
            Rule.parse('flies(tina) -< chicken(tina), scared(tina).'),
            Rule.parse('chicken(tina).'),
            Rule.parse('scared(tina).'),
        ], i)
        s1 = d1.get_structure()
        d2 = Derivation([
            Rule.parse('~flies(tina) -< chicken(tina).'),
            Rule.parse('chicken(tina).'),
        ], i)
        s2 = d2.get_structure()
        result = s1.is_strictly_more_specific_than(s2)

        assert_that(result).is_true()
