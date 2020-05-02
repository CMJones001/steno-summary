#!/usr/bin/env python3
from steno_summary.parse_dict import read_dict
import argh

""" Manager for the steno summary dictonary. """


@argh.aliases("cont")
def contains(string: str):
    """ Print the names that contains the string. """
    briefs = read_dict()

    filtered_briefs = [
        b.print_block() for b in briefs if string.lower() in b.name.lower()
    ]


@argh.aliases("start")
def starting_with(string: str):
    """ Print the names that starts with the string. """
    briefs = read_dict()

    filtered_briefs = [
        b.print_block() for b in briefs if b.name.lower().startswith(string)
    ]


@argh.aliases("tag")
def matches_tag(tag: str):
    """ Print the names of the strokes that contain the tags. """
    briefs = read_dict()

    filtered_briefs = [b.print_block() for b in briefs if tag in b.tags]


if __name__ == "__main__":
    argh.dispatch_commands([contains, starting_with, matches_tag])
