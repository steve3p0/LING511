import nose
import unittest
from tree import Tree
from nltk.parse import stanford
from nltk import Tree as nltk_tree
from nltk.draw.tree import TreeView
import inspect

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"

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
            print(f"Expected String: \n{expected_tree_str}\n")
            print(f"Actual String: \n{actual_tree_str}\n")
            # expected_tree.draw()
            # import threading
            # actual_thread = threading.Thread(target=expected_tree.draw)
            # actual_thread.start()
            tree.write_to_file(expected_tree, f"tree_expected_{testid}")
            tree.write_to_file(actual_tree, f"tree_actual_{testid}")

        return expected_tree, actual_tree

    # HW Tests: 10 Trees A Day # 3
    # @unittest.skip("demonstrating skipping")
    def test_ten_trees_a_all_all3(self):
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

    def test_ten_trees_a_day_1(self):
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

