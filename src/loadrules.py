#!/usr/bin/env python3

import yaml
from nltk import Tree

from transductionrule import XTRule

def loadrules(fn):
    out = []
    loaded = None
    with open(fn) as infile: 
        loaded = yaml.load(infile)
    if not loaded: raise ValueError("couldn't load file: " + fn)

    for d in loaded:
        lhs = tree_or_string(d["lhs"])
        rhs = tree_or_string(d["rhs"])
        state = d["state"]
        
        if "weight" in d:
            weight = d["weight"]
        else:
            weight = 1.0

        if "newstates" in d:
            newstates = paths_as_dicts(d["newstates"])
        else:
            newstates = {}
        newrule = XTRule(state, lhs, rhs, newstates, weight)
        out.append(newrule)
    return out

def tree_or_string(s):
    """Given a string loaded from the yaml, produce either a Tree or a string,
    if it's just a terminal."""
    if s.startswith("("):
        return Tree(s)
    return s

def paths_as_dicts(fromyaml):
    """Given a list of lists of the shape [[path,state],...], produce a
    dictionary of the shape {path:state, ...}."""
    out = {}
    for (path, state) in fromyaml:
        out[tuple(path)] = state
    return out

def main():
    print(loadrules("figure5.yaml"))

if __name__ == "__main__": main()
