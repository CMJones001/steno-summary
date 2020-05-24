#!/usr/bin/env python3
import unittest
import steno_summary.brief_info as b
import steno_summary.letters as l
from parameterized import parameterized

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

    def validate_missing(
        self, word: b.Brief, left_keys: set, right_keys: set, starred=False
    ):
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

        self.assertEqual(starred, word.starred, msg=f"{word} failed")

    def test_double_stoke(self):
        """ Test parsing of left and right stroke. """
        word = b.Brief(name="", keys="NN")
        left = {l for l in "TPH"}
        right = {l for l in "PB"}

        self.validate_missing(word, left, right)

    def test_right_dash_stoke(self):
        """ Test parsing right with dash stroke. """
        word = b.Brief(name="", keys="-S")
        left = set()
        right = {l for l in "S"}

        self.validate_missing(word, left, right)

    def test_left_stoke(self):
        """ Test parsing right with dash stroke. """
        word = b.Brief(name="", keys="S")
        left = {l for l in "S"}
        right = set()

        self.validate_missing(word, left, right)

    def test_complex_stoke(self):
        """ Test a mixture of both. """
        word = b.Brief(name="", keys="NVOENS")
        left = {l for l in "TPHSRO"}
        right = {l for l in "EPBS"}

        self.validate_missing(word, left, right)

    def test_add_starred_letter_right(self):
        """ Handle right hand letters with a star. """
        word = b.Brief(name="V", keys="-V")
        left = set()
        right = set("F")

        self.validate_missing(word, left, right, starred=True)

    def test_add_starred_letter_left(self):
        """ Handle left hand letters with a star. """
        word = b.Brief(name="Z", keys="Z")
        left = set("S")
        right = set()
        self.validate_missing(word, left, right, starred=True)

    def test_add_starred_letter_both(self):
        """ Handle right hand letters with a star. """
        word = b.Brief(name="ZV", keys="Z-V")
        left = set("S")
        right = set("F")

        self.validate_missing(word, left, right, starred=True)

    def test_daul_letter(self):
        """ Handle two letter strokes.  """
        word = b.Brief(name="Ch", keys="Ch")
        left = {l for l in "KH"}
        right = set()

        self.validate_missing(word, left, right, starred=False)

    def test_daul_letter_left_right(self):
        """ Handle two letter strokes with extra keys. """
        word = b.Brief(name="ChCh", keys="ChCh")
        left = {l for l in "KH"}
        right = {l for l in "FP"}

        self.validate_missing(word, left, right, starred=False)

    def test_daul_letter_left_twice(self):
        """ Handle two letter strokes with extra keys. """
        word = b.Brief(name="ChB", keys="ChB")
        left = {l for l in "KHPW"}
        right = set()

        self.validate_missing(word, left, right, starred=False)

    def test_daul_letter_star(self):
        """ Handle two letter strokes with extra keys. """
        word = b.Brief(name="Th", keys="ITh")
        left = set()
        right = {l for l in "EUT"}

        self.validate_missing(word, left, right, starred=True)

    @parameterized.expand(
        [
            ("-Th", "", "T", True),
            ("Ng", "", "PBG", False),
            ("Nk", "", "PBG", True),
            ("Mp", "", "PL", True),
            ("OMp", "O", "PL", True),
            ("SChAIChTh", "SKHA", "EUFPT", True),
        ]
    )
    def test_clusers(self, keys, left, right, starred):
        """ Handle two letter strokes with mixtures of dashes and stars keys. """
        word = b.Brief(name="Th", keys=keys)

        left = {l for l in left} if left else set()
        right = {l for l in right} if right else set()

        self.validate_missing(word, left, right, starred=starred)


class TestVowelStroke(unittest.TestCase):
    def validate_missing(
        self, word: b.Brief, left_keys: set, right_keys: set, starred=False
    ):
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

        self.assertEqual(starred, word.starred, msg=f"{word} failed")

    def test_vowel_simple(self):
        """ Adding a simple stroke that requires both sides of the keyboard. """
        word = b.Brief("Vowel", "Aw")

        left = {"A"}
        right = {"U"}
        self.validate_missing(word, left, right)

    def test_vowel_complex(self):
        """ Adding a vowel stroke along with other chars. """
        word = b.Brief("Vowel", "NAwCh")

        left = {l for l in "TPHA"}
        right = {l for l in "UFP"}
        self.validate_missing(word, left, right)

    def test_breaking_sting(self):
        """ Raise an appropriate error if things are out of order. """
        with self.assertRaises(ValueError):
            word = b.Brief("Vowel", "-FAw")


class TestGrid(unittest.TestCase):
    @unittest.skip
    def test_splitting(self):
        names = ["Think", "Now", "Function"]
        strokes = ["ThI", "NOE", "FUKS"]
        briefs = [b.Brief(name, stroke) for name, stroke in zip(names, strokes)]

        b.brief_grid(briefs)

    @unittest.skip
    def test_splitting_multiline(self):
        names = ["Think", "Now", "Function", "Yours", "Have", "Do"]
        strokes = ["ThI", "NOE", "FUKS", "URS", "V", "DO"]
        briefs = [b.Brief(name, stroke) for name, stroke in zip(names, strokes)]

        b.brief_grid(briefs)

        self.assertTrue(False)


class TestBriefMultiple(unittest.TestCase):
    """ Parsing of multi-stroke briefs. """

    def validate_missing(
        self, word: b.Brief, left_keys: set, right_keys: set, starred=False
    ):
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

        self.assertEqual(starred, word.starred, msg=f"{word} failed")

    def test_double_simple(self):
        """ Test the keys in a simple double brief. """
        word = b.Brief(name="Double", keys="T/-S")
        left = {l for l in "T"}
        right = set()

        self.validate_missing(word, left, right)

        child = word.next_
        self.validate_missing(child, set(), {l for l in "S"})

    def test_double_complex(self):
        """ Test the keys in a complex double brief. """
        word = b.Brief(name="Double", keys="L-Th/-G")

        left = {l for l in "HR"}
        right = {l for l in "T"}

        self.validate_missing(word, left, right, starred=True)

        child = word.next_
        self.validate_missing(child, set(), {"G"})

    def test_triple_stroke(self):
        """ Test the keys in a complex triple stroke. """
        word = b.Brief(name="Double", keys="L-Th/-G/KWRO-NG")
        self.validate_missing(word, {l for l in "HR"}, {"T"}, starred=True)

        word = word.next_
        self.validate_missing(word, set(), {"G"}, starred=False)

        word = word.next_
        self.validate_missing(
            word, {l for l in "KWRO"}, {l for l in "PBG"}, starred=False
        )

    def test_single_len(self):
        """ Get the number of keys in single stroke. """
        word = b.Brief(name="Single", keys="-G")
        n_strokes_test = len(word)
        n_strokes_expected = 1

        self.assertEqual(n_strokes_test, n_strokes_expected)

    def test_double_len(self):
        """ Get the number of keys in double stroke. """
        word = b.Brief(name="Double", keys="L-Th/-G")
        n_strokes_test = len(word)
        n_strokes_expected = 2

        self.assertEqual(n_strokes_test, n_strokes_expected)

    def test_triple_len(self):
        """ Get the number of keys in a triple stroke. """
        word = b.Brief(name="Double", keys="L-Th/-G/KWRO-NG")
        n_strokes_test = len(word)
        n_strokes_expected = 3

        self.assertEqual(n_strokes_test, n_strokes_expected)
