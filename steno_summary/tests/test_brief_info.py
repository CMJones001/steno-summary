#!/usr/bin/env python3
import unittest
import steno_summary.brief_info as b
import steno_summary.letters as l

left_set = {l for l in "STKPWHRAO"}
right_set = {l for l in "EUFRPBLGTSDZ"}


class TestBrief(unittest.TestCase):
    """ Manual parsing of provided strings. """

    def validate_missing(self, word: b.Brief, left_keys: set, right_keys: set):
        """ Test for the recorded and missing letters on the left/right side. """

        remaining_left_expeceted = left_set - left_keys
        remaining_left_actual = word.remaining_left
        self.assertEqual(remaining_left_expeceted, remaining_left_actual)

        left_letter_expected = left_keys
        left_letter_actual = word.left_letters
        self.assertEqual(left_letter_expected, left_letter_actual)

        remaining_right_expeceted = right_set - right_keys
        remaining_right_actual = word.remaining_right
        self.assertEqual(remaining_right_expeceted, remaining_right_actual)

        right_letter_expected = right_keys
        right_letter_actual = word.right_letters
        self.assertEqual(right_letter_expected, right_letter_actual)

    def test_valid_left(self):
        word = b.Brief(name="", keys="")
        word.left_letters = {"T", "K"}

        remaining_letters_expected = left_set - {"T", "K"}
        remaining_letters_test = word.remaining_left

        self.assertEqual(remaining_letters_expected, remaining_letters_test)

    def test_add_left_letter(self):
        """" Add a key to the array """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.n)

        remaining_letters_expeceted = left_set - {"T", "H", "P"}
        remaining_letters_actual = word.remaining_left

        self.assertEqual(remaining_letters_expeceted, remaining_letters_actual)

    def test_add_left_letter_mult(self):
        """" Add multiple keys to the array """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.f)
        word._parse_key_stroke(l.v)
        word._parse_key_stroke(l.o)

        left_keys = {l for l in "TPSRO"}
        self.validate_missing(word, left_keys, set())

    def test_add_right_letter(self):
        """" Add a single right hand letter """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.e)
        self.validate_missing(word, set(), {"E"})

    def test_add_right_mult(self):
        """" Add a right hand letter followed by an ambigious letter"""
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.e)
        word._parse_key_stroke(l.s)

        self.validate_missing(word, set(), {l for l in "ES"})

    def test_add_right_left(self):
        """" We should get an error on trying left key after right. """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.e)
        word._parse_key_stroke(l.n)
        with self.assertRaises(ValueError):
            word._parse_key_stroke(l.o)

    def test_parse_dash(self):
        """ Providing a dash should starting parsing on the right side. """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke("-")
        word._parse_key_stroke(l.s)

        self.validate_missing(word, set(), {"S"})

    def test_parse_double(self):
        """ Parse the left and right stroke of a letter """
        word = b.Brief(name="", keys="")
        word._parse_key_stroke(l.n)
        word._parse_key_stroke(l.n)

        self.validate_missing(word, {l for l in "TPH"}, {l for l in "PB"})


class TestWordParsing(unittest.TestCase):
    """ Parsing of strings handed directly to the Brief """

    def validate_missing(self, word: b.Brief, left_keys: set, right_keys: set):
        """ Test for the recorded and missing letters on the left/right side. """
        # Left side unchanged
        remaining_left_expeceted = left_set - left_keys
        remaining_left_actual = word.remaining_left
        self.assertEqual(remaining_left_expeceted, remaining_left_actual)

        left_letter_expected = left_keys
        left_letter_actual = word.left_letters
        self.assertEqual(left_letter_expected, left_letter_actual)

        # Right side missing the letter
        remaining_right_expeceted = right_set - right_keys
        remaining_right_actual = word.remaining_right
        self.assertEqual(remaining_right_expeceted, remaining_right_actual)

        right_letter_expected = right_keys
        right_letter_actual = word.right_letters
        self.assertEqual(right_letter_expected, right_letter_actual)

    def test_double_stoke(self):
        """ Test parsing of left and right stroke. """
        word = b.Brief(name="", keys="nn")
        left = {l for l in "TPH"}
        right = {l for l in "PB"}

        self.validate_missing(word, left, right)

    def test_right_dash_stoke(self):
        """ Test parsing right with dash stroke. """
        word = b.Brief(name="", keys="-s")
        left = set()
        right = {l for l in "S"}

        self.validate_missing(word, left, right)

    def test_left_stoke(self):
        """ Test parsing right with dash stroke. """
        word = b.Brief(name="", keys="s")
        left = {l for l in "S"}
        right = set()

        self.validate_missing(word, left, right)

    def test_complex_stoke(self):
        """ Test a mixture of both. """
        word = b.Brief(name="", keys="nvoens")
        left = {l for l in "TPHSRO"}
        right = {l for l in "EPBS"}

        self.validate_missing(word, left, right)
