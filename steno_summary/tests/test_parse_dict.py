#!/usr/bin/env python3
import unittest
from pathlib import Path
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

    def test_load(self):
        """ Test the loading af a simple file from disk. """
        test_dir_path = Path(__file__).parent
        test_dict_path = test_dir_path / "data/test_dict.tsv"
        briefs_test = parse.read_dict(test_dict_path)

        names = ["Now", "Forget", "Ask"]
        keys = ["NOE", "FO-RGT", "SK"]
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


if __name__ == "__main__":
    unittest.main()
