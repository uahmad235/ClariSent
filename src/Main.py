# setting python working environment

from anytree import RenderTree, NodeMixin, PostOrderIter, PreOrderIter, LevelOrderIter
import re
from Data_Layer import DataLayer
from Utility_Functions import *


#  "not working->childOf->None" and "not working well->childOf->well" anomaly
# if we keep the sort order in alphabetic manner, we can keep this anomaly controlled
# let's see how:
# if alphabetically sorted, "not working well" will be somewhere next to "not working" and so "not working" will become
# parent and "not working well" will become it's child.


class MyNode(NodeMixin):
    """ contains enhanced attributes for a Sentiment-Phrase (Node)"""

    def __init__(self, name, parent=None, value=None, checked=False):
        super(MyNode, self).__init__()

        # attributes default
        self.name = name
        self.parent = parent

        # attributes modified
        self.value = value
        self.checked = checked


def print_tree(tree):
    for pre, _, node in RenderTree(tree):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(30), node.value, node.checked)


def first_in_second(first, second):
    """ returns true if the first expression is contained in second """

    compiled_regex = re.compile(r"\b(%s)\b" % (first), re.IGNORECASE)
    objects = re.search(compiled_regex, second)

    if objects:
        return True

    return False


def regex_demo():
    text = """this  is a cat. this is very very good cat. i like it very much
                This is a brown dog. thisse ! Is it compatible?\n
                Very Good"""
    word_separator = re.compile(r"\b(very good)\b", re.IGNORECASE)
    m = re.findall(word_separator, text)
    if m:
        print(m)
        # print(m.group(1))
    else:
        print("None")


def search_in_descendants(trees, new_term):
    """ searches for new sub-term in roots of all trees """
    for tree in trees:
        # if tree.name in new_term: # if tree contains
        if first_in_second(tree.name, new_term):
            return tree


def insert_descendant(found_tree, new_term, value):
    """ adds the term to tree as descendant on specified position """

    # if found_tree.name in new_term:
    if first_in_second(found_tree.name, new_term):
        #     if children exist match term to childs data
        if found_tree.children:
            for child in found_tree.children:  # iterate all childs

                # if child.name in new_term:  # child contains new_term
                if first_in_second(child.name, new_term):
                    insert_descendant(child, new_term, value)  # insert in child next time
                    break  # don't iterate for next childs if it's found in some child already

            else:  # if new_term's data doesn't contain in any child (loop doesn't break )
                MyNode(new_term, value=value, parent=found_tree)

        else:  # no children
            MyNode(new_term, value=value, parent=found_tree)


def make_trees(sentiment_terms):
    """ returns list of "dictionary of trees" """
    all_trees = []
    for i, term in enumerate(sentiment_terms):
        # if it is a single-word term add as root into tree-list
        if len(term[0].split(' ')) == 1:
            all_trees.append(MyNode(name=term[0], value=term[1]))
        else:
            found_tree = search_in_descendants(all_trees, term[0])

            if found_tree:
                # leaf_nodes = get_leaf_nodes_of_tree(found_tree)
                insert_descendant(found_tree, term[0], term[1])

            else:  # no single-term root found for new_term
                # add multi-word phrase directly as root
                all_trees.append(MyNode(name=term[0], value=term[1]))

    return all_trees


def has_unchecked_descendants(tree):
    """ returns a boolean than a tree has unchecked descendant or not"""

    for node in LevelOrderIter(tree):
        if not node.checked:  # if any node is not checked i.e., node.checked = False
            return True

    return False


def get_unchecked_ultimate_descendants(tree):
    """ return final unchecked descendant """

    return reversed([x for x in LevelOrderIter(tree) if not x.checked ])  # 133


def set_all_ancestors_checked(node):

    while (node):

        node.checked = True
        node = node.parent



def main():
    """ entry point of the programme """
    sentiment_terms = DataLayer().read_sentiment_terms(path="../data/phone_st_fake.txt")
    all_trees = make_trees(sentiment_terms)

    terms_counter = 0
    # for i,t in enumerate(all_trees[:]):
    #     # print_tree(t)
    #     for pre, _, node in RenderTree(t):
    #         treestr = u"%s%s%d" % (pre, node.name, i)
    #         print(treestr.ljust(30), node.value, node.checked)
    #         terms_counter += 1
    #     print('*'*40)

    utils = UtilityFunctions()

    del sentiment_terms
    review_1 = """Their staff are rude and they are not very careful with their items however this item arrived in very good condition so I won't grumble at the fact the delivery man was grumpy\
    and barely helped me get it into my doorway."""
    review_2 = """Very fast delivery! This bed is amazing pure comfort. Extremely good price. Although there is a slight smell of plastic, nothing strong!"""

    tokenized_text = utils.split_string_with_multiple_tokenizers(review_1)
    tokenized_text = map(lambda x: x.strip(), tokenized_text)


    # print(list(tokenized_text))
    # utils.score_individual_piece_of_text(text=tokenized_text, sentiment_trees=all_trees)

    # for x in LevelOrderIter(all_trees[104]): #133
    #     # if x.is_leaf:
    #     # x.checked = True
    #     print(x.name, x.is_leaf)
    # print('*'*40)

    # for x in reversed(list(LevelOrderIter(all_trees[104]))): #133
    #     print(x.name, x.is_leaf)

    # for node in LevelOrderIter(all_trees[104]):
    #     print(node.name)
    # print('*'*50)

    # print("unchecked_descendant:", has_unchecked_descendants(all_trees[104]))

    # reversed_descendants = get_unchecked_ultimate_descendants(all_trees[104])



    # from copy import copy, deepcopy
    # pass the copy of "list of all_trees" which doesn't affect actual data
    # utils.score_individual_piece_of_text(tokenized_text, deepcopy(all_trees[:]))

    utils.score_individual_piece_of_text(tokenized_text, all_trees[:])



    for i, t in enumerate(all_trees):
        # print_tree(t)
        for pre, _, node in RenderTree(t):
            treestr = u"%s%s%d" % (pre, node.name, i)
            print(treestr.ljust(30), node.value, node.checked)
        print('*' * 40)


if __name__ == "__main__":
    main()
