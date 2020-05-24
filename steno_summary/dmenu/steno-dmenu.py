#!/usr/bin/env python3
from steno_summary import manager
from enum import Enum
from pathlib import Path
from subprocess import PIPE, run, Popen
from time import sleep
import steno_summary
import i3ipc
import sys

""" Use dmenu to lookup a brief using rofi/dmenu. """

# ["echo", "awk", "-F'\t '$4 { print $4 }'", user_dict], shell=True, stdout=PIPE,


def read_tags(user_dict: Path):
    """ Get the tags from the file. """

    # Grab a set of unique tags from the dict
    tags = run(["awk", "-F	", "$4 && NR>1 { print $4 }", user_dict], stdout=PIPE)
    tags = set(_decode_stdout(tags).split("\n"))

    # dmenu requires a new line seperated string
    tag_string = "\n".join(tags)
    selection = run(["dmenu"], input=tag_string.encode("utf8"), stdout=PIPE)
    return _decode_stdout(selection)


def _decode_stdout(selection) -> str:
    """ Return the stdout as a string. """
    return selection.stdout.decode("utf8").strip("\r\n")


def launch_term(*lookup_args):
    """ Create the lookup terminal. """
    interactive_term = sys.stdout.isatty()
    manager_path = Path(manager.__file__)
    run_command = manager_path

    if interactive_term:
        run([run_command, *lookup_args])
    else:
        lookup_flat = " ".join(lookup_args)
        run(["guake", "--show", "-e", f"steno-manager {lookup_flat} -b"])


def main():
    """ Get users to choose a mode and use this to launch the lookup. """
    Option = Enum("Option", "start cont tag add")

    # Dmenu requires options separated by \n
    opts = "\n".join([name for name, member in Option.__members__.items()])

    # Get the values from dmenu
    ps = Popen(["echo", opts], stdout=PIPE)
    selection = run(["dmenu"], stdin=ps.stdout, stdout=PIPE)
    # Fail silently if dmenu fails
    if selection.returncode == 0:
        selection = Option[_decode_stdout(selection)]
    else:
        return

    interactive_term = sys.stdout.isatty()
    print(f"interactive_term = {interactive_term}")
    dict_path = Path(steno_summary.__file__).parent / "user_dict.tsv"

    if selection is Option.start:
        launch_term("starting-with")
    elif selection is Option.cont:
        launch_term("contains")
    elif selection is Option.tag:
        # Read tag from dmenu
        tag = read_tags(dict_path)
        launch_term("tag", tag)
    elif selection is Option.add:
        launch_term("add")
    else:
        raise ValueError("Unrecognised choice from dmenu.")


if __name__ == "__main__":
    main()
