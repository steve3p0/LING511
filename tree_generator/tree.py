import os
#from nltk.parse import stanford
import nltk
from nltk.draw.tree import TreeView
from PIL import Image

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

#model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"

# mapping = {'NP-SBJ': 'NP', 'NP-TMP': 'NP'}
tag_mapping = {
    # Sentence
    'S': 'TP',
    'SBAR': 'CP',
    # Determiners
    'DT': 'D',
    'CD': 'D',
    # Nouns
    'NN': 'N',
    'NNS': 'N',
    'PRP': 'N',
    # Verbs
    'VB': 'V',
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
    # Prepositions
    'IN': 'P',
    # 'IN': 'C', sometimes IN is C (complement)?

    # issues:
    # 1) IF MD IS tense, then it needs to be moved to and a transfer must occur
    #    look at #8 from 10TAD3
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
    def __init__(self, parser=None):
        self.parser = parser

    @staticmethod
    def tree_to_string(tree):
        s = str(tree)
        # pformat(self, margin=70, indent=0, nodesep="", parens="()", quotes=False)
        #s = tree.pformat()
        return s

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

    def promote_tense(self, t, modal_labels, new_label):
        try:
            t.label()
        except AttributeError:
            return

        if t.label() in modal_labels:
            current = t
            parent = current.parent()
            grandpa = parent.parent()
            parent.pop(0)

            # to do:
            # tense = nltk.tree.ParentedTree.fromstring(f"({new_label} {t[0]})")
            tense = nltk.tree.ParentedTree.convert(nltk.tree.Tree.fromstring(f"({new_label} {t[0]})"))
            grandpa.insert(1, tense)

        for child in t:
            self.promote_tense(child, modal_labels, new_label)

    def promote_modals_to_tense(self, t):
        # VBN - Verb, past participle
        # VBP - Verb, non-3rd person singular present
        # VBZ
        ptree = nltk.tree.ParentedTree.convert(t)
        modal_tags = ["VBD", "MD"]
        self.promote_tense(ptree, modal_tags, "T")
        new_tree_str = str(ptree)
        new_tree = nltk.tree.Tree.fromstring(new_tree_str)
        return new_tree

    def collapse_duplicate_nodes(self, t, label):
        try:
            t.label()
        except AttributeError:
            return

        if t.label() == label:
            current = t
            parent = current.parent()
            if parent.label() == label and current.right_sibling() is None:
                current = t
                parent = current.parent()

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

        if t.label() in preterminal_tags:
            current = t
            current_position = t.treeposition()
            parent = current.parent()
            phrase_label = f"{t.label()}P"
            if parent.label() != phrase_label:
                grandpa = parent.parent()
                parent_index = current.parent_index()
                new_child = nltk.tree.ParentedTree.convert(current)
                #parent.pop(current_position)
                #r = current.root()
                #r.remove(current_position)
                #r_list = list()

                new_parent = nltk.tree.ParentedTree(phrase_label, [new_child])
                parent.remove(current)

                #new_parent = nltk.tree.ParentedTree("AdvP", [nltk.tree.ParentedTree([new_child])])
                # new_parent = nltk.tree.ParentedTree(phrase_label, [
                #     nltk.tree.ParentedTree('NOUN', ['dog'])])
                #new_parent = nltk.tree.ParentedTree(f"{phrase_label}", new_child)
                # new_parent = nltk.tree.ParentedTree.fromstring(f"{phrase_label}", new_child)
                # new_parent = nltk.tree.ParentedTree.fromstring(f"({phrase_label})", [new_child])
                # new_parent.insert(0, new_child)

                #parent.insert(current_position, new_parent)
                #grandpa.insert(parent_index, new_parent)
                parent.insert(parent_index, new_parent)
            # test t back to current before continuing to traverse.
            t = new_child

        for child in t:
            self.expand_phrase_nodes(child, preterminal_tags)

    def expand_phrase(self, t):
        # Search for preterminals with child_label that are not a child of a phrase (phrase_label)
        # Insert a phrase node above the child
        preterminal_tags = ["Adv", "Adj"]

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

    def parse_sentence(self, sentence):
        tree = next(self.parser.raw_parse(sentence))

        tree = self.promote_modals_to_tense(tree)
        tree = self.collapse_duplicate(tree)
        tree = self.convert_tree_labels(tree, tag_mapping)

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

# if __name__ == '__main__':
#     # sentences = ["He thought that other places must be more interesting"]
#
#     sentences = [
#                     "The animals did not think the buffalo would eat them",
#                     "They were afraid the buffalo would trample them",
#                     "The buffalo were pursuing fresh grass",
#                     "Those buffalo were large and lumbering",
#                     "The herd that the animals had heard caused considerable alarm",
#                     "One young buffalo trotted slowly behind the herd",
#                     "He was smelling the fresh grass",
#                     "This buffalo was wondering whether he would find any adventures",
#                     "He was tired of the dry grassy plains",
#                     "He thought that other places must be more interesting"
#                 ]
#
#     parser = stanford.StanfordParser(model_path=model_path)
#     tree_builder = TreeBuilder(parser)
#     tree_builder.parse_sentences(sentences)

