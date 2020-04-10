import nose
import unittest
from nltk.parse import stanford
from nltk import Tree as nltk_tree
from nltk.draw.tree import TreeView
import inspect

#import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
#import inspect
import os
from io import StringIO
import logging

from tree import Tree

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"


class TestTree(unittest.TestCase):
    def test_tree_to_string(self):
        self.fail()

    def test_write_to_file(self):
        self.fail()

    def test_parse_stanford(self):
        sentence = "He thought that other places must be more interesting"

        stanford_parser = stanford.StanfordParser(model_path=model_path)
        tree = Tree(parser=stanford_parser)

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
        expected_tree = nltk_tree.fromstring(tree_s)
        expected_str = inspect.cleandoc(str(expected_tree))

        stanford_parser = stanford.StanfordParser(model_path=model_path)
        tree = Tree(parser=stanford_parser)
        actual_tree = tree.parse_sentence(sentence)
        actual_str = inspect.cleandoc(str(actual_tree))

        print(f"Expected String: \n{expected_str}")
        print(f"Actual String: \n{actual_str}")

        print(f"Expected String: \n{expected_str}")
        print(f"Actual String: \n{actual_str}")

        self.assertEqual(actual_tree, expected_tree)

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


class TestTenTreesADay3(unittest.TestCase):
    @staticmethod
    def get_expected_actual_trees(sentence, expected_tree_str, testid, debug=False):
        stanford_parser = stanford.StanfordParser(model_path=model_path)

        tree = Tree(parser=stanford_parser)
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        actual_tree = tree.parse_sentence(sentence)
        actual_tree_str = inspect.cleandoc(str(actual_tree)).replace('\n', '').replace('\r', '').replace('  ', ' ')

        # tree.write_to_file(expected_tree, "tree_expected_XX")
        # tree.write_to_file(actual_tree, "tree_expected_XX")

        if debug:
            print("\n#########################################################################################")
            print(f"Test Sentence {testid}:\n {sentence}:")

            # print(f"Actual String: \n{str(actual_tree)}\n")
            # print(f"Expected String: \n{str(expected_tree)}\n")

            tree.write_to_file(expected_tree, f"tree_expected_{testid}")
            tree.write_to_file(actual_tree, f"tree_actual_{testid}")

            print(f"{testid}) ACTUAL: ********************************")
            nltk_tree.pretty_print(actual_tree)

            print(f"{testid}) EXPECTED: ********************************")
            nltk_tree.pretty_print(expected_tree)

        return expected_tree, actual_tree

    @unittest.skip("")
    def test_productions_demo(self):
        s = "(TP (NP (D The) (N dog)) (VP (V chased) (NP (D the) (N cat))))"
        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

    def test_ten_trees_a_day_three_01(self):
        sentence = "The animals did not think the buffalo would eat them"
        expected_parse_str = \
            "(TP (NP (D The) (N animals)) (T did) (VP (AdvP (Adv not)) (V think) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V eat) (NP (N them)))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_02(self):
        sentence = "They were afraid the buffalo would trample them"
        expected_parse_str = \
            "(TP (NP (N They)) (VP (V were) (AdjP (Adj afraid) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V trample) (NP (N them))))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_03(self):
        sentence = "The buffalo were pursuing fresh grass"
        expected_parse_str = \
            "(TP (NP (D The) (N buffalo)) (T were) (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_04(self):
        sentence = "Those buffalo were large and lumbering"
        expected_parse_str = \
            "(TP (NP (D Those) (N buffalo)) (VP (V were) (AdjP (AdjP (Adj large)) (Conj and) (AdjP (Adj lumbering)))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_05(self):
        sentence = "The herd that the animals had heard caused considerable alarm"
        expected_parse_str = \
            "(TP (NP (NP (D The) (N herd)) (CP (C that) (TP (NP (D the) (N animals)) (T had) (VP (V heard))))) (VP (V caused) (NP (AdjP (Adj considerable)) (N alarm))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_06(self):
        sentence = "One young buffalo trotted slowly behind the herd"
        expected_parse_str = \
            "(TP (NP (D One) (AdjP (Adj young)) (N buffalo)) (VP (V trotted) (AdvP (Adv slowly)) (PP (P behind) (NP (D the) (N herd)))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_07(self):
        sentence = "He was smelling the fresh grass"
        expected_parse_str = \
            "(TP (NP (N He)) (T was) (VP (V smelling) (NP (D the) (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_08(self):
        sentence = "This buffalo was wondering whether he would find any adventures"
        expected_parse_str = \
            "(TP (NP (D This) (N buffalo)) (T was) (VP (V wondering) (CP (C whether) (TP (NP (N he)) (T would) (VP (V find) (NP (D any) (N adventures)))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_09(self):
        sentence = "He was tired of the dry grassy plains"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V was) (AdjP (Adj tired) (PP (P of) (NP (D the) (AdjP (Adj dry)) (AdjP (Adj grassy)) (N plains))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_10(self):
        sentence = "He thought that other places must be more interesting"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V thought) (CP (C that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (AdvP (Adv more)) (AdjP (Adj interesting))))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_book23_10(self):
        sentence = "He thought that other places must be more interesting"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V thought) (CP (C that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (AdvP (Adv more)) (AdjP (Adj interesting))))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_book23_23a(self):
        sentence = "the big yellow book"
        expected_parse_str = \
            "(FRAG (NP (D the) (AdjP (Adj big)) (AdjP (Adj yellow)) (N book)))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_book23_23b(self):
        sentence = "the very yellow book"
        expected_parse_str = \
            "(FRAG (NP (D the) (AdjP (AdvP (Adv very)) (Adj yellow)) (N book)))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTreesADay4(unittest.TestCase):
    @staticmethod
    def get_expected_actual_trees(sentence, expected_tree_str, testid, debug=False):
        stanford_parser = stanford.StanfordParser(model_path=model_path)

        tree = Tree(parser=stanford_parser)
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        actual_tree = tree.parse_sentence(sentence)
        actual_tree_str = inspect.cleandoc(str(actual_tree)).replace('\n', '').replace('\r', '').replace('  ', ' ')

        # tree.write_to_file(expected_tree, "tree_expected_XX")
        # tree.write_to_file(actual_tree, "tree_expected_XX")

        if debug:
            print("#########################################################################################")
            print(f"Test Sentence {testid}:\n {sentence}:")

            print(f"Expected String: \n{str(expected_tree)}\n")
            print(f"Actual String: \n{str(actual_tree)}\n")

            tree.write_to_file(expected_tree, f"tree_expected_{testid}")
            tree.write_to_file(actual_tree, f"tree_actual_{testid}")

            ohsu_tree = Tree.from_string(expected_tree_str)
            expect_pretty_str = ohsu_tree.pretty()
            print(f"{testid}) EXPECTED PRETTY: ********************************")
            print(expect_pretty_str)

            ohsu_tree = Tree.from_string(actual_tree_str)
            actual_pretty_str = ohsu_tree.pretty()
            print(f"{testid}) ACTUAL PRETTY: **********************************")
            print(actual_pretty_str)

        return expected_tree, actual_tree

    def test_ten_trees_a_day_four_01(self):
        sentence = "The herd slowly came to a stop"
        expected_parse_str = \
            "(TP (NP (D The) (N animals)) (T did) (VP (AdvP (Adv not)) (V think) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V eat) (NP (N them)))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_02(self):
        sentence = "The mouse peeked her head out of the hole"
        expected_parse_str = \
            "(TP (NP (N They)) (VP (V were) (AdjP (Adj afraid) (CP (C Ø) (TP (NP (D the) (N buffalo)) (T would) (VP (V trample) (NP (N them))))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_03(self):
        sentence = "She saw a young buffalo nearby"
        expected_parse_str = \
            "(TP (NP (D The) (N buffalo)) (T were) (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_04(self):
        sentence = "The buffalo looked too young to be dangerous"
        expected_parse_str = \
            "(TP (NP (D Those) (N buffalo)) (VP (V were) (AdjP (AdjP (Adj large)) (Conj and) (AdjP (Adj lumbering)))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_05(self):
        sentence = "The mouse began to talk to the young buffalo"
        expected_parse_str = \
            "(TP (NP (NP (D The) (N herd)) (CP (C that) (TP (NP (D the) (N animals)) (T had) (VP (V heard))))) (VP (V caused) (NP (AdjP (Adj considerable)) (N alarm))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_06(self):
        sentence = "The mouse asked about life on the plains"
        expected_parse_str = \
            "(TP (NP (D One) (AdjP (Adj young)) (N buffalo)) (VP (V trotted) (AdvP (Adv slowly)) (PP (P behind) (NP (D the) (N herd)))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_07(self):
        sentence = "The mouse had lived in the city before she had moved to the country"
        expected_parse_str = \
            "(TP (NP (N He)) (T was) (VP (V smelling) (NP (D the) (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_08(self):
        sentence = "The mouse and the buffalo talked for a while"
        expected_parse_str = \
            "(TP (NP (D This) (N buffalo)) (T was) (VP (V wondering) (CP (C whether) (TP (NP (N he)) (T would) (VP (V find) (NP (D any) (N adventures)))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_09(self):
        sentence = "She could tell the buffalo about many other places"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V was) (AdjP (Adj tired) (PP (P of) (NP (D the) (AdjP (Adj dry)) (AdjP (Adj grassy)) (N plains))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_10(self):
        sentence = "The buffalo would have listened to her for hours"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V thought) (CP (C that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (AdvP (Adv more)) (AdjP (Adj interesting))))))))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)
