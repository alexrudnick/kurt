#!/usr/bin/env python3

from nltk import Tree

from loadrules import loadrules
from translate import translate

import debugutil
debugutil.DEBUGGING = False

def main():
    rules = loadrules("german.yaml")
    trees = []

    ## I like eating / Ich esse gern
    trees.append(Tree("(S (NP (PRP I)) (VP (VB like) (VBG eating)))"))

    ## I am hungry / Ich habe Hunger
    trees.append(Tree("(S (NP (PRP I)) (VP (VB am) (JJ hungry)))"))

    for tree in trees: 
        translate(tree, rules)

if __name__ == "__main__": main()
