import unittest

import transduce
import transductionrule
import loadrules

from nltk import Tree

class TestTransduce(unittest.TestCase):
    def setUp(self):
        self.rules = loadrules.loadrules("testrules.yaml")

    def test_onesymbol(self):
        results = transduce.transduce("F", self.rules, "q")
        trees = [ss.tree for ss in results]
        self.assertIn("V", trees)
        self.assertIn("W", trees)
        self.assertEqual(2, len(results))

    def test_no_transduction(self):
        tree = Tree("(foo bar)")
        results = transduce.transduce(tree, self.rules, "q")
        self.assertListEqual([], results)

    def test_one_result(self):
        tree = Tree("(A foo bar)")
        results = transduce.transduce(tree, self.rules, "q")
        trees = [ss.tree for ss in results]

        self.assertEqual(results[0].weight, 1.0)
        self.assertListEqual([Tree("(A (R bar foo) (S X))")], trees)

    def test_figure_five(self):
        tree = Tree("(A (B D E) (C F G))")
        rules = loadrules.loadrules("figure5.yaml")
        results = transduce.transduce(tree, rules, "q")
        trees = [ss.tree for ss in results]

        ss1 = transduce.SearchState(Tree("(A (R (T V W) U) (S X))"), {}, 0.27)
        ss2 = transduce.SearchState(Tree("(A (R (T V W) U) (S X))"), {}, 
                                          (1.0 * 0.4 * 1.0 * 0.1 * 0.5))

        self.assertIn(ss1, results)
        self.assertIn(ss2, results)

    def test_nested(self):
        tree = Tree("(S Abe (VP kicked the-ball))")
        results = transduce.transduce(tree, self.rules, "q")
        trees = [ss.tree for ss in results]

        ss1 = transduce.SearchState(Tree("(S kicked Abe the-ball)"), {}, 1)
        ss2 = transduce.SearchState(Tree("(kicked kicked kicked kicked)"),
                                    {}, 0.5)
        # print(ss1)
        # print(ss2)
        self.assertIn(ss1, results)
        self.assertNotIn(ss2, results)

class TestTheUtils(unittest.TestCase):
    def test_variables_to_paths(self):
        tr = Tree("(foo (bar (baz ?x0)))")
        
        tuples = transductionrule.variables_to_paths(tr)
        self.assertEqual([("?x0", (0,0,0))], tuples)

        tuples = transductionrule.variables_to_paths("?x5")
        self.assertEqual([("?x5", ())], tuples)

        tuples = transductionrule.variables_to_paths(Tree("(foo (bar))"))
        self.assertEqual([], tuples)
