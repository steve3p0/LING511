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

    # def traverse(self, t, np_trees):
    #     # VBN - Verb, past participle
    #     # VBP - Verb, non-3rd person singular present
    #     # VBZ
    #
    #     try:
    #         t.label()
    #     except AttributeError:
    #         return
    #
    #     if t.label() == "VBZ":
    #         current = t
    #         while current.parent() is not None:
    #             while current.left_sibling() is not None:
    #                 if current.left_sibling().label() == "NP":
    #                     np_trees.append(current.left_sibling())
    #                 current = current.left_sibling()
    #             current = current.parent()
    #
    #     for child in t:
    #         self.traverse(child, np_trees)

    def traverse(self, t, np_trees):
        # VBN - Verb, past participle
        # VBP - Verb, non-3rd person singular present
        # VBZ

        try:
            t.label()
        except AttributeError:
            return

        if t.label() == "VBD":
            current = t
            parent = current.parent()
            #new_parent = parent
            #new_parent.remove(t[0])
            #new_parent.remove('did')
            #new_parent.remove('VBD')
            grandpa = parent.parent()
            parent.pop(0)

            #grandpa.insert(1, current)
            tense = nltk.tree.Tree.fromstring(f"(T {t[0]})")
            tense = nltk.tree.ParentedTree.convert(nltk.tree.Tree.fromstring(f"(T {t[0]})"))
            grandpa.insert(1, tense)
            #grandpa.insert(1, nltk.tree.Tree('T', [t[0]]))
            #left_uncle = parent.left_sibiling()




            #grandpa.insert(1,  nltk.tree.Tree('T', ['fuck']))
            #grandpa.insert(1, nltk.tree.Tree('T', [t[0]]))

            #t[0]

            # while current.parent() is not None:
            #     while current.left_sibling() is not None:
            #         if current.left_sibling().label() == "NP":
            #             # STOP
            #             # np_trees.append(current.left_sibling())
            #
            #
            #
            #
            #         current = current.left_sibling()
            #     current = current.parent()

        for child in t:
            self.traverse(child, np_trees)

    def parse_sentence(self, sentence):
        tree = next(self.parser.raw_parse(sentence))
        #tree = self.convert_tree_labels(tree, tag_mapping)
        # Get rid of of ROOT node
        return tree[0]
        #return tree

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

