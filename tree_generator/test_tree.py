import nose
import unittest
from tree import Tree
from nltk.parse import stanford
from nltk import Tree as nltk_tree
from nltk.draw.tree import TreeView
import inspect

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"

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

expected_parse_strings = [
    # 1. The animals did not think the buffalo would eat them
    "(TP (NP (D The) (N animals)) (T did) (VP (AdvP (Adv not)) (V think) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V eat) (NP (N them)))))))",
    # 2. They were afraid the buffalo would trample them
    "(TP (NP (N They)) (VP (V were) (AdjP (Adj afraid) (CP (TP (NP (D the) (N buffalo)) (T would) (VP (V trample) (NP (N them))))))))",
    # 3. The buffalo were pursuing fresh grass
    "(TP (NP (D The) (N buffalo)) (T were) (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass))))",
    # 4. Those buffalo were large and lumbering
    "(TP (NP (D Those) (N buffalo)) (T were) (VP (V were) (AdjP (Adj large) (Conj and) (Adj lumbering))))",
    # 5. The herd that the animals had heard caused considerable alarm
    "(TP (NP (NP (D The) (N herd)) (CP (C that) (TP (NP (D the) (N animals)) (T had) (VP (VBN heard))))) (VP (V caused) (NP (AdjP (Adj considerable)) (N alarm))))",
    # 6. One young buffalo trotted slowly behind the herd
    "(TP (NP (D One) (AdjP (Adj young)) (N buffalo)) (VP (VBN trotted) (AdvP (Adv slowly)) (PP (P behind) (NP (D the) (N herd)))))",
    # 7. He was smelling the fresh grass
    "(TP (NP (N He)) (T was) (VP (V smelling) (NP (D the) (AdjP (Adj fresh)) (N grass))))",
    # 8. This buffalo was wondering whether he would find any adventures
    "(TP (NP (D This) (N buffalo)) (T was) (VP (V wondering) (CP (P whether) (TP (NP (N he)) (T would) (VP (V find) (NP (D any) (N adventures)))))))",
    # 9. He was tired of the dry grassy plains
    "(TP (NP (N He)) (T was) (VP (AdjP (Adj tired) (PP (P of) (NP (D the) (AdjP (Adj dry)) (AdjP (Adj grassy)) (N plains))))))",
    # 10. He thought that other places must be more interesting
    "(TP (NP (N He)) (T thought) (VP (CP (P that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (RBR more) (Adj interesting)))))))"
]

class TestTree(unittest.TestCase):
    def test_tree_to_string(self):
        self.fail()

    def test_write_to_file(self):
        self.fail()

    def test_parse_sentence_integration(self):
        sentence = "He thought that other places must be more interesting"
        parser = stanford.StanfordParser(model_path=model_path)
        tree = Tree(parser)
        t = tree.parse_sentence(sentence)
        actual_str = inspect.cleandoc(tree.tree_to_string(t))
        print(f"Actual String: \n{actual_str}")

        expect_str = inspect.cleandoc("""(ROOT
          (S
            (NP (PRP He))
            (VP
              (VBD thought)
              (SBAR
                (IN that)
                (S
                  (NP (JJ other) (NNS places))
                  (VP
                    (MD must)
                    (VP (VB be) (ADJP (RBR more) (JJ interesting)))))))))""")

        print(f"Expected String: \n{expect_str}")
        self.assertEqual(actual_str, expect_str)

    def test_parse_sentence(self):
        sentence = "The dog chased the cat"
        tree_s = "(TP (NP (D The) (N dog)) (VP (V chased) (NP (D the) (N cat))))"
        expected_tree = nltk_tree.fromstring(tree_s, remove_empty_top_bracketing=True)
        expected_str = inspect.cleandoc(str(expected_tree))

        parser = stanford.StanfordParser(model_path=model_path)
        tree = Tree(parser)
        actual_tree = tree.parse_sentence(sentence)
        actual_str = inspect.cleandoc(str(actual_tree))

        print(f"Expected String: \n{expected_str}")
        print(f"Actual String: \n{actual_str}")

        self.assertEqual(actual_tree, expected_tree)


class TestTreeIntegration(unittest.TestCase):

    @staticmethod
    def get_expected_actual_trees(sentence, expected_tree_str, testid, debug=False):
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        parser = stanford.StanfordParser(model_path=model_path)
        tree = Tree(parser)
        actual_tree = tree.parse_sentence(sentence)
        actual_tree_str = inspect.cleandoc(str(actual_tree))

        if debug:
            print("#########################################################################################")
            print(f"Test Sentence {testid}: {sentence}:")
            print(f"Expected String: \n{expected_tree_str}\n")
            print(f"Actual String: \n{actual_tree_str}\n")
            tree.write_to_file(expected_tree, f"tree_expected_{testid}")
            tree.write_to_file(actual_tree, f"tree_actual_{testid}")

        return expected_tree, actual_tree

    # HW Tests: 10 Trees A Day # 3
    @unittest.skip("skip old")
    def test_ten_trees_a_all_old(self):
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
        tree = Tree(parser)
        tree.parse_sentences(sentences)

    def test_ten_trees_a_day_three(self):
        sentences = [
            # "The animals did not think the buffalo would eat them",
            # "They were afraid the buffalo would trample them",
            # "The buffalo were pursuing fresh grass",
            # "Those buffalo were large and lumbering",
            # "The herd that the animals had heard caused considerable alarm",
            # "One young buffalo trotted slowly behind the herd",
            "He was smelling the fresh grass",
            "This buffalo was wondering whether he would find any adventures",
            "He was tired of the dry grassy plains",
            "He thought that other places must be more interesting"
        ]

        expected_parse_strings = [
            # 1. The animals did not think the buffalo would eat them
            # "(TP (NP (D The) (N animals)) (T did) (VP (AdvP (Adv not)) (V think) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V eat) (NP (N them)))))))",
            # 2. They were afraid the buffalo would trample them
            # "(TP (NP (N They)) (VP (V were) (AdjP (Adj afraid) (CP (TP (NP (D the) (N buffalo)) (T would) (VP (V trample) (NP (N them))))))))",
            # # 3. The buffalo were pursuing fresh grass
            # "(TP (NP (D The) (N buffalo)) (T were) (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass))))",
            # # 4. Those buffalo were large and lumbering
            # "(TP (NP (D Those) (N buffalo)) (T were) (VP (V were) (AdjP (Adj large) (Conj and) (Adj lumbering))))",
            # # 5. The herd that the animals had heard caused considerable alarm
            # "(TP (NP (NP (D The) (N herd)) (CP (C that) (TP (NP (D the) (N animals)) (T had) (VP (VBN heard))))) (VP (V caused) (NP (AdjP (Adj considerable)) (N alarm))))",
            # # 6. One young buffalo trotted slowly behind the herd
            # "(TP (NP (D One) (AdjP (Adj young)) (N buffalo)) (VP (VBN trotted) (AdvP (Adv slowly)) (PP (P behind) (NP (D the) (N herd)))))",
            # 7. He was smelling the fresh grass
            "(TP (NP (N He)) (T was) (VP (V smelling) (NP (D the) (AdjP (Adj fresh)) (N grass))))",
            # 8. This buffalo was wondering whether he would find any adventures
            "(TP (NP (D This) (N buffalo)) (T was) (VP (V wondering) (CP (P whether) (TP (NP (N he)) (T would) (VP (V find) (NP (D any) (N adventures)))))))",
            # 9. He was tired of the dry grassy plains
            "(TP (NP (N He)) (T was) (VP (AdjP (Adj tired) (PP (P of) (NP (D the) (AdjP (Adj dry)) (AdjP (Adj grassy)) (N plains))))))",
            # 10. He thought that other places must be more interesting
            "(TP (NP (N He)) (T thought) (VP (CP (P that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (RBR more) (Adj interesting)))))))"
        ]

        i = 1
        for sentence, expected_parse_str in zip(sentences, expected_parse_strings):
            expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, i, True)
            i += 1
            self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_1_old(self):
        sentence = "The animals did not think the buffalo would eat them"
        expected_tree_str = inspect.cleandoc("""
        (TP
          (NP (D The) (N animals))
          (T did)
          (VP
            (AdvP 
                (Adv not))
            (V think)
            (CP
              (C ∅)
              (TP
                (NP (D the) (N buffalo))
                (T would)
                (VP (V eat) (NP (N them)))))))""")

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_tree_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    # def test_ten_trees_a_day_1(self):
    #
    #     expected_tree, actual_tree = self.get_expected_actual_trees(sentences[], expected_tree_str, 1, True)
    #     self.assertEqual(actual_tree, expected_tree)

    def test_traverse(self):
        from nltk.tree import ParentedTree
        expected_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (T did)
          (VP
            (RB not)
            (VP
              (VB think)
              (SBAR
                (S
                  (NP (DT the) (NN buffalo))
                  (VP (MD would) (VP (VB eat) (NP (PRP them)))))))))""")
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        before_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (VP
            (VBD did)
            (RB not)
            (VP
              (VB think)
              (SBAR
                (S
                  (NP (DT the) (NN buffalo))
                  (VP (MD would) (VP (VB eat) (NP (PRP them)))))))))""")

        before_tree = ParentedTree.fromstring(before_tree_str)
        steve_tree = Tree()
        steve_tree.traverse(before_tree)
        new_tree_str = str(before_tree)
        actual_tree = nltk_tree.fromstring(new_tree_str)
        print(f"Actual Tree: \n{actual_tree}\n")

        steve_tree.write_to_file(actual_tree, "moved_VZD_to_T")
        self.assertEqual(actual_tree, expected_tree)

    def test_promote_modals_to_tense(self):
        expected_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (T did)
          (VP
            (RB not)
            (VP
              (VB think)
              (SBAR
                (S
                  (NP (DT the) (NN buffalo))
                  (VP (MD would) (VP (VB eat) (NP (PRP them)))))))))""")
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        before_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (VP
            (VBD did)
            (RB not)
            (VP
              (VB think)
              (SBAR
                (S
                  (NP (DT the) (NN buffalo))
                  (VP (MD would) (VP (VB eat) (NP (PRP them)))))))))""")

        before_tree = nltk_tree.fromstring(before_tree_str)
        steve_tree = Tree()
        actual_tree = steve_tree.promote_modals_to_tense(before_tree)
        print(f"Actual Tree: \n{actual_tree}\n")

        steve_tree.write_to_file(actual_tree, "moved_VZD_to_T")
        self.assertEqual(actual_tree, expected_tree)

    def test_collapse_duplicate_nodes(self):
        expected_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (T did)
          (VP
            (RB not)
            (VB think)
            (SBAR
              (S
                (NP (DT the) (NN buffalo))
                (VP (MD would) (VP (VB eat) (NP (PRP them))))
              )
            )
          )
        )""")
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        before_tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NNS animals))
          (T did)
          (VP
            (RB not)
            (VP
              (VB think)
              (SBAR
                (S
                  (NP (DT the) (NN buffalo))
                  (VP (MD would) (VP (VB eat) (NP (PRP them))))
                )
              )
            )
          )
        )""")

        before_tree = nltk_tree.fromstring(before_tree_str)
        steve_tree = Tree()
        actual_tree = steve_tree.collapse_duplicate(before_tree)
        print(f"Actual Tree: \n{actual_tree}\n")

        steve_tree.write_to_file(actual_tree, "collapse_duplicate_nodes")
        self.assertEqual(actual_tree, expected_tree)

    def test_expand_phrase(self):
        expected_tree_str = inspect.cleandoc("""
        (TP
          (NP (D The) (N animals))
          (T did)
          (VP
            (AdvP 
                (Adv not))
            (V think)
            (CP
              (C ∅)
              (TP
                (NP (D the) (N buffalo))
                (T would)
                (VP (V eat) (NP (N them)))))))""")
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        before_tree_str = inspect.cleandoc("""
        (TP
          (NP (D The) (N animals))
          (T did)
          (VP
            (Adv not)
            (V think)
            (CP
              (C ∅)
              (TP
                (NP (D the) (N buffalo))
                (T would)
                (VP (V eat) (NP (N them)))))))""")

        before_tree = nltk_tree.fromstring(before_tree_str)
        steve_tree = Tree()
        actual_tree = steve_tree.expand_phrase(before_tree)
        print(f"Actual Tree: \n{actual_tree}\n")

        steve_tree.write_to_file(actual_tree, "expand_phrase_nodes")
        self.assertEqual(actual_tree, expected_tree)