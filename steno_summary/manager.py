#!/usr/bin/env python3
import backtrace
from steno_summary.parse_dict import read_dict
from steno_summary.brief_info import brief_grid
import argh

""" Manager for the steno summary dictonary. """

backtrace.hook(align=True, strip_path=True)


@argh.aliases("cont")
def contains(string: str):
    """ Print the names that contains the string. """
    briefs = read_dict()
    filtered_briefs = [b for b in briefs if string.lower() in b.name.lower()]
    print(brief_grid(filtered_briefs))


@argh.aliases("start")
def starting_with(string: str):
    """ Print the names that starts with the string. """
    briefs = read_dict()
    lower_str = string.lower()
    filtered_briefs = [b for b in briefs if b.name.lower().startswith(lower_str)]
    print(brief_grid(filtered_briefs))


@argh.aliases("tag")
def matches_tag(tag: str):
    """ Print the names of the strokes that contain the tags. """
    briefs = read_dict()
    filtered_briefs = [b for b in briefs if tag in b.tags]
    print(brief_grid(filtered_briefs))


if __name__ == "__main__":
    argh.dispatch_commands([contains, starting_with, matches_tag])
