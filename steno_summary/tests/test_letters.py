#!/usr/bin/env python3
import unittest
import steno_summary.letters as l
from parameterized import parameterized


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


class TestSplitCapitalLetters(unittest.TestCase):
    """ Test breaking of a string of characters on captial letters. """

    @parameterized.expand(["ABEC", "A", "FZFQCUND"])
    def test_split_all_caps(self, test_str):
        """ In the case of all caps this is the same as a string iter. """
        split_expected = [i for i in test_str]
        split_test = l.split_on_capital(test_str)

        self.assertEqual(split_test, split_expected)

    @parameterized.expand(
        [
            ("ChSK", ["Ch", "S", "K"]),
            ("ShAttYP", ["Sh", "Att", "Y", "P"]),
            ("QFprHrmZ", ["Q", "Fpr", "Hrm", "Z"]),
        ]
    )
    def test_split_mixed_cap(self, test_string, split_expected):
        """ Test that we split mixed strings correctly. """
        split_test = l.split_on_capital(test_string)
        self.assertEqual(split_test, split_expected)

    def test_split_error(self):
        """ Raise an error if start with a lower case string. """
        with self.assertRaises(ValueError):
            l.split_on_capital("aFAst")

    @parameterized.expand(
        [
            ("Ch-SK", ["Ch", "-", "S", "K"]),
            ("ShAttY-P", ["Sh", "Att", "Y", "-", "P"]),
            ("QFprH-rmZ", ["Q", "Fpr", "H", "-rm", "Z"]),
        ]
    )
    def test_split_mixed_cap_dash(self, test_string, split_expected):
        """ Test that we split mixed strings with splits correctly. """
        split_test = l.split_on_capital(test_string)
        self.assertEqual(split_test, split_expected)

    @parameterized.expand(
        [
            ("Ch*SK", ["Ch", "*", "S", "K"]),
            ("ShAttY*P", ["Sh", "Att", "Y", "*", "P"]),
            ("QFprH*-rmZ", ["Q", "Fpr", "H", "*", "-rm", "Z"]),
        ]
    )
    def test_split_mixed_cap_dash(self, test_string, split_expected):
        """ Test that we split mixed strings with splits correctly. """
        split_test = l.split_on_capital(test_string)
        self.assertEqual(split_test, split_expected)
