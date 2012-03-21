#!/usr/bin/env python3

from functools import lru_cache

from nltk import Tree
from nltk import ImmutableTree

from loadrules import loadrules


## a wRTG has these parts.
## Sigma: alphabet
## N: set of nonterminals
## S: initial nonterminal
## P: set of weighted productions


## in the output...
# R: ... what is R?
# N: nonterminals?
# S: initial nonterminal
# P: set of weighted productions

def immutable(tr):
    """Given a Tree, make it an ImmutableTree."""
    str = tr.pprint(margin=10000)
    return ImmutableTree(str)

def deriv(rules, initial, intree, outtree):
    """
    Based on Algorithm 1 in "Training Tree Transducers". Takes a list of rules,
    a start state, an observed input tree and an observed output tree. Returns
    the derivation wRTG that describes all of the weighted derivation trees
    that could have produced the output tree.
    """

    return None

@lru_cache(maxsize=None)
def produce(intree, outtree, rules, q, i, o):
    """
    ... understand this soon!
    """
    
    ## do the pattern match...
    for rule in rules: # ...
        pass

    return False

def main():
    intree = ImmutableTree("(foo bar)")
    outtree = ImmutableTree("(bar foo)")

    mutable = Tree("(foo bar)")
    imm = immutable(mutable)
    print(imm)

    rules = loadrules("testrules.yaml")
    setofrules = set()
    for rule in rules:
        setofrules.add(rule)
    print(setofrules)
    setofrules = frozenset(setofrules)

    ## XXX(alexr): do we need to make rules be sets?
    ## ah geez. let's just use frozenrules.
    print(produce(intree, outtree, setofrules, "q0", (0), (1)))

if __name__ == "__main__": main()
