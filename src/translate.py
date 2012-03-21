#!/usr/bin/env python3

from operator import itemgetter

from transduce import transduce

def translate(tr, rules):
    intext = " ".join(tr.leaves())
    print("** Translating:", intext)

    theresults = transduce(tr, rules, "q")
    output_triples = set()

    if not theresults:
        print("  FAILED TO TRANSLATE O NOES.")

    for result in theresults:
        treestr = result.tree.pprint(margin=1000)
        outtext = " ".join(result.tree.leaves())
        w = result.weight
        output_triples.add((treestr,outtext,w))

    inorder = sorted(list(output_triples), key=itemgetter(2))
    for treestr,outtext,w in inorder:
        print("  text:", outtext)
        print("  tree:", treestr)
        print("  weight:", w)
