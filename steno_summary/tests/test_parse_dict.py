#!/usr/bin/env python3
import unittest
from pathlib import Path

import tempfile
from steno_summary import parse_dict as parse
from steno_summary.brief_info import Brief


class TestReadDict(unittest.TestCase):
    def compare_briefs(self, brief_test, brief_expected):
        """ Compare that the major keys of two briefs are the same.

        We might overload __eq__ in ``Brief`` in later releases to make this redundant,
        but for now this more stable.
        """

        self.assertEqual(brief_test.name, brief_expected.name)
        self.assertEqual(brief_test.keys, brief_expected.keys)

    def test_load_unsorted(self):
        """ Test the loading af a simple file from disk. """
        test_dir_path = Path(__file__).parent
        test_dict_path = test_dir_path / "data/test_dict.tsv"
        briefs_test = parse.read_dict(test_dict_path)

        names = ["Now", "Forget", "Ask"]
        keys = ["NOE", "FO-RGT", "SK"]
        briefs_actual = [Brief(n, k) for n, k in zip(names, keys)]
        briefs_actual.sort()

        self.assertEqual(len(briefs_test), len(briefs_test))
        [self.compare_briefs(t, a) for t, a in zip(briefs_test, briefs_actual)]

    def test_load_sorted(self):
        """ Test the loading af a simple file from disk. """
        test_dir_path = Path(__file__).parent
        test_dict_path = test_dir_path / "data/test_dict.tsv"
        briefs_test = parse.read_dict(test_dict_path)

        names = ["Ask", "Forget", "Now"]
        keys = ["SK", "FO-RGT", "NOE"]
        briefs_actual = [Brief(n, k) for n, k in zip(names, keys)]

        self.assertEqual(len(briefs_test), len(briefs_test))
        [self.compare_briefs(t, a) for t, a in zip(briefs_test, briefs_actual)]

    def test_parse_fail(self):
        """ Test that we catch lines with too many enteries. """
        with self.assertRaises(ValueError):
            parse._line_to_brief("Now\t")

    def test_parse_minimal(self):
        """ Parsing of lines with a name and a key. """
        line = "Now\tNOU"

        brief_test = parse._line_to_brief(line)
        brief_expected = Brief("Now", "NOU")

        self.compare_briefs(brief_test, brief_expected)

    def test_tags(self):
        """ Test the loading of tags from the file. """
        test_dir_path = Path(__file__).parent
        test_dict_path = test_dir_path / "data/test_dict_tags.tsv"
        briefs_test = parse.read_dict(test_dict_path)

        matching_names_test = [b.name for b in briefs_test if "single" in b.tags]
        matching_names_expected = ["Comp", "Rather", "Test"]

        self.assertEqual(matching_names_test, matching_names_expected)

        matching_names_test = [b.name for b in briefs_test if "alt" in b.tags]
        matching_names_expected = ["Test"]

        self.assertEqual(matching_names_test, matching_names_expected)


class TestWriteDict(unittest.TestCase):
    def test_add_conflict(self):
        """ Add an already existing entry to the brief list. """
        names = ["Now", "Forget", "Ask"]
        keys = ["NOE", "FO-RGT", "SK"]
        briefs_set = [Brief(n, k) for n, k in zip(names, keys)]

        new_brief = Brief("Now", "NOE")
        with self.assertRaises(ValueError):
            parse.add_to_dict(new_brief, briefs_set)

    def test_add_new(self):
        """ Add an already existing entry to the brief list. """
        names = ["Ask", "Forget", "Now"]
        keys = ["SK", "FO-RGT", "NOE"]
        briefs_set = [Brief(n, k) for n, k in zip(names, keys)]

        new_brief = Brief("Easy", "EZ")
        parse.add_to_dict(new_brief, briefs_set)

        names_expected = sorted(names + ["Easy"])
        names_test = [b.name for b in briefs_set]

        self.assertEqual(names_test, names_expected)


class TestSaveDict(unittest.TestCase):
    def test_save_dict(self):
        """ Save the brief list a temporary file. """
        names = ["Ask", "Forget", "Now"]
        keys = ["SK", "FO-RGT", "NOE"]
        briefs_set = [Brief(n, k) for n, k in zip(names, keys)]

        with tempfile.TemporaryDirectory() as dir_:
            dir_path = Path(dir_)
            dict_path = dir_path / "dict.tab"

            # Write the file to disk
            parse.save_dict_to_file(briefs_set, dict_path)

            # Read it again
            briefs_test = parse.read_dict(dict_path)

        names_test = [b.name for b in briefs_test]
        self.assertEqual(names_test, names)


if __name__ == "__main__":
    unittest.main()
