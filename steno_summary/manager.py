#!/usr/bin/env python3
import backtrace
from steno_summary.parse_dict import read_dict
from steno_summary.brief_info import brief_grid, Brief
import steno_summary.parse_dict as pd
from typing import Optional
import argh

""" Manager for the steno summary dictonary. """

backtrace.hook(align=True, strip_path=True)


@argh.aliases("cont")
def contains(string: Optional[str] = None, block: bool = False):
    """ Print the names that contains the string. """
    string = _query_user_if_none(string, "Search for words containing: ")
    briefs = read_dict()
    filtered_briefs = [b for b in briefs if string.lower() in b.name.lower()]
    print(brief_grid(filtered_briefs))
    _wait_if(block)


@argh.aliases("start")
def starting_with(string: Optional[str] = None, block: bool = False):
    """ Print the names that starts with the string. """
    string = _query_user_if_none(string, "Words starting with: ")
    briefs = read_dict()
    lower_str = string.lower()
    filtered_briefs = [b for b in briefs if b.name.lower().startswith(lower_str)]
    print(brief_grid(filtered_briefs))
    _wait_if(block)


@argh.aliases("tag")
def matches_tag(tag: str, block: bool = False):
    """ Print the names of the strokes that contain the tags. """
    briefs = read_dict()
    filtered_briefs = [b for b in briefs if tag in b.tags]
    print(brief_grid(filtered_briefs))
    _wait_if(block)


@argh.arg("-t", "--tags", nargs="+")
def add(name: str = None, keys: str = None, tags: Optional[str] = None):
    """ Add a new entry to the dict. """
    name = _query_user_if_none(name, "Brief name: ")
    keys = _query_user_if_none(keys, "Brief keys: ")
    print(keys)
    brief = Brief(name, keys, tags=tags)

    briefs = read_dict()
    briefs.sort()
    pd.add_to_dict(brief, briefs)

    pd.save_dict_to_file(briefs)


def _query_user_if_none(string: Optional[str], message=str) -> str:
    """ Return the value or ask the user for a value if not provided. """
    return string if string else input(message)


def _wait_if(block: Optional[bool] = False):
    """ Optionally wait for user input. Useful if we create a terminal. """
    if not block:
        return

    try:
        user_val = input("Search again or quit? [.sctq] ")
    except KeyboardInterrupt:
        return
    if user_val.startswith("s") or user_val.startswith("."):
        args = user_val.split(maxsplit=1)[1:]
        starting_with(*args, block=True)
    elif user_val.startswith("c"):
        args = user_val.split(maxsplit=1)[1:]
        contains(*args, block=True)
    elif user_val.startswith("t"):
        args = user_val.split(maxsplit=1)[1:]
        matches_tag(*args, block=True)


if __name__ == "__main__":
    argh.dispatch_commands([contains, starting_with, matches_tag, add])
