#!/usr/bin/env python3

from copy import deepcopy
from operator import itemgetter

from debugutil import dprint

class XTRule:
    """One rule in a tree transducer. It has a left-hand side (a pattern) and a
    right-hand side. Later it will also have a weight."""

    def __init__(self, state, lhs, rhs, newstates, weight):
        self.lhs = lhs
        self.rhs = rhs
        self.state = state
        self.newstates = newstates
        self.weight = weight

    def matches(self, tree, statemap):
        """Returns the count of this rule's LHS matches in the given tree.
        Accounts for pattern matching too."""
        count = 0
        my_vars = variables_to_paths(self.lhs)
        ## Check whether, once you replace the right parts of the given tree
        ## with variables, it's equal to this rule's LHS.
        dprint("matching this lhs:", self.lhs)
        for path, state in statemap.items():
            indexed = tree_index(tree, path)
            subtree = deepcopy(indexed)
            dprint("subtree:", subtree)
            try:
                for (var,varpath) in my_vars:
                    if varpath is ():
                        subtree = var
                        break
                    subtree[varpath] = var
            except:
                # print("EXCEPTION:", path)
                # tree is wrong shape, keep tranglin'.
                continue
            if self.state == state and subtree == self.lhs:
                # print("FOUND A MATCH.")
                count += 1
        return count

    def apply(self, tree, statemap):
        """Returns a list of (new tree, new statemap) by applying this rule in
        all the places where it works."""
        # print("APPLYING", self.lhs, "to", tree, statemap)
        out = []
        my_vars = variables_to_paths(self.lhs)
        for path, state in statemap.items():
            indexed = tree_index(tree, path)
            subtree = deepcopy(indexed)
            try:
                for (var,vp) in my_vars:
                    if vp is ():
                        subtree = var
                        break
                    subtree[vp] = var
            except:
                continue

            if self.state == state and subtree == self.lhs:
                newtree = deepcopy(tree)
                newsubtree = replace(indexed, self.lhs, self.rhs)
                newstates_with_prepend = {
                   tuple(list(path) + list(rulepath)) : state
                   for (rulepath, state) in self.newstates.items()
                }
                newstates_with_prepend.update(statemap)
                del newstates_with_prepend[path]

                if path == ():
                    out.append((newsubtree, newstates_with_prepend))
                else:
                    newtree[path] = newsubtree
                    out.append((newtree, newstates_with_prepend))
        # print("PRODUCED:", out)
        return out
    
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return (("<rule.\n  state: {0}\n  lhs: {1}\n  rhs: {2}\n" +
                 "  newstates: {3}>").format(
            self.state, self.lhs, self.rhs, self.newstates))

def tree_index(tr, path):
    if type(tr) == str and path != ():
        raise(ValueError, "can't index into a string with a non-empty path")
    if type(tr) == str:
        return tr
    else:
        return tr[path]

def get_top(tr):
    """Given a thing that might be a tree or maybe a terminal string, return
    the 'top' of it -- either the node of a tree, or just the string itself."""
    return (tr if type(tr) == str else tr.node)

def replace(concrete, lhs, rhs, failok=False):
    """Given a concrete tree (ie, maybe a subtree of a larger tree) and lhs and
    rhs patterns, produce the new tree resulting from substituting the things
    in concrete in the positions determined by lhs into the rhs pattern."""
    out = deepcopy(rhs)
    vps_rhs = variables_to_paths(rhs)
    vps_lhs = variables_to_paths(lhs)

    for (rhs_var, rhs_path) in vps_rhs:
        if rhs_var in [var for (var,path) in vps_lhs]:
            var_path_for_lhs = [path for var,path in vps_lhs
                                     if var == rhs_var][0]
            if var_path_for_lhs is ():
                if rhs_path is ():
                    out = deepcopy(concrete)
                else:
                    out[rhs_path] = deepcopy(concrete)
            else:
                out[rhs_path] = deepcopy(concrete[var_path_for_lhs])
        else:
            if failok:
                return None
            else:
                raise ValueError(
                "LHS {0} missing expected variable {1}.".format(lhs, rhs_var))
    return out

def variables_to_paths(tr):
    """Given a tree, return a list of (var,path) tuples -- not a dictionary
    because a variable may occur more than once."""
    out = []
    if type(tr) == str:
        if tr.startswith("?"):
            out.append((tr,()))
    else:
        candidates = [(get_top(tr[path]), path) for path in tr.treepositions()]
        for name,path in candidates:
            if name.startswith("?"):
                out.append((name, path))
    return out
