#!/usr/bin/env python3

from nltk import Tree

from loadrules import loadrules
from translate import translate

import debugutil
debugutil.DEBUGGING = False

def main():
    rules = loadrules("pokemon.yaml")
    trees = []
    trees.append(Tree("(S let me show you my Pokémon)"))
    trees.append(Tree("(S let me show you my cats)"))

    for tree in trees: 
        translate(tree, rules)

if __name__ == "__main__": main()
