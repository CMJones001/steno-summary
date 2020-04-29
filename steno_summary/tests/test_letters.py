#!/usr/bin/env python3
import unittest
import steno_summary.letters as l


class TestAddLetter(unittest.TestCase):
    def test_add_letter_left_error(self):
        """ Attempt to add a letter that does not belong to either side. """
        with self.assertRaises(ValueError):
            l.Letter("q")

    def test_add_letter_left_valid(self):
        """ Add a valid letter to the left hand side. """
        letter_actual = set(["S"])
        letter_test = l.Letter("s").left

    def test_add_letter_left_multi_valid(self):
        """ Add multiple letters as a string. """
        letter_actual = set(["S", "T", "R"])
        letter_test = l.Letter("str").left
        self.assertEqual(letter_actual, letter_test)

    def test_add_letter_left_multi_error(self):
        """ Attempt to add a multiple letter but with an error. """
        with self.assertRaises(ValueError):
            l.Letter("STRQ")

    def test_add_letter_right_error(self):
        """ Attempt to add a letter that does not belong to either side. """
        with self.assertRaises(ValueError):
            l.Letter(right="k")

    def test_add_letter_right_valid(self):
        """ Add a letter that on the right hand side. """
        letter_actual = set(["U"])
        letter_test = l.Letter(right="u").right
        self.assertEqual(letter_actual, letter_test)

    def test_add_letter_right_multi_valid(self):
        """ Add multiple letters as a string. """
        letter_actual = set(["B", "T", "D"])
        letter_test = l.Letter(right="BTD").right
        self.assertEqual(letter_actual, letter_test)

    def test_add_letter_right_multi_error(self):
        """ Attempt to add a multiple letter but with an error. """
        with self.assertRaises(ValueError):
            l.Letter(right="TDQ")
