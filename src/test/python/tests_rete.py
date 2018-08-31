from unittest import TestCase

from assertpy import assert_that

from depysible.domain.definitions import Atom


class TestAtomUnification(TestCase):
    def test_unifies_0(self):
        pattern = Atom('x', [])
        ground = Atom('x', [])
        assert_that(pattern.unifies(ground)).is_empty()

    def test_unifies_1(self):
        pattern = Atom('x', [])
        ground = Atom('y', [])
        assert_that(pattern.unifies(ground)).is_none()

    def test_unifies_2(self):
        pattern = Atom('x', [5])
        ground = Atom('x', [5])
        assert_that(pattern.unifies(ground)).is_empty()

    def test_unifies_3(self):
        pattern = Atom('x', ['b'])
        ground = Atom('y', [5])
        assert_that(pattern.unifies(ground)).is_none()

    def test_unifies_4(self):
        pattern = Atom('x', ['X'])
        ground = Atom('x', [5])
        assert_that(pattern.unifies(ground)).contains_only('X').contains_entry({'X': 5})

    def test_unifies_5(self):
        pattern = Atom('x', ['X', 'X'])
        ground = Atom('y', [5, 7])
        assert_that(pattern.unifies(ground)).is_none()

    def test_unifies_6(self):
        pattern = Atom('x', ['X', 'Y'])
        ground = Atom('x', [5, 'b'])
        assert_that(pattern.unifies(ground)).contains_only('X', 'Y').contains_entry({'X': 5}, {'Y': 'b'})
