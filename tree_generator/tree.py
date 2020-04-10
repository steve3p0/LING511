import os
from typing import Dict, Any, Union

from nltk.parse import stanford
import nltk
from nltk.draw.tree import TreeView
from PIL import Image

# taken from ohsu_tree
import logging
import sys
import re
#import os
from re import escape, finditer
import collections
from collections import defaultdict
import itertools
import operator

# Requirements:
# This script requires Ghostscript for image conversion
# You have to install the python package (via pip):
# $ pip3 install Ghostscript
# And you have to Download and install Ghostscript binaries for your OS:
# https://www.ghostscript.com/download/gsdnld.html
# Lastly, add ghostscript install directory bin folder to PATH environment variable
# On windows, for example, your ghostscript install directory bin folder might be:
#   C:\Program Files\gs\gs9.52
# Add that line to the path environment variable
# You may have to reboot for the path environment variable to take effect

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"

# left and delimiters on trees
LDEL = '('
RDEL = ')'
LDELE = escape(LDEL)
RDELE = escape(RDEL)
DELIMITERS = r'({})|({})'.format(LDELE, RDELE)

# labels are a sequence of non-whitespace, non-delimiter characters used
# both for terminals and non-terminals
LABEL = r'[^\s{}{}]+'.format(LDELE, RDELE)

# a "token" consists of:
# * a left delimiter
# * possibly some whitespace (though not usually)
# * one of:
#   - a label for a head (possibly null)
#   - a right delimiter
#   - a label for a terminal
TOKEN = r'({0})\s*({2})?|({1})|({2})'.format(LDELE, RDELE, LABEL)

# characters for naming heads introduced by tree transformation; should
# not overlap LDEL or RDEL if you are writing to text files
CU_JOIN_CHAR = '+'
MARKOVIZE_CHAR = '|'
CNF_JOIN_CHAR = '&'
CNF_LEFT_DELIMITER = '<'
CNF_RIGHT_DELIMITER = '>'

# mapping = {'NP-SBJ': 'NP', 'NP-TMP': 'NP'}

# MODAL_TAGS = ["VBD", "MD"]
MODAL_TAGS = ["V"]
TENSE_TAG = 'T'

# Reverse dictionary lookup
# keys = [key for key, value in dict_obj.items() if value == 'value']
tag_mapping: Dict[Union[str, Any], Union[str, Any]] = {
    # Sentence
    'S': 'TP',
    'SINV': 'TP',
    'SBAR': 'CP',
    # Determiners
    'DT': 'D',
    'CD': 'D',
    'PRP$': 'D',
    # Nouns
    'NN': 'N',
    'NNS': 'N',
    'PRP': 'N',
    # Verbs
    'VB': 'V',
    'VBN': 'V',
    'VBD': 'V',
    'VBG': 'V',
    # Adjectives
    'ADJP': 'AdjP',
    'JJ': 'Adj',  # Need to convert JJ to AdjP -> Adj
    # Conjuctions
    'CC': 'Conj',
    # Adverbs
    'ADVP': 'AdvP',
    'RB': 'Adv',
    'RBR': 'Adv',
    # Prepositions
    'IN': 'P',
    #'IN': 'C',  # sometimes IN is C (complement)?

    # Modal issues:
    # 1) IF MD IS tense, then it needs to be moved to and a transfer must occur
    #    look at #8 from 10TAD3
    'MD': 'V',


    # 2) JJ : AdjP -> Adj
    # 3) Complementizer Phrases
    #     a) # empty set C: ∅
    #        see #8 from 10TAD3
    #
    #


    # '': '',
    # '': '',
    # '': '',
    # '': '',
}


class Tree(object):

    # def __init__(self, parser=None):
    #     self.parser = parser

    def __init__(self, label=None, daughters=None, parser=None):
        self.label = label
        self.daughters = daughters if daughters else []
        self.parser = parser

    # def __repr__(self):
    #     return self.pretty()

    ############################################################################
    # magic methods for access, etc., all using self.daughters

    def __iter__(self):
        return iter(self.daughters)

    def __getitem__(self, i):
        return self.daughters[i]

    def __setitem__(self, i, value):
        self.daughters[i] = value

    def __len__(self):
        return len(self.daughters)


    def pretty(self, indent=0, step=4):
        """
        Serialize tree into human-readable multiline string

        >>> s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        >>> t = Tree.from_string(s)
        >>> t
        (TOP
            (S
                (VP
                    (TO to)
                    (VP
                        (VB play)
                    )
                )
            )
        )
        """
        string = LDEL + self.label
        i = indent + step
        is_tree = None
        for daughter in self:
            is_terminal = Tree.terminal(daughter)
            if is_terminal:
                string += ' ' + daughter
            else:
                # recursively print with increased indent
                string += '\n' + (' ' * i) + daughter.pretty(i)
        # add a newline and spaces after last non-terminal at this depth
        if not is_terminal:
            string += '\n' + (' ' * indent)
        string += RDEL
        return string


    @classmethod
    def from_string(cls, string):
        r"""
        Read a single Treebank-style tree from a string. Example:

        >>> s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> Tree.from_string(s)
        (ADVP
            (ADV widely)
            (CONJ and)
            (ADV friendly)
        )

        It doesn't break just because there are weird newlines, either:

        >>> str(Tree.from_string(s)) == \
        ... str(Tree.from_string(s.replace(' ', '\n')))
        True

        A few types of errors are known:

        >>> Tree.from_string(s[:-1])
        Traceback (most recent call last):
        ...
        ValueError: End-of-string, need /\)/
        >>> Tree.from_string(s[1:])
        Traceback (most recent call last):
        ...
        ValueError: Need /\(/
        >>> s_without_head = s[6:-1]
        >>> Tree.from_string(s_without_head)
        Traceback (most recent call last):
        ...
        ValueError: String contains 3 trees
        """
        # initialize stack to "empty"
        stack = [(None, [])]
        for m in finditer(TOKEN, string):
            token = m.group()
            if m.group(1):  # left delimiter
                stack.append((m.group(2), []))
            elif m.group(3):  # right delimiter
                # if stack is "empty", there is nothing in need of closure
                if len(stack) == 1:
                    raise ValueError('Need /{}/'.format(LDELE))
                (mother, children) = stack.pop()
                stack[-1][1].append(cls(mother, children))
            elif m.group(4):  # leaf
                stack[-1][1].append(m.group(4))
            else:
                raise ValueError('Parsing failure: {}'.format(m.groups()))
        # check to make sure the stack is "empty"
        if len(stack) > 1:
            raise ValueError('End-of-string, need /{}/'.format(RDELE))
        elif len(stack[0][1]) == 0:
            raise ValueError('End-of-string, need /{}/'.format(LDELE))
        elif len(stack[0][1]) > 1:
            raise ValueError('String contains {} trees'.format(
                len(stack[0][1])))
        return stack[0][1][0]

    @classmethod
    def from_stream(cls, handle):
        r"""
        Given a treebank-style data *.psd file, yield all its Trees, using
        `from_string` above

        Mock up a real file using cStringIO

        >>> from io import StringIO
        >>> s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> source = StringIO(s.replace(' ', '\n\n\n') + s)
        >>> (one, two) = Tree.from_stream(source)
        >>> str(one) == str(two)
        True
        """
        # TODO I am deeply unhappy with this solution. It would be nicer
        # to use the cleverer logic found in Tree.from_string instead.
        stack = 0
        start = 0
        string = handle.read()
        for m in finditer(DELIMITERS, string):
            # left bracket
            if m.group(1):
                stack += 1
            # right bracket
            else:
                stack -= 1
                # if brackets match, parse it
                if stack == 0:
                    end = m.end()
                    yield Tree.from_string(string[start:end])
                    start = end

    @staticmethod
    def tree_to_string(tree):
        s = str(tree)
        # pformat(self, margin=70, indent=0, nodesep="", parens="()", quotes=False)
        #s = tree.pformat()
        return s

    ############################################################################
    # static methods for traversal (etc.)

    @staticmethod
    def terminal(obj):
        return not hasattr(obj, 'label')

    @staticmethod
    def preterminal(obj):
        for child in obj:
            return not hasattr(child, 'label')

        return False

    @staticmethod
    def unary(obj):
        return len(obj) == 1

    def binary(obj):
        return len(obj) == 2

    @staticmethod
    def ternary(obj):
        return len(obj) == 3

    @staticmethod
    def several(obj):
        # 3 or more
        return len(obj) > 2

    @staticmethod
    def get_label(obj):
        terminal = Tree.terminal(obj)
        if terminal:
            return obj
        return obj.label

    @staticmethod
    def unary_daughter_is_terminal(mother):
        if not Tree.unary(mother):
            return False

        if not Tree.terminal(mother.daughters[0]):
            return False

        return True

    @staticmethod
    def binary_daughters_are_nonterminal(mother):
        if not Tree.binary(mother):
            return False

        if Tree.terminal(mother.daughters[0]) or Tree.terminal(mother.daughters[0]):
            return False

        return True


    ############################################################################################
    ############################################################################################
    ## New Code

    @staticmethod
    def write_to_file(tree, filename):
        if os.path.exists(f"{filename}.png"):
            os.remove(f"{filename}.png")

        import tempfile
        with tempfile.NamedTemporaryFile() as file:
            in_path = "{0:}.ps".format(file.name)
            TreeView(tree)._cframe.print_to_file(in_path)
            with Image.open(in_path) as img:
                img.load(scale=4)
                img.save(f"{filename}.png")

    def convert_tree_labels(self, tree, mapping):
        # '''
        # >>> convert_tree_labels(Tree('S', [Tree('NP-SBJ', [('foo', 'NN')])]), {'NP-SBJ': 'NP'})
        # Tree('S', [Tree('NP', [('foo', 'NN')])])
        # '''
        children = []

        for t in tree:
            if isinstance(t, nltk.tree.Tree):
                children.append(self.convert_tree_labels(t, mapping))
            else:
                children.append(t)

        label = mapping.get(tree.label(), tree.label())
        return nltk.tree.Tree(label, children)

    def promote_tense(self, t):
        try:
            t.label()
        except AttributeError:
            #print(t)
            return

        if t.label() in MODAL_TAGS:
            current = t
            parent = current.parent()
            right_sibling = getattr(current.right_sibling(), 'label', lambda: None)()

            if right_sibling in MODAL_TAGS:
                tense_node = nltk.tree.ParentedTree.fromstring(f"({TENSE_TAG} {t[0]})")
                parent.remove(current)
                grandpa = parent.parent()
                grandpa.insert(len(grandpa) - 1, tense_node)

        for child in t:
            self.promote_tense(child)

    def promote_modals_to_tense(self, t):
        # VBN - Verb, past participle
        # VBP - Verb, non-3rd person singular present
        # VBZ
        ptree = nltk.tree.ParentedTree.convert(t)
        self.promote_tense(ptree)
        new_tree_str = str(ptree)
        new_tree = nltk.tree.Tree.fromstring(new_tree_str)
        return new_tree

    def collapse_duplicate_nodes(self, t, label):
        try:
            t.label()
        except AttributeError:
            print(t)
            return

        if t.label() == label:
            current = t
            parent = current.parent()
            if parent.label() == label and current.right_sibling() is None:
                current = t
                parent = current.parent()

                child_count = len(parent)

                # You have to refresh grandparent after parent did a pop
                grandpa = parent.parent()

                if len(parent) > 2:
                    for i in (0, len(parent) - 2):

                        # Save left sibling of the current node before we pop it!
                        # We will make it the left child of the current node
                        # p_left_child = current.left_sibling()
                        # p_left_child = nltk.tree.ParentedTree.convert(p_left_child)
                        oldest = parent[0]
                        oldest = nltk.tree.ParentedTree.convert(oldest)

                        # We are going to pop the left sibling move it down to the left most
                        #parent.pop(0)
                        #parent.pop(i)
                        parent.remove(oldest)
                        parent = nltk.tree.ParentedTree.convert(parent)

                        # Now insert the popped off left_child into the left-most child spot of current node
                        #current.insert(0, p_left_child)
                        #current.insert(i, oldest)
                        length = len(current) - 2
                        current.insert(length, oldest)
                        current = nltk.tree.ParentedTree.convert(current)
                else:
                    # Save left sibling of the current node before we pop it!
                    # We will make it the left child of the current node
                    p_left_child = current.left_sibling()

                    # We are going to pop the left sibling move it down to the left most
                    parent.pop(0)

                    # You have to refresh grandparent after parent did a pop
                    grandpa = parent.parent()

                    # Now insert the popped off left_child into the left-most child spot of current node
                    current.insert(0, p_left_child)

                # Now Pop off the right most child of grandpa (which is the current node)
                grandpa.pop(len(grandpa) - 1)

                # Now promote up the duplicate child (current) to the right most child of the grandparent
                # You have to covert to do this again to kill current's parents?  Makes no sense!!!
                current = nltk.tree.ParentedTree.convert(current)
                grandpa.insert(len(grandpa), current)

                # test t back to current before continuing to traverse.
                t = current

        for child in t:
            self.collapse_duplicate_nodes(child, label)

    def expand_phrase_nodes(self, t, preterminal_tags):
        try:
            t.label()
        except AttributeError:
            return

        # NOTE: To access the left-child node    (object) of a tree node:  t[0]
        # NOTE: To access the left-child label    (str)   of a tree node:  t[0].label()
        # NOTE: To access the left-child terminal (str)   of a tree node:  t[0][0]
        # NOTE: To whoever designed nltk.tree: That's fucked

        if t.label() in preterminal_tags:
            current = t
            parent = current.parent()

            phrase_label = f"{t.label()}P"
            if parent.label() != phrase_label:
                parent_index = current.parent_index()
                new_child = nltk.tree.ParentedTree.convert(current)

                new_parent = nltk.tree.ParentedTree(phrase_label, [new_child])
                parent.remove(current)
                parent.insert(parent_index, new_parent)

                # test t back to current before continuing to traverse.
                t = new_child

            # If parent is a Phrase of the same tag type, but is not preterminal (it has more than 1 child nodes)....
            # Replace the current node with a preterminal phrase and move the current node as it's only child
            elif parent.label() == phrase_label and len(parent) > 1:
                parent_index = current.parent_index()
                new_child = nltk.tree.ParentedTree.convert(current)

                new_parent = nltk.tree.ParentedTree(phrase_label, [new_child])
                parent.remove(current)
                parent.insert(parent_index, new_parent)

                # test t back to current before continuing to traverse.
                t = new_child

        for child in t:
            self.expand_phrase_nodes(child, preterminal_tags)

    def expand_phrase(self, t):
        # Search for preterminals with child_label that are not a child of a phrase (phrase_label)
        # Insert a phrase node above the child
        preterminal_tags = ["Adv", "Adj"]
        #preterminal_tags = ["Adj"]

        # Need to convert a ntlk.tree.Tree to a ParentedTree
        # in order to access parent nodes collapsing
        ptree = nltk.tree.ParentedTree.convert(t)

        # Collapse ParentedTree ptree (by referece)
        self.expand_phrase_nodes(ptree, preterminal_tags)

        # Convert ParentedTree ptree back into a nltk.tree.Tree
        # before returning it
        new_tree = nltk.tree.Tree.convert(ptree)
        return new_tree

    def collapse_duplicate(self, t):
        # We are just going to collapse duplicate VP nodes for now
        tags = "VP"

        # Need to convert a ntlk.tree.Tree to a ParentedTree
        # in order to access parent nodes collapsing
        ptree = nltk.tree.ParentedTree.convert(t)

        # Collapse ParentedTree ptree (by referece)
        self.collapse_duplicate_nodes(ptree, tags)

        # Convert ParentedTree ptree back into a nltk.tree.Tree
        # before returning it
        new_tree = nltk.tree.Tree.convert(ptree)
        return new_tree

    def add_complement(self, t):
        try:
            t.label()
        except AttributeError:
            return

        # NOTE: To access the left-child node    (object) of a tree node:  t[0]
        # NOTE: To access the left-child label    (str)   of a tree node:  t[0].label()
        # NOTE: To access the left-child terminal (str)   of a tree node:  t[0][0]

        # NOTE: To whoever designed nltk.tree: That's fucked

        if t.label() == 'CP':
            current = t

            # If there is only one child node of a Complement Clause (CP),
            # Then it is missing it's complement, therefore, INSERT AN EMPTY SET CLAUSE
            if len(current) == 1:
                # (C Ø)  <- The empty set
                empty_set_node = nltk.tree.Tree.fromstring("(C Ø)")
                current.insert(0, empty_set_node)

            # Else, if there is more than one child node,
            # Then check it is not complement, replace it's label with C
            # NOTE: This is because you failed to set it correctly when you shift a verb tense tense
            # object, because that object was tagged as a preposition (P)
            elif t[0].label != 'C':
                complement_node = nltk.tree.Tree.fromstring(f"(C {t[0][0]})")
                t.remove(t[0])
                t.insert(0, complement_node)

        for child in t:
            self.add_complement(child)

    def parse_sentence(self, sentence):
        tree = next(self.parser.raw_parse(sentence))

        print(f"STANFORD PRETTY: ********************************")
        nltk.Tree.pretty_print(tree)

        tree = self.collapse_duplicate(tree)
        tree = self.convert_tree_labels(tree, tag_mapping)

        ###############
        # self.write_to_file(tree, "XXXXXX")
        ###############

        tree = nltk.ParentedTree.convert(tree)
        self.promote_tense(tree)
        tree = nltk.Tree.convert(tree)

        tree = self.expand_phrase(tree)
        self.add_complement(tree)

        return tree[0]

    def parse_sentences(self, sentences):
        i = 0
        for s in sentences:
            i += 1
            filename = f"tree_{i}"
            tree = self.parse_sentence(s)
            tree_str = self.tree_to_string(tree)
            print(f"{i}. {s}\n{tree_str}\n")
            self.write_to_file(tree, filename)


if __name__ == '__main__':
    # sentences = ["He thought that other places must be more interesting"]

    sentences = [
                    "The animals did not think the buffalo would eat them",
                    "They were afraid the buffalo would trample them",
                    "The buffalo were pursuing fresh grass",
                    "Those buffalo were large and lumbering",
                    "The herd that the animals had heard caused considerable alarm",
                    "One young buffalo trotted slowly behind the herd",
                    "He was smelling the fresh grass",
                    "This buffalo was wondering whether he would find any adventures",
                    "He was tired of the dry grassy plains",
                    "He thought that other places must be more interesting"
                ]

    parser = stanford.StanfordParser(model_path=model_path)
    tree_builder = Tree(parser)
    tree_builder.parse_sentences(sentences)

