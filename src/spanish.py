#!/usr/bin/env python3

from nltk import Tree

from loadrules import loadrules
from translate import translate

import debugutil
debugutil.DEBUGGING = False

def main():
    rules = loadrules("spanish.yaml")

    trees = []
    ## I like Mary / María me gusta a mi
    trees.append( Tree("(S (NP (PRP I)) (VP (VB like) (NP (NNP Mary))))"))

    ## John usually goes home / Juan suele ir a casa
    trees.append(Tree(
"""
(S (NP (NNP John))
   (VP (RB usually)
       (VP (VBZ goes) (RB home))))
"""))

    ## John entered the house / Juan entró en la casa
    trees.append( Tree(
"""
(S (NP (NNP John))
   (VP (VBD entered) (NP (DT the) (NN house))))
"""))

    ## John broke into the room / Juan forzó la entrada al cuarto.
    trees.append(Tree(
"""
(S (NP (NNP John))
   (VP (VBD broke)
       (PP (IN into)
           (NP (DT the) (NN room)))))"""
    ))

    ## I stabbed John / Yo le di puñaladas a Juan
    trees.append( Tree("(S (NP (PRP I)) (VP (VBD stabbed) (NP (NNP John))))"))

    for tree in trees: 
        translate(tree, rules)

if __name__ == "__main__": main()
