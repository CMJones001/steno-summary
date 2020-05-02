#!/usr/bin/env python
from typing import Optional, Iterable, Dict
from pathlib import Path
from steno_summary.brief_info import Brief

""" Read and write to the user dictionary.

For now we store this as a TSV file as both semicolons and commas are used elsewhere. Of
course, we could use pandas to parse the tsv, but for now we keep the data stored in the
classes rather than a dataframe. Hypothetically, this may lead to slower performance but
I cannot see this becoming a noticable problem for now.

"""


def read_dict(dict_location: Optional[Path] = None) -> Iterable[Brief]:
    """ Read the dictionary from file. """
    dict_path = _validate_path(dict_location)

    with open(dict_path, "r") as f:
        # Skip the header
        briefs = [_line_to_brief(l) for l in f.readlines()[1:] if not l.startswith("#")]

    # Remove the None lines from comments
    return briefs


def _line_to_brief(line: str) -> Optional[Brief]:
    """ Convert a line of text into a Brief.

    This involves validating the inputs and splitting them where needed.
    """
    # Ignore comment lines
    if line.startswith("#"):
        return
    # Remove new lines or hanging tabs
    chunks = line.strip("\n\r\t").split("\t")
    n_chunks = len(chunks)

    if n_chunks > 4:
        raise ValueError(f"Too many entries in line [{n_chunks}>4] {line}.")
    if n_chunks < 2:
        raise ValueError(f"Too few entries in line [{n_chunks}<2] {line}.")

    # TODO: Add more complex parsing of dict chunks
    b = Brief(name=chunks[0], keys=chunks[1])
    return b


def _validate_path(dict_location: Optional[Path]) -> Path:
    """ Validate the given path  and return a default if none is provided. """
    if dict_location is None:
        source_dir = Path(__file__).parent
        dict_location = source_dir / "user_dict.tsv"

    if not dict_location.is_file():
        raise FileNotFoundError(f"Given user dict {dict_location} does not exist.")
    return dict_location


if __name__ == "__main__":
    briefs = read_dict()
    briefs.sort(key=lambda k: len(k.name))
    # [print(b) for b in briefs if "you" in b.name.lower()]
    [print(b) for b in briefs]
