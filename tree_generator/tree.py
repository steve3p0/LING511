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

MODAL_TAGS = ["VBD", "MD", "TO"]
VERB_TAGS = ["VB", "VBN", "VBD", "VBG", "VBZ"]
#MODAL_TAGS = ["V"]
TENSE_TAG = 'T'
EMPTY_SET = "∅"  # Ø

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
    'NN'   : 'N',
    'NNS'  : 'N',
    'NNP'  : 'N',
    'PRP'  : 'N',
    'NNPS' : 'N',
    # Verbs
    'VB'   : 'V',
    'VBN'  : 'V',
    'VBD'  : 'V',
    'VBG'  : 'V',
    'VBZ'  : 'V',
    'VBP'  : 'V',
    # Adjectives
    'ADJP' : 'AdjP',
    'JJ'   : 'Adj',  # Need to convert JJ to AdjP -> Adj
    # Conjuctions
    'CC'   : 'Conj',
    # Adverbs
    'ADVP' : 'AdvP',
    'RB'   : 'Adv',
    'RBR'  : 'Adv',
    # Prepositions
    'PRT'  : 'PP',
    'RP'   : 'P',
    'IN'   : 'P',
    'TO'   : 'P',
    #'IN': 'C',  # sometimes IN is C (complement)?

    # Modal issues:
    # 1) IF MD IS tense, then it needs to be moved to and a transfer must occur
    #    look at #8 from 10TAD3
    'MD'   : 'V',


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

# TAG_MAPPING_VERBS: Dict[Union[str, Any], Union[str, Any]] = \
TAG_MAPPING_VERBS: Dict[str, Dict[str, str]] = \
    {
        # Verbs
        'VB':  {'pos': 'V', 'tense': 'present' },  # base form
        'VBD': {'pos': 'V', 'tense': 'past'    },  # past tense
        'VBG': {'pos': 'V', 'tense': 'present' },  # gerund or present participle
        'VBN': {'pos': 'V', 'tense': 'past'    },  # past participle
        'VBP': {'pos': 'V', 'tense': 'present' },  # non-3rd person singular present
        'VBZ': {'pos': 'V', 'tense': 'present' },  # 3rd person singular present
    }


class Verb(object):
    def __init__(self, label, word):
        self.label = label
        self.word = word
        self.pos_penn = label
        self.pos_pdx = self.get_verb_pos(self.pos_penn)
        self.tense = self.get_verb_tense(self.pos_penn)

    def get_verb_properties(self, label):
        verb_properties = TAG_MAPPING_VERBS[label]

        return verb_properties

    def get_verb_pos(self, label):
        verb_props = TAG_MAPPING_VERBS[label]
        verb_pos = verb_props['pos']

        return verb_pos

    def get_verb_tense(self, label):
        verb_props = TAG_MAPPING_VERBS[label]
        verb_tense = verb_props['tense']

        return verb_tense


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

    @staticmethod
    def pretty_productions(t_prod):
        rules = ''
        for (mother, daughters) in t_prod:
            rules += format('{: <20} -> {}\n'.format(mother, ' '.join(daughters)))

        rules = os.linesep.join([st for st in rules.splitlines() if st])
        return rules

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

    ###################
    # Static helper methods
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
        children = []

        for t in tree:
            if isinstance(t, nltk.tree.Tree):
                children.append(self.convert_tree_labels(t, mapping))
            else:
                children.append(t)

        label = mapping.get(tree.label(), tree.label())
        return nltk.tree.Tree(label, children)

    def remove_duplicates(self, t, parent):
        if len(t) == 1:
            #only_child = getattr(t[0], 'label', lambda: None)()
            only_child = t[0]
            only_child = nltk.tree.ParentedTree.convert(only_child)
            if only_child.label() == t.label():
                parent.remove(t)
                parent.insert(len(parent), only_child)
                parent = nltk.tree.ParentedTree.convert(parent)
                return parent

    def traverse_tree_words(self, t):
        # print("tree:", tree)
        for subtree in t:
            if type(subtree) == nltk.tree.Tree:
                #assert isinstance(subtree, object)
                self.traverse_tree_words(subtree)
            else:
                print(subtree, end=" ")

    def write_tree_stream(self, nltk_tree):
        """
        Draws and outputs in PNG for ipython.
        PNG is used instead of PDF, since it can be displayed in the qt console and
        has wider browser support.
        """
        import os
        import base64
        import subprocess
        import tempfile
        from nltk.draw.tree import tree_to_treesegment
        from nltk.draw.util import CanvasFrame
        from nltk.internals import find_binary

        _canvas_frame = CanvasFrame()
        # widget = tree_to_treesegment(_canvas_frame.canvas(), self)
        widget = tree_to_treesegment(_canvas_frame.canvas(), nltk_tree)
        _canvas_frame.add_widget(widget)
        x, y, w, h = widget.bbox()
        # print_to_file uses scrollregion to set the width and height of the pdf.
        _canvas_frame.canvas()["scrollregion"] = (0, 0, w, h)
        with tempfile.NamedTemporaryFile() as file:
            in_path = "{0:}.ps".format(file.name)
            out_path = "{0:}.png".format(file.name)
            _canvas_frame.print_to_file(in_path)
            _canvas_frame.destroy_widget(widget)
            try:
                subprocess.call(
                    [
                        find_binary(
                            "gs",
                            binary_names=["gswin32c.exe", "gswin64c.exe"],
                            env_vars=["PATH"],
                            verbose=False,
                        )
                    ]
                    + "-q -dEPSCrop -sDEVICE=png16m -r90 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dSAFER -dBATCH -dNOPAUSE -sOutputFile={0:} {1:}".format(
                        out_path, in_path
                    ).split()
                )
            except LookupError:
                pre_error_message = str(
                    "The Ghostscript executable isn't found.\n"
                    "See http://web.mit.edu/ghostscript/www/Install.htm\n"
                    "If you're using a Mac, you can try installing\n"
                    "https://docs.brew.sh/Installation then `brew install ghostscript`"
                )
                print(pre_error_message, file=sys.stderr)
                raise LookupError

            with open(out_path, "rb") as sr:
                res = sr.read()
                b = bytearray(res)
                # b0 = b[0]
            os.remove(in_path)
            os.remove(out_path)
            # return base64.b64encode(res).decode()
            # return base64.b64encode(res)

            # return b0
            return b

    def next_preterminal(self, subtree, root):

        position = -1
        i = 0
        for st in root:
            if st == subtree:
                position = i
                break
            i += 1

        if position > -1:
            t = root[position + 1]
            while True:
                if type(t[0]) != str:
                    t = t[0]
                else:
                    return t

    @staticmethod
    def get_verb_tense(label):
        verb_properties = TAG_MAPPING_VERBS[label]
        verb_tense = verb_properties['tense']

        return verb_tense

    @staticmethod
    def create_feature_node(tag: str, feature: str) -> nltk.tree.ParentedTree:
        node = f"({tag} {feature})"
        node = nltk.tree.ParentedTree.fromstring(node)
        return node

    @staticmethod
    def get_position(subtree: nltk.tree.ParentedTree, root: nltk.tree.ParentedTree) -> int:
        position = -1
        i = 0
        for st in root:
            if st == subtree:
                position = i
                break
            i += 1

        return position

    #####################################
    # protected methods
    def add_tense(self, t):

        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        current = t
        for child in current:
            if self.terminal(child):
                next
            elif child.label() == "VP":
                for grandchild in child:
                    if grandchild.label() in TAG_MAPPING_VERBS:
                        verb = Verb(grandchild.label(), child[0])
                        if verb.tense == "past":
                            feature = "[+past]"
                        else:
                            feature = "[-past]"

                        tense_feature = self.create_feature_node(TENSE_TAG, feature)

                        vp_pos = self.get_position(child, current)
                        current.insert(vp_pos, tense_feature)
                        current = nltk.tree.ParentedTree.convert(current)
                        child = nltk.tree.ParentedTree.convert(child)

        for child in t:
            self.add_tense(child)

    def promote_tense(self, t):
        # VBN - Verb, past participle
        # VBP - Verb, non-3rd person singular present
        # VBZ
        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        if t.label() in MODAL_TAGS:
            current = t
            parent = current.parent()
            tense_node = nltk.tree.ParentedTree.fromstring(f"({TENSE_TAG} {t[0]})")

            #next_pt = self.next_preterminal(t.parent()[1])
            next_pt = self.next_preterminal(t, parent)

            if (next_pt.label() == "RB"):
                next_pt = self.next_preterminal(next_pt, parent)
                if next_pt is not None:
                    if (next_pt.label() in VERB_TAGS):
                        parent.remove(current)
                        grandpa = parent.parent()
                        grandpa.insert(len(grandpa) - 1, tense_node)
                        parent = nltk.tree.ParentedTree.convert(parent)
                        grandpa = nltk.tree.ParentedTree.convert(grandpa)
                        parent = self.remove_duplicates(parent, grandpa)
            elif (next_pt.label() in VERB_TAGS):
                parent.remove(current)
                grandpa = parent.parent()
                grandpa.insert(len(grandpa) - 1, tense_node)
                parent = nltk.tree.ParentedTree.convert(parent)
                grandpa = nltk.tree.ParentedTree.convert(grandpa)
                parent = self.remove_duplicates(parent, grandpa)

        for child in t:
            self.promote_tense(child)

    def collapse_only_child(self, t, label):
        try:
            t.label()
        except AttributeError:
            #print(t)
            return

        if t.label() == label and len(t) == 1:
            only_child = t[0]
            if only_child.label() == label:
                t.remove(t[0])
                i = 0
                for leaf in only_child:
                    leaf = nltk.tree.ParentedTree.convert(leaf)
                    t.insert(i, leaf)
                    i += 1

        for child in t:
            self.collapse_only_child(child, label)


        for child in t:
            self.collapse_only_child(child, label)

    def collapse_phrases(self, t, label):
        try:
            t.label()
        except AttributeError:
            #print(t)
            return

        to_move = []
        to_remove = None
        if t.label() == label:
            for c in t:
                if c.label() == label:
                    for g in c:
                        to_move.insert(0, g)
                    to_remove = c

        if to_remove is not None:
            t.remove(to_remove)
            t.extend(reversed(to_move))
            return

        for child in t:
            self.collapse_phrases(child, label)

    def expand_phrase_nodes(self, t, preterminal_tags):
        try:
            t.label()
        except AttributeError:
            #print(t)
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
            # elif parent.label() == phrase_label and len(parent) > 1:
            #     parent_index = current.parent_index()
            #     new_child = nltk.tree.ParentedTree.convert(current)
            #
            #     new_parent = nltk.tree.ParentedTree(phrase_label, [new_child])
            #     parent.remove(current)
            #     parent.insert(parent_index, new_parent)
            #
            #     # test t back to current before continuing to traverse.
            #     t = new_child

        for child in t:
            self.expand_phrase_nodes(child, preterminal_tags)

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
                empty_set_node = nltk.tree.Tree.fromstring(F"(C {EMPTY_SET})")
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

    def convert_sbar_cp_that(self, t):
        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        current = t
        for child in current:  # Current is NP
            if self.terminal(child):
                next
            elif child.label() == "SBAR":
                # collapse SBAR and S
                # Detach NP children
                # get 'that' from NP parent
                if child.left_sibling().label() != "NP":
                    return
                left_sibling_terminals = child.left_sibling().leaves()
                if left_sibling_terminals == ['That']:
                    # create that complement clause
                    c = nltk.ParentedTree.fromstring("(C That)")
                    cp = child
                    cp = nltk.ParentedTree.convert(cp)

                    # Now remove current
                    root = current.parent()
                    current_pos = self.get_position(current, root)
                    root.remove(current)
                    root.insert(current_pos, cp)
                    cp.insert(0, c)

                    root = nltk.ParentedTree.convert(root)

        for child in t:
            self.convert_sbar_cp_that(child)

    def convert_particle_prep(self, t):
        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        current = t
        for child in current:  # Current is NP
            if self.terminal(child):
                next
            elif child.label() == "PRT":

                right_sibling = child.right_sibling()

                current = nltk.ParentedTree.convert(current)
                child = nltk.ParentedTree.convert(child)

                new_right = nltk.Tree.convert(right_sibling)
                current.remove(right_sibling)
                new_right = nltk.ParentedTree.convert(new_right)

                #current[1].append(new_right)
                t[1].append(new_right)
                t.remove(right_sibling)
                #child.append(new_right)
                #child = nltk.ParentedTree.convert(child)

                current = nltk.ParentedTree.convert(current)
                t = nltk.ParentedTree.convert(t)
                #current = nltk.Tree.convert(current)
                print(f"blah")

                # current.remove(right_sibling)
                # # collapse SBAR and S
                # # Detach NP children
                # # get 'that' from NP parent
                # if child.left_sibling().label() != "NP":
                #     return
                # left_sibling_terminals = child.left_sibling().leaves()
                # if left_sibling_terminals == ['That']:
                #     # create that complement clause
                #     c = nltk.ParentedTree.fromstring("(C That)")
                #     cp = child
                #     cp = nltk.ParentedTree.convert(cp)
                #
                #     # Now remove current
                #     root = current.parent()
                #     current_pos = self.get_position(current, root)
                #     root.remove(current)
                #     root.insert(current_pos, cp)
                #     cp.insert(0, c)
                #
                #     root = nltk.ParentedTree.convert(root)

        for child in t:
            self.convert_particle_prep(child)

    # Make sure that the left child of a CP is a C
    def enforce_cpc(self, t: nltk.Tree):
        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        if t.label() == "CP":
            t[0].set_label("C")

        for child in t:
            self.enforce_cpc(child)

    # Make sure that the left child of a CP is a C
    def convert_adv_deg(self, t: nltk.Tree):

        # RB - Adverb
        # RBR - Adverb, comparative
        # RBS - Adverb, superlative

        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        if t.label() in ["ADJP", "ADVP"]:
            phrase = t

            try:
                if phrase[0].label() == "RB" and \
                   phrase[1].label() in ["RB", "JJ"]:
                    #t = nltk.ParentedTree.convert(t)
                    adv = phrase[0]
                    if adv[0] in ["too", "very"]:
                        if len(t) > 1:
                            if adv.right_sibling().label() in ["RB", "JJ"]:
                                deg = nltk.ParentedTree("Deg", [adv[0]])
                                t.remove(t[0])
                                t.insert(0, deg)

                                t = nltk.ParentedTree.convert(t)
                                parent = t.parent()
                                parent = nltk.ParentedTree.convert(parent)
            except:
                #print("swallow hard!")
                pass

        for child in t:
            self.convert_adv_deg(child)

    def convert_adv_neg(self, t: nltk.Tree):

        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        if t.label() in ["AdvP"]:
            phrase = t

            try:
                if phrase[0].label() == "Adv" and \
                   phrase[0][0] == 'not':
                    #t = nltk.ParentedTree.convert(t)
                    t.set_label('NegP')
                    phrase[0].set_label("Neg")
            except:
                #print("swallow hard!")
                pass

        for child in t:
            self.convert_adv_neg(child)


    # Make sure that the left child of a CP is a C
    def embed_n_np(self, t: nltk.Tree):

        # RB - Adverb
        # RBR - Adverb, comparative
        # RBS - Adverb, superlative

        try:
            t.label()
        except AttributeError:
            # print(t)
            return

        try:
            for child in t:
                #t = nltk.ParentedTree.convert(t)
                if child.label() == child.right_sibling().label() == "NN":
                    # noun = child
                    noun = nltk.ParentedTree("NN", [child[0]])

                    np = nltk.ParentedTree("NP", [noun])
                    child_pos = self.get_position(child, t)
                    t.remove(child)
                    t.insert(child_pos, np)

                    t = nltk.ParentedTree.convert(t)
                    parent = t.parent()
                    parent = nltk.ParentedTree.convert(parent)
        except Exception:
            #print("swallow hard!")
            pass

        for child in t:
            self.embed_n_np(child)

    ####################
    # Callers: They call recursive functions
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

    # def add_tense_phrase(self, t):
    #
    #     try:
    #         t.label()
    #     except AttributeError:
    #         # print(t)
    #         return
    #
    #
    #     self.promote_tense(t)
    #     self.add_tense(t)
    #
    #     for child in t:
    #         self.add_tense_phrase(child)

    ####################
    # Main public functions
    def parse_sentence(self, sentence, require_tense=False):
        print(sentence)

        tree = next(self.parser.raw_parse(sentence))

        # print(f"STANFORD: ********************************")
        # nltk.Tree.pretty_print(tree)
        # print(str(tree))
        # #self.write_to_file(tree, "XXXXXX_stanford")
        # ###############

        tree = nltk.ParentedTree.convert(tree)
        self.convert_adv_deg(tree)
        self.embed_n_np(tree)

        ##############################################
        # Tense Stuff
        if (require_tense):
            self.add_tense(tree)
        else:
            self.promote_tense(tree)
        #self.add_tense_phrase(tree)
        # self.promote_tense(tree)
        # self.add_tense(tree)

        self.convert_sbar_cp_that(tree)

        self.convert_particle_prep(tree)

        ##############################################################################
        # CONVERSION OF STANFORD TAGS TO SIMPLIFIED SET
        tree = self.convert_tree_labels(tree, tag_mapping)
        #print(f"CONVERT: ********************************")
        #nltk.Tree.pretty_print(tree)

        # Collapse Duplicate Nodes
        #tree = self.collapse_duplicate(tree)
        tree = nltk.tree.ParentedTree.convert(tree)
        self.collapse_only_child(tree, "VP")
        tree = nltk.tree.Tree.convert(tree)

        # print(f"BEFORE COLLAPSE: ********************************")
        # nltk.Tree.pretty_print(tree)
        # self.collapse_phrases(tree, "VP")
        # tree = nltk.tree.Tree.convert(tree)

        tree = self.expand_phrase(tree)
        self.convert_adv_neg(tree)
        self.add_complement(tree)

        self.enforce_cpc(tree)
        #print(str(tree))

        # Write PDX Parse Tree to .png file
        # self.write_to_file(tree, "XXXXXX_pdx")

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

##################################
# API Methods

#def parse(sentence, parser=None, output="bracketed", brackets="[]"):
def parse(sentence, parser, request_formats):
    tree_str = ""

    if parser == "pdx":
        # Use the default PSU Parser - but first use stanford and convert to PSU format
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        psu_tree = Tree(parser=stanford_parser)
        tree = psu_tree.parse_sentence(sentence, require_tense=False)
    elif parser == "stanford":
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        #tree_parser = Tree(parser=stanford_parser)
        tree = next(stanford_parser.raw_parse(sentence))

    print(tree_str)

    # Create dictionary of parse objects to return
    response_formats = {}

    if "tree_image" in request_formats:
        print("do image thingy")
        # print('getting object from tree.__repr__()')
        # img = tree.__repr__()
        psu_tree = Tree()
        # img = psu_tree.write_tree_stream(tree)
        img_byte_arr = psu_tree.write_tree_stream(tree)
        import base64
        # encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        encoded_img = base64.encodebytes(img_byte_arr).decode('ascii')
        response_formats["tree_image"] = encoded_img

    if "tree_ascii" in request_formats:
        print("add tree_ascii to output")

        from nltk.treeprettyprinter import TreePrettyPrinter
        ascii_str = str(TreePrettyPrinter(tree)).rstrip()
        #ascii_str = nltk.Tree.pretty_print(tree)
        response_formats["tree_ascii"] = ascii_str

    if "bracket_diagram" in request_formats:
        print("add labelled_bracket to output")
        bracket_diagram = str(tree)
        open_b, close_b = "[]"
        bracket_diagram = bracket_diagram.replace("(", open_b).replace(")", close_b)
        bracket_diagram = " ".join(bracket_diagram.split())
        response_formats["bracket_diagram"] = bracket_diagram

    if "tree_str" in request_formats:
        print("add tree_str to output")
        tree_str = str(tree)
        tree_str = " ".join(tree_str.split())
        response_formats["tree_str"] = tree_str

    res = {'sentence': sentence, 'parser': parser, 'response_formats': response_formats}

    return res

if __name__ == '__main__':
    # sentences = [
    #                 "The animals did not think the buffalo would eat them",
    #                 "They were afraid the buffalo would trample them",
    #                 "The buffalo were pursuing fresh grass",
    #                 "Those buffalo were large and lumbering",
    #                 "The herd that the animals had heard caused considerable alarm",
    #                 "One young buffalo trotted slowly behind the herd",
    #                 "He was smelling the fresh grass",
    #                 "This buffalo was wondering whether he would find any adventures",
    #                 "He was tired of the dry grassy plains",
    #                 "He thought that other places must be more interesting"
    #             ]
    #
    # parser = stanford.StanfordParser(model_path=model_path)
    # tree_builder = Tree(parser)
    # tree_builder.parse_sentences(sentences)

    parser = stanford.StanfordParser(model_path=model_path)
    tree_builder = Tree(parser)
    parse_tree = tree_builder.parse_sentence(sys.argv[1])
    parse_str = str(parse_tree)
    print(parse_str)
    sys.stdout.flush()



