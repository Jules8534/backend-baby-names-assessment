#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import argparse

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""
__author__ = "Chris, Koren, Sean, and Demo"

def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single list starting
    with the year string followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    
    year = r'Popularity\sin\s(\d\d\d\d)'
    names = []
    
    with open(filename) as f:
        text = f.read()

    year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
    if not year_match:
        sys.stderr.write('Couldn\'t find the year!\n')
        sys.exit(1)
    year = year_match.group(1)
    names.append(year)

    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', text)

    names_to_rank = {}
    for rank_tuple in tuples:
        (rank, boyname, girlname) = rank_tuple
        if boyname not in names_to_rank:
            names_to_rank[boyname] = rank
        if girlname not in names_to_rank:
            names_to_rank[girlname] = rank
    
    sorted_names = sorted(names_to_rank.keys())

    for name in sorted_names:
        names.append(name + " " + names_to_rank[name])


    return names


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""
    parser = argparse.ArgumentParser(description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more filenames.
    # It will also expand wildcards just like the shell, e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):    
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files


    create_summary = ns.summaryfile

    # For each filename, call `extract_names` with that single file.
    # Format the resulting list a vertical list (separated by newline \n)
    # Use the create_summary flag to decide whether to print the list,
    # or to write the list to a summary file e.g. `baby1990.html.summary`

    for filename in file_list:
        print("working on file: {}".format(filename))
        names = extract_names(filename)
        text = '\n'.join(names)
        if create_summary:
            with open(filename + '.summary', 'w') as outf:
                outf.write(text + '\n')
        else:
            print(text)

if __name__ == '__main__':
    main(sys.argv[1:])
