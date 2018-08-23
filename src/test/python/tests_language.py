from unittest import TestCase

from assertpy import assert_that

from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Program
from defeasible.domain.definitions import Rule
from defeasible.domain.definitions import RuleType
from defeasible.domain.interpretation import Derivation
from defeasible.domain.interpretation import Interpreter


class TestLanguage(TestCase):

    def test__get_derivations__0(self):
        p = Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """)
        i = Interpreter(p)
        expected = {Derivation([Rule.parse('e.')], i)}
        result = i.get_derivations(Literal.parse('e'))

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__1(self):
        p = Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """)
        i = Interpreter(p)
        expected = {Derivation([Rule.parse('d <- h.'), Rule.parse('h.')], i)}
        result = i.get_derivations(Literal.parse('d'))

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__2(self):
        p = Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """)
        i = Interpreter(p)
        expected = {Derivation([Rule.parse('c <- f, g.'), Rule.parse('f.'), Rule.parse('g.')], i)}
        result = i.get_derivations(Literal.parse('c'))

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__3(self):
        p = Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """)
        i = Interpreter(p)
        expected = {
            Derivation([Rule.parse('b <- c.'), Rule.parse('c <- f, g.'), Rule.parse('f.'), Rule.parse('g.')], i),
            Derivation([Rule.parse('b <- d, e.'), Rule.parse('d <- h.'), Rule.parse('h.'), Rule.parse('e.')], i),
        }
        result = i.get_derivations(Literal.parse('b'))

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__4(self):
        p = Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """)
        i = Interpreter(p)
        expected = {
            Derivation([
                Rule.parse('a <- b, c.'),
                Rule.parse('b <- c.'),
                Rule.parse('c <- f, g.'),
                Rule.parse('f.'),
                Rule.parse('g.'),
            ], i),
            Derivation([
                Rule.parse('a <- b, c.'),
                Rule.parse('b <- d, e.'),
                Rule.parse('d <- h.'),
                Rule.parse('h.'),
                Rule.parse('e.'),
                Rule.parse('c <- f, g.'),
                Rule.parse('f.'),
                Rule.parse('g.'),
            ], i),
        }
        result = i.get_derivations(Literal.parse('a'))

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__bird_tina__defeasibly(self):
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
        expected = {Derivation([Rule.parse('bird(tina) <- chicken(tina).'), Rule.parse('chicken(tina).')], i)}
        result = i.get_derivations(Literal.parse('bird(tina)'), RuleType.DEFEASIBLE)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__bird_tina__strictly(self):
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
        expected = {Derivation([Rule.parse('bird(tina) <- chicken(tina)..'), Rule.parse('chicken(tina).')], i)}
        result = i.get_derivations(Literal.parse('bird(tina)'), RuleType.STRICT)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__flies_tina__defeasibly(self):
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
        expected = {
            Derivation([Rule.parse('flies(tina) -< chicken(tina), scared(tina).'), Rule.parse('chicken(tina).'),
                        Rule.parse('scared(tina).')], i),
            Derivation([Rule.parse('flies(tina) -< bird(tina).'), Rule.parse('bird(tina) <- chicken(tina).'),
                        Rule.parse('chicken(tina).')], i),
        }
        result = i.get_derivations(Literal.parse('flies(tina)'), RuleType.DEFEASIBLE)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__flies_tina__strictly(self):
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
        expected = set()
        result = i.get_derivations(Literal.parse('flies(tina)'), RuleType.STRICT)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__not_bird_tina__defeasibly(self):
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
        expected = set()
        result = i.get_derivations(Literal.parse('~bird(tina)'), RuleType.DEFEASIBLE)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__not_bird_tina__strictly(self):
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
        expected = set()
        result = i.get_derivations(Literal.parse('~bird(tina)'), RuleType.STRICT)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__not_flies_tina__defeasibly(self):
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
        expected = {Derivation([Rule.parse('~flies(tina) -< chicken(tina).'), Rule.parse('chicken(tina).')], i)}
        result = i.get_derivations(Literal.parse('~flies(tina)'), RuleType.DEFEASIBLE)

        assert_that(result).is_equal_to(expected)

    def test__get_derivations__not_flies_tina__strictly(self):
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
        expected = set()
        result = i.get_derivations(Literal.parse('~flies(tina)'), RuleType.STRICT)

        assert_that(result).is_equal_to(expected)

    def test__is_contradictory__defeasibly(self):
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
        expected = True
        result = bool(i.is_contradictory(RuleType.DEFEASIBLE))

        assert_that(result).is_equal_to(expected)

    def test__is_contradictory__strictly(self):
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
        expected = False
        result = bool(i.is_contradictory(RuleType.STRICT))

        assert_that(result).is_equal_to(expected)
