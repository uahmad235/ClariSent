from anytree import RenderTree, LevelOrderIter, NodeMixin

from src.Utility_Functions import *



class SentimentTreesManager(object):
    """ manages all the trees operations for class """

    def search_in_descendants(self,trees, new_term):
        """ searches for new sub-term in roots of all trees """
        for tree in trees:
            # if tree.name in new_term: # if tree contains
            if UtilityFunctions.first_in_second(tree.name, new_term):
                return tree

    def insert_descendant(self,found_tree, new_term, value):
        """ adds the term to tree as descendant on specified position """

        if UtilityFunctions.first_in_second(found_tree.name, new_term):
            # if children exist match term to childs data
            if found_tree.children:
                for child in found_tree.children:  # iterate all childs

                     # child contains new_term
                    if UtilityFunctions.first_in_second(child.name, new_term):
                        self.insert_descendant(child, new_term, value)  # insert in child next time
                        break  # don't iterate for next child if it's found in some child already

                else:  # if new_term's data doesn't contain in any child (loop doesn't break )
                    MyNode(new_term, value=value, parent=found_tree)

            else:  # no children
                MyNode(new_term, value=value, parent=found_tree)

    def make_trees(self, sentiment_terms):
        """ returns list of "dictionary of trees" """
        all_trees = []
        for i, term in enumerate(sentiment_terms):
            # if it is a single-word term add as root into tree-list
            if len(term[0].split(' ')) == 1:
                all_trees.append(MyNode(name=term[0], value=term[1]))
            else:
                found_tree = self.search_in_descendants(all_trees, term[0])

                if found_tree:
                    # leaf_nodes = get_leaf_nodes_of_tree(found_tree)
                    self.insert_descendant(found_tree, term[0], term[1])

                else:  # no single-term root found for new_term
                    # add multi-word phrase directly as root
                    all_trees.append(MyNode(name=term[0], value=term[1]))

        self.all_trees =  all_trees
        return self.all_trees

    @staticmethod
    def has_unchecked_descendants(tree):
        """ returns a boolean than a tree has unchecked descendant or not"""
        for node in LevelOrderIter(tree):
            if not node.checked:  # if any node is not checked i.e., node.checked = False
                return True

        return False

    @staticmethod
    def get_unchecked_ultimate_descendants(tree):
        """ return final unchecked descendant """

        return reversed([x for x in LevelOrderIter(tree) if not x.checked])  # 133

    @staticmethod
    def set_all_ancestors_checked(node):

        """ sets all ancestors of a specific node checked"""
        while (node):
            node.checked = True
            node = node.parent


    def reset_all_trees(self, all_trees = None):
        """ reset the checked attribute of all the trees as FLase"""

        if not all_trees:
            all_trees = self.all_trees
            for i, t in enumerate(all_trees[:]):

                for pre, _, node in RenderTree(t):
                    node.checked = False
    @staticmethod
    def print_tree(tree):
        """ prints a single passed tree """
        for pre, _, node in RenderTree(tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(30), node.value, node.checked)


class MyNode(NodeMixin):
    """ contains enhanced attributes for a Sentiment-Phrase (Node)"""

    def __init__(self, name, parent=None, value=None, checked=False):
        super(MyNode, self).__init__()

        # attributes inherited
        self.name = name
        self.parent = parent

        # attributes modified
        self.value = value
        self.checked = checked