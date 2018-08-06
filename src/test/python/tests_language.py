from unittest import TestCase

from assertpy import assert_that

from defeasible.domain.definitions import Literal, Program, RuleType
from defeasible.domain.memory import Memory


class TestLanguage(TestCase):
    def test__derive__0(self):
        memory = Memory(Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """))

        assert_that(memory.get_derivation(Literal.parse('e'))) \
            .contains_only({Literal.parse('e')})

    def test__derive__1(self):
        memory = Memory(Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """))

        assert_that(memory.get_derivation(Literal.parse('d'))) \
            .contains_only({Literal.parse('h'), Literal.parse('d')})

    def test__derive__2(self):
        memory = Memory(Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """))

        assert_that(memory.get_derivation(Literal.parse('c'))) \
            .contains_only({Literal.parse('f'), Literal.parse('g'), Literal.parse('c')})

    def test__derive__3(self):
        memory = Memory(Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """))

        assert_that(memory.get_derivation(Literal.parse('b'))) \
            .contains_only({Literal.parse('f'), Literal.parse('g'), Literal.parse('c'), Literal.parse('b')},
                           {Literal.parse('h'), Literal.parse('d'), Literal.parse('e'), Literal.parse('b')})

    def test__derive__4(self):
        memory = Memory(Program.parse("""
            a <- b, c. 
            b <- d, e. 
            b <- c. 
            c <- f, g. 
            d <- h. 
            e. 
            f. 
            g. 
            h.
        """))

        assert_that(memory.get_derivation(Literal.parse('a'))) \
            .contains_only(
            {Literal.parse('f'), Literal.parse('g'), Literal.parse('c'), Literal.parse('b'),
             Literal.parse('a')},
            {Literal.parse('h'), Literal.parse('d'), Literal.parse('f'), Literal.parse('e'),
             Literal.parse('g'), Literal.parse('b'), Literal.parse('c'), Literal.parse('a')})

    def test__derive__bird_tina__defeasibly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('bird(tina)'), RuleType.DEFEASIBLE)) \
            .contains_only([Literal.parse('chicken(tina)'), Literal.parse('bird(tina)')])

    def test__derive__bird_tina__strictly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('bird(tina)'), RuleType.STRICT)) \
            .contains_only([Literal.parse('chicken(tina)'), Literal.parse('bird(tina)')])

    def test__derive__flies_tina__defeasibly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('flies(tina)'), RuleType.DEFEASIBLE)) \
            .contains_only(
            [Literal.parse('chicken(tina)'), Literal.parse('bird(tina)'), Literal.parse('flies(tina)')],
            [Literal.parse('chicken(tina)'), Literal.parse('scared(tina)'), Literal.parse('flies(tina)')])

    def test__derive__flies_tina__strictly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('flies(tina)'), RuleType.STRICT)).is_none()

    def test__derive__not_bird_tina__defeasibly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('~bird(tina)'), RuleType.DEFEASIBLE)).is_none()

    def test__derive__not_bird_tina__strictly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('~bird(tina)'), RuleType.STRICT)).is_none()

    def test__derive__not_flies_tina__defeasibly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('~flies(tina)'), RuleType.DEFEASIBLE)) \
            .contains_only([Literal.parse('chicken(tina)'), Literal.parse('~flies(tina)')])

    def test__derive__not_flies_tina__strictly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.get_derivation(Literal.parse('~flies(tina)'), RuleType.STRICT)).is_none()

    def test__is_contradictory__defeasibly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.is_contradictory(RuleType.DEFEASIBLE)).is_true()

    def test__is_contradictory__strictly(self):
        program = Program.parse("""
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
        memory = Memory(program)

        assert_that(memory.is_contradictory(RuleType.STRICT)).is_false()
