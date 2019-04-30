#!/usr/bin/python

"""
expand_aliases.py

Recursively expand out all aliases in specified file.  Only expands local 
definitions - it does no remote magic with SMTP VRFY because that would be 
bonkers.

James B 2018-02-12
"""

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("aliases", help="aliases file")
parser.add_argument("-c", "--count", help="show counts", action="store_true")
args = parser.parse_args()

# Read aliases flat file into dict
aliases = {}
with open(args.aliases, 'r') as aliases_file:
    for line in aliases_file:
        # If not comment or blank line
        if not (re.search('^\s*#', line) or re.search('^\s*$', line)):
            search = re.search('^([^:]+):\s+(.*)', line.rstrip())
            if not search:
                sys.stderr.write("SEARCH DID NOT MATCH (line=%s)\n" % line)
            else:
                # left is alias name (left hand side of :)
                left = search.group(1).lower()
                # right is one or more comma separated alias
                # members (right hand side of :)
                right = search.group(2)
                if left in aliases:
                    sys.stderr.write("DUPLICATE ALIAS (line=%s)\n" % line)
                else:
                    members = right.split(",")
                    aliases[left] = set([m.strip() for m in members])

# Recursively resolve alias into its members.  Does case-insensitive search.
def resolve_alias(alias_name, aliases):
    members = aliases[alias_name]
    leaves = set([])
    for member in members:
        m = member.lower()
        if m in aliases:
            leaves.update(resolve_alias(m, aliases))
        else:
            leaves.add(member)
    return leaves

# Use resolve_aliases() to stitch together a complete aliases list down to leaves
resolved_aliases = {}
for alias_name in aliases.keys():
    members = resolve_alias(alias_name, aliases)
    resolved_aliases[alias_name] = members

for alias, members in resolved_aliases.items():
    if args.count:
        print("%d %s: %s" % (len(members), alias, ','.join(members)))
    else:
        print("%s: %s" % (alias, ','.join(members)))
    for m in members:
        if not (re.search('^[^@]+@[a-zA-Z0-9.-]+$', m) or re.search('^/', m)):
            sys.stderr.write("WEIRD - no @ in alias '%s' member '%s'\n" % (alias, m))

