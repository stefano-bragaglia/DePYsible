from unittest import TestCase

from assertpy import assert_that

from defeasible.domain.definitions import Literal, Program, disagree


class TestRebuttals(TestCase):
    def test__disagreement__0(self):
        a = Literal.parse('a')
        b = Literal.parse('b')
        program = Program.parse('~h <- b. h <- a.')

        assert_that(disagree(a, b, program.get_strict())).is_true()


