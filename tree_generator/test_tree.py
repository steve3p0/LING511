import nltk
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

import tree
from tree import Tree

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"


def get_expected_actual_trees(sentence, expected_tree_str, testid, debug=False, require_tense=False):
    stanford_parser = stanford.StanfordParser(model_path=model_path)

    tree = Tree(parser=stanford_parser)
    expected_tree = nltk_tree.fromstring(expected_tree_str)

    actual_tree = tree.parse_sentence(sentence, require_tense=require_tense)
    #actual_tree_str = inspect.cleandoc(str(actual_tree)).replace('\n', '').replace('\r', '').replace('  ', ' ')
    actual_tree_str = inspect.cleandoc(str(actual_tree))

    if debug:
        print("\n#########################################################################################")
        print(f"Test Sentence {testid}:\n {sentence}:")

        # Write output to .png file
        tree.write_to_file(expected_tree, f"tree_expected_{testid}")
        tree.write_to_file(actual_tree, f"tree_actual_{testid}")

        print(f"{testid}) EXPECTED: ********************************")
        nltk_tree.pretty_print(expected_tree)
        print(f"{testid}) ACTUAL: ********************************")
        nltk_tree.pretty_print(actual_tree)

        print(f"{testid}) EXPECTED: ********************************")
        print(f"Expected String: \n{str(expected_tree)}\n")
        print(f"{testid}) ACTUAL: ********************************")
        print(f"Actual String: \n{actual_tree_str}\n")

        tree.write_to_file(expected_tree, "tree_expected_XX")
        tree.write_to_file(actual_tree, "tree_actual_XX")

    return expected_tree, actual_tree


class TestTree(unittest.TestCase):

    def test_next_preterminal(self):
        tree_str = inspect.cleandoc("""
        (S
            (NP 
                (DT The) 
                (NN buffalo))
            (VP 
                (VBD were) 
                (VP 
                    (VBG pursuing) 
                    (NP 
                        (JJ fresh) 
                        (NN grass)
                    )
                )
            )
        )""")

        t = nltk_tree.fromstring(tree_str)
        t = nltk.tree.ParentedTree.convert(t)
        vbd = t[1][0]
        assert(vbd.label() == "VBD")

        tree = Tree()
        #vbg1 = None
        vbg = tree.next_preterminal(vbd.parent()[1])

        assert(vbg.label() == "VBG")

    def test_traverse_tree_small(self):
        tree_str = inspect.cleandoc("""
        (VP (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass)))))""")

        t = nltk_tree.fromstring(tree_str)

        tree = Tree()
        tree.traverse_tree_words(t)

    def test_traverse_tree(self):
        tree_str = inspect.cleandoc("""
        (ROOT
          (S
            (NP (DT The) (NN buffalo))
            (VP (VBD were) (VP (VBG pursuing) (NP (JJ fresh) (NN grass))))))""")

        t = nltk_tree.fromstring(tree_str)

        tree = Tree()
        tree.traverse_tree_words(t)

    def test_copy_tree(self):
        tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NN buffalo))
          (VP (VBD were) (VP (VBG pursuing) (NP (JJ fresh) (NN grass)))))""")

        t = nltk_tree.fromstring(tree_str)

        psu_tree = Tree()
        new_tree = psu_tree.copy_tree(t)

        self.assertEqual(t, new_tree)

    def test_promote_tense_1(self):
        tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NN herd))
          (VP
            (ADVP (RB slowly))
            (VBD came)
            (PP (TO to) (NP (DT a) (NN stop))))))""")

        t = nltk_tree.fromstring(tree_str)

        psu_tree = Tree()
        new_tree = psu_tree.copy_tree(t)

        self.assertEqual(t, new_tree)

    def test_next_preterminal(self):
        tree_str = inspect.cleandoc("""
        (S
          (NP (DT The) (NN herd))
          (VP
            (ADVP (RB slowly))
            (VBD came)
            (PP (TO to) (NP (DT a) (NN stop))))))""")

        t = nltk_tree.fromstring(tree_str)

        psu_tree = Tree()
        new_tree = psu_tree.copy_tree(t)

        self.assertEqual(t, new_tree)

    def test_tree_to_string(self):
        self.fail()

    def test_write_to_file(self):
        filename = "test_write_to_file"
        parse_str = "(S (NP (N Steve)) (VP (V drinks) (NP (N cider))))"

        tree = nltk_tree.fromstring(parse_str)
        psu_tree = Tree()
        psu_tree.write_to_file(tree, filename)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_file_path = dir_path + "\\" + filename + ".png"

        self.assertTrue(os.path.isfile(full_file_path))

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
        expected_tree_str = inspect.cleandoc(f"""
        (TP
          (NP (D The) (N animals))
          (T did)
          (VP
            (AdvP 
                (Adv not))
            (V think)
            (CP
              (C {tree.EMPTY_SET})
              (TP
                (NP (D the) (N buffalo))
                (T would)
                (VP (V eat) (NP (N them)))))))""")
        expected_tree = nltk_tree.fromstring(expected_tree_str)

        before_tree_str = inspect.cleandoc(f"""
        (TP
          (NP (D The) (N animals))
          (T did)
          (VP
            (Adv not)
            (V think)
            (CP
              (C {tree.EMPTY_SET})
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

    def test_ten_trees_a_day_three_01(self):
        sentence = "The animals did not think the buffalo would eat them"
        expected_parse_str = \
            f"(TP (NP (D The) (N animals)) (T did) (VP (AdvP (Adv not)) (V think) (CP (C {tree.EMPTY_SET}) (TP (NP (D the) (N buffalo)) (T would) (VP (V eat) (NP (N them)))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_02(self):
        sentence = "They were afraid the buffalo would trample them"
        expected_parse_str = \
            f"(TP (NP (N They)) (VP (V were) (AdjP (Adj afraid) (CP (C {tree.EMPTY_SET}) (TP (NP (D the) (N buffalo)) (T would) (VP (V trample) (NP (N them))))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_03(self):
        sentence = "The buffalo were pursuing fresh grass"
        expected_parse_str = \
            "(TP (NP (D The) (N buffalo)) (T were) (VP (V pursuing) (NP (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_04(self):
        sentence = "Those buffalo were large and lumbering"
        expected_parse_str = \
            "(TP (NP (D Those) (N buffalo)) (VP (V were) (AdjP (Adj large) (Conj and) (Adj lumbering))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_05(self):
        sentence = "The herd that the animals had heard caused considerable alarm"
        expected_parse_str = \
            "(TP (NP (NP (D The) (N herd)) (CP (C that) (TP (NP (D the) (N animals)) (T had) (VP (V heard))))) (VP (V caused) (NP (AdjP (Adj considerable)) (N alarm))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_06(self):
        sentence = "One young buffalo trotted slowly behind the herd"
        expected_parse_str = \
            "(TP (NP (D One) (AdjP (Adj young)) (N buffalo)) (VP (V trotted) (AdvP (Adv slowly)) (PP (P behind) (NP (D the) (N herd)))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_07(self):
        sentence = "He was smelling the fresh grass"
        expected_parse_str = \
            "(TP (NP (N He)) (T was) (VP (V smelling) (NP (D the) (AdjP (Adj fresh)) (N grass))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_08(self):
        sentence = "This buffalo was wondering whether he would find any adventures"
        expected_parse_str = \
            "(TP (NP (D This) (N buffalo)) (T was) (VP (V wondering) (CP (C whether) (TP (NP (N he)) (T would) (VP (V find) (NP (D any) (N adventures)))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_09(self):
        sentence = "He was tired of the dry grassy plains"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V was) (AdjP (Adj tired) (PP (P of) (NP (D the) (AdjP (Adj dry)) (AdjP (Adj grassy)) (N plains))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_three_10(self):
        sentence = "He thought that other places must be more interesting"
        expected_parse_str = \
            "(TP (NP (N He)) (VP (V thought) (CP (C that) (TP (NP (AdjP (Adj other)) (N places)) (T must) (VP (V be) (AdjP (AdvP (Adv more)) (Adj interesting)))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

    @unittest.skip("Book Excercises")
    def test_productions_demo(self):
        s = "(TP (NP (D The) (N dog)) (VP (V chased) (NP (D the) (N cat))))"
        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

    @unittest.skip("Book Excercises")
    def test_book23_23a(self):
        sentence = "the big yellow book"
        expected_parse_str = \
            "(FRAG (NP (D the) (AdjP (Adj big)) (AdjP (Adj yellow)) (N book)))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

    @unittest.skip("Book Excercises")
    def test_book23_23b(self):
        sentence = "the very yellow book"
        expected_parse_str = \
            "(FRAG (NP (D the) (AdjP (AdvP (Adv very)) (Adj yellow)) (N book)))"

        expected_tree, actual_tree = self.get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTreesADay4(unittest.TestCase):

    def test_ten_trees_a_day_four_01(self):
        sentence = "The herd slowly came to a stop"
        expected_parse_str = \
            "(TP (NP (D The) (N herd)) (VP (AdvP (Adv slowly)) (V came) (PP (P to) (NP (D a) (N stop)))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_02(self):
        sentence = "The mouse peeked her head out of the hole"
        expected_parse_str = \
            "(TP(NP (D The) (N mouse))(VP (V peeked) (NP (D her) (N head)) (PRT (RP out)) (PP (P of) (NP (D the) (N hole)))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_03(self):
        sentence = "She saw a young buffalo nearby"
        expected_parse_str = \
            "(TP(NP (N She))(VP (V saw) (NP (D a) (AdjP (Adj young)) (N buffalo)) (AdvP (Adv nearby))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_04(self):
        sentence = "The buffalo looked too young to be dangerous"
        expected_parse_str = \
            f"(TP(NP (D The) (N buffalo))(VP (V looked) (AdjP  (AdvP (Deg too))  (Adj young)  (TP (NP {tree.EMPTY_SET}) (VP (P to) (V be) (AdjP (Adj dangerous)))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_05(self):
        sentence = "The mouse began to talk to the young buffalo"
        expected_parse_str = \
            f"(TP(NP (D The) (N mouse)) (VP (V began) (TP (NP {tree.EMPTY_SET}) (P to) (VP (V talk) (PP (P to) (NP (D the) (AdjP (Adj young)) (N buffalo)))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_06(self):
        sentence = "The mouse asked about life on the plains"
        expected_parse_str = \
            "(TP(NP (D The) (N mouse))(VP (V asked) (PP (P about) (NP (N life))) (PP (P on) (NP (D the) (N plains)))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_07(self):
        sentence = "The mouse had lived in the city before she had moved to the country"
        expected_parse_str = \
            "(TP(NP (D The) (N mouse))(T had)(VP (V lived) (PP (P in) (NP (D the) (N city))) (CP  (C before)  (TP   (NP (N she))   (T had)   (VP (V moved) (PP (P to) (NP (D the) (N country))))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_08(self):
        sentence = "The mouse and the buffalo talked for a while"
        expected_parse_str = \
            "(TP(NP (NP (D The) (N mouse)) (Conj and) (NP (D the) (N buffalo)))(VP (V talked) (PP (P for) (NP (D a) (N while)))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_09(self):
        sentence = "She could tell the buffalo about many other places"
        expected_parse_str = \
            "(TP(NP (N She))(T could)(VP (V tell) (NP  (NP (D the) (N buffalo))  (PP   (P about)   (NP (AdjP (Adj many)) (AdjP (Adj other)) (N places))))))"

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_ten_trees_a_day_four_10(self):
        sentence = "The buffalo would have listened to her for hours"
        expected_parse_str = inspect.cleandoc("""
            (TP 
                (NP (D The) (N buffalo)) 
                (T would) 
                (VP (V have) 
                    (VP 
                        (V listened) 
                        (PP (P to) (NP (N her))) 
                        (PP (P for) (NP (N hours)))
                    )
                )
            )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)


# 10TAD5 Isn't dddddeedasdfasdfasdf setup yet
class TestTenTAD_05(unittest.TestCase):

    def test_10TAD5_01(self):
        sentence = "The buffalo had always lived on the grassy plains"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_02(self):
        sentence = "The buffalo longed for adventure"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_03(self):
        #sentence = "He wanted to explore the wide, wide world"
        sentence = "He wanted to explore the wide wide world"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_04(self):
        sentence = "The mouse woke the buffalo early one day"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_05(self):
        sentence = "The mouse told the buffalo that there were places far away"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_06(self):
        sentence = "The mouse’s stories were very interesting"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_07(self):
        sentence = "The buffalo decided to travel to new places"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_08(self):
        sentence = "He trotted eagerly away from his herd"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_09(self):
        sentence = "He soon came to a river"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD5_10(self):
        sentence = "The river blocked the buffalo’s path"
        expected_parse_str = inspect.cleandoc("""
            (TP 
                (NP (D The) (N buffalo)) 
                (T would) 
                (VP (V have) 
                    (VP 
                        (V listened) 
                        (PP (P to) (NP (N her))) 
                        (PP (P for) (NP (N hours)))
                    )
                )
            )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)

class TestTenTAD_06(unittest.TestCase):

    def test_10TAD06_01(self):
        sentence = "The deep river flowed quickly"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (AdjP (Adj deep)) (N river))
            (VP (V flowed) (AdvP (Adv quickly))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=False, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD06_02(self):
        sentence = "The buffalo pondered his options"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (N buffalo))
            (VP (V pondered) (NP (D his) (N options))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=3, require_tense=False, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD06_03(self):
        sentence = "He might be considered a foolish young buffalo"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (N He))
        (T might)
        (VP
          (V be)
          (VP
            (V considered)
            (NP (D a) (AdjP (Adj foolish)) (AdjP (Adj young)) (N buffalo)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_04(self):
        sentence = "The buffalo waded into the river and swam"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP 
                (D The) 
                (N buffalo)
            )
            (VP
                (VP
                    (V waded)
                    (PP (P into) (NP (D the) (N river)))
                ) 
                (VP 
                    (Conj and) 
                    (N swam)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_05(self):
        sentence = "The fast current caught him by surprise"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (AdjP (Adj fast)) (N current))
            (VP (V caught) (NP (N him)) (PP (P by) (NP (N surprise)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_06(self):
        sentence = "He tumbled down the river out of control"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N He))
            (VP
                (V tumbled)
                (PP 
                    (P down)
                    (NP
                        (D the)
                        (N river)
                    )
                )
                (PP 
                    (P out) 
                    (PP 
                        (P of) 
                        (NP (N control))
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_07(self):
        sentence = "The buffalo began to panic"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP 
                (D The) (N buffalo)
            )
            (VP 
                (V began) 
                (TP 
                    (NP (N {tree.EMPTY_SET}))
                    (T to) 
                    (VP (V panic))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_08(self):
        sentence = "He cried out for help"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N He))
            (VP
                (VP 
                    (V cried) 
                    (P out)
                )
            ) 
            (PP 
                (P for) 
                (NP (N help))
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_09(self):
        sentence = "A wily old mare on the other bank heard his frantic cries"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP
          (NP (D A) (AdjP (Adj wily)) (AdjP (Adj old)) (N mare))
          (PP (P on) (NP (D the) (AdjP (Adj other)) (N bank))))
        (VP (V heard) (NP (D his) (AdjP (Adj frantic)) (N cries))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD06_10(self):
        sentence = "She quickly cantered to the riverbank"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (VP
                (AdvP (Adv quickly))
                (V cantered)
                (PP (P to) (NP (D the) (N riverbank)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_07(unittest.TestCase):

    @unittest.skip("Unit Test")
    def test_get_verb_tense(self):
        input_label = "VBD"
        expect_tense = "past"
        actual_tense = Tree.get_verb_tense(input_label)

        self.assertEqual(expect_tense, actual_tense)

    @unittest.skip("Unit Test")
    def test_if_label_is_verb(self):

        input_label = "VBD"
        if input_label in tree.TAG_MAPPING_VERBS:
            self.assertTrue(True)

    def test_10TAD07_01(self):
        sentence = "The mare quickly assessed the situation"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (N mare))
            (T [+past])
            (VP 
                (AdvP (Adv quickly)) 
                (V assessed) 
                (NP (D the) (N situation))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD07_02(self):
        sentence = "That the buffalo was in trouble was clear to her"
        expected_parse_str = inspect.cleandoc("""
        (TP
           (CP 
              (C That)
              (TP
                 (NP (D the) (N buffalo))
                 (T [+past])
                 (VP 
                    (V was) 
                    (PP 
                       (P in) 
                       (NP (N trouble))
                    )
                 )
              )
           )
           (T [+past])
           (VP (V was) (AdjP (Adj clear) (PP (P to) (NP (N her))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=3, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD07_03(self):
        sentence = "The river was flowing too fast for him"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (N river))
            (T was)
            (VP
              (V flowing)
              (AdvP (Deg too) (Adv fast))
              (PP (P for) (NP (N him)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_04(self):
        sentence = "Her options were very limited"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D Her) (N options))
            (T [+past])
            (VP 
                (V were) 
                (AdjP 
                    (Deg very) 
                    (Adj limited)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_05(self):
        sentence = "She saw a large branch on the river bank"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (T [+past])
            (VP
                (V saw)
                (NP (D a) (AdjP (Adj large)) (N branch))
                (PP 
                    (P on) 
                    (NP 
                        (D the) 
                        (NP (N river)) 
                        (N bank)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_06(self):
        sentence = "She swiftly grabbed the branch with her teeth"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (T [+past])
            (VP
                (AdvP (Adv swiftly))
                (V grabbed)
                (NP (D the) (N branch))
                (PP (P with) (NP (D her) (N teeth)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_07(self):
        sentence = "She tossed the branch into the river"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (T [+past])
            (VP
                (V tossed)
                (NP (D the) (N branch))
                (PP (P into) (NP (D the) (N river)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_08(self):
        sentence = "She then yelled for him to swim to it"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (T [+past])
            (VP
                (AdvP (Adv then))
                (V yelled)
                (CP
                    (C for)
                    (TP
                        (NP (N him))
                        (T to)
                        (VP 
                            (V swim) 
                            (PP 
                                (P to) 
                                (NP (N it))
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_09(self):
        #sentence = "The buffalo ran to the branch"
        sentence = "The buffalo swam to the branch"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP (V swam) (PP (P to) (NP (D the) (N branch)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_10(self):
        sentence = "He wished that he had opposable thumbs so he could grab the branch"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (N He))
        (T [+past])
        (VP
          (V wished)
          (CP
            (C that)
            (TP
              (NP (N he))
              (T [-past])
              (VP
                (V had)
                (NP (AdjP (Adj opposable)) (N thumbs))
                (CP
                  (C so)
                  (TP
                    (NP (N he))
                    (T could)
                    (VP (V grab) (NP (D the) (N branch))))))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_08(unittest.TestCase):

    def test_10TAD10_01(self):
        sentence = "The buffalo chomped down on the branch with his powerful jaws"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP
                (V chomped)
                (PP 
                    (P down)
                    (PP 
                        (P on) 
                        (NP (D the) (N branch))
                    )
                    (PP 
                        (P with) 
                        (NP 
                            (D his) 
                            (AdjP (Adj powerful)) 
                            (N jaws)
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD10_02(self):
        sentence = "He whirled with the branch down the river"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N He))
        (T [+past])
        (VP
          (V whirled)
          (PP (P with) (NP (D the) (N branch)))
          (PP (P down) (NP (D the) (N river)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD10_03(self):
        sentence = 'They soon became stuck in the bank of the river'
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N They))
            (T [+past])
            (VP
                (AdvP (Adv soon))
                (V became)
                (AdjP
                    (Adj stuck)
                    (PP
                        (P in)
                        (NP
                            (D the)
                            (N bank)
                            (PP 
                                (P of)
                                (NP (D the) (N river))
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_04(self):
        sentence = "The old mare cantered over to him"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (AdjP (Adj old)) (N mare))
            (T [+past])
            (VP 
                (V cantered) 
                (PP 
                    (P over)
                    (PP 
                        (P to) 
                        (NP (N him))
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_05(self):
        sentence = "She dangled her long flowing tail into the water for the buffalo to grab"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N She))
            (T [+past])
            (VP
                (V dangled)
                (NP (D her) (AdjP (Adj long)) (AdjP (Adj flowing)) (N tail))
                (PP
                    (P into)
                    (NP (D the) (N water))
                )
                (CP
                    (C for)
                    (TP
                        (NP
                            (D the)
                            (N buffalo)
                        )
                        (T to) 
                        (VP (V grab))
                    )
                )
            )    
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_06(self):
        sentence = "He grabbed her tail"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V grabbed)
                (NP (D her) (N tail))
            )    
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_07(self):
        sentence = "She pulled the buffalo with great strength"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (N She))
        (T [+past])
        (VP
          (V pulled)
          (NP (D the) (N buffalo))
          (PP (P with) (NP (AdjP (Adj great)) (N strength)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_08(self):
        sentence = "The buffalo slowly scrambled up the bank with the mare’s help"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP
                (AdvP (Adv slowly))
                (V scrambled)
                (PP 
                    (P up)
                    (NP (D the) (N bank))
                )
                (PP 
                    (P with) 
                    (NP 
                        (NP 
                            (D the) 
                            (N mare's)
                        )
                        (N help)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_09(self):
        # sentence = "The buffalo ran to the branch"
        sentence = "He flopped exhausted onto the green grass"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V flopped)
                (AdjP (Adj exhausted))
                (PP 
                    (P onto) 
                    (NP 
                        (D the) 
                        (AdjP (Adj green))
                        (N grass)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_10(self):
        sentence = "For the buffalo to be saved pleased the old mare"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (CP
                (C For)
                (TP
                    (NP (D the) (N buffalo))
                    (T to)
                    (VP (V be) (VP (V saved)))
                )
            )
            (T [+past])
            (VP
                (V pleased)
                (NP 
                    (D the) (AdjP (Adj old)) (N mare)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True,
                                                               require_tense=False)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_09(unittest.TestCase):

    def test_10TAD_01(self):
        sentence = "The old mare walked over to the recumbent buffalo"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (AdjP (Adj old)) (N mare))
            (T [+past])
            (VP
            (V walked)
                (PP 
                    (P over)
                    (PP (P to) (NP (D the) (AdjP (Adj recumbent)) (N buffalo)))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_02(self):
        sentence = "I want to know why you were crossing the treacherous river"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (T [-past])
            (VP
                (V want)
                (CP
                    (C {tree.EMPTY_SET})
                    (TP
                        (NP {tree.EMPTY_SET})
                        (T to)
                        (VP
                            (V know)
                            (CP
                                (C why)
                                (TP
                                    (NP (N you))
                                    (T were)
                                    (VP
                                        (V crossing)
                                        (NP 
                                            (D the) 
                                            (AdjP (Adj treacherous)) 
                                            (N river)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=False, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_03(self):
        sentence = 'I am going to see the city'
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (T am)
            (VP
                (V going) 
                (TP 
                    (T to) 
                    (VP 
                        (V see) 
                        (NP (D the) (N city))
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True,
                                                               require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_04(self):
        sentence = "A mouse told me that cities are sensational"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (D A) (N mouse))
        (T [+past])
        (VP
          (V told)
          (NP (N me))
          (CP
            (C that)
            (TP
              (NP (N cities))
              (T [-past])
              (VP (V are) (AdjP (Adj sensational)))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_05(self):
        sentence = "You silly young buffalo"
        expected_parse_str = inspect.cleandoc("""
        (NP 
            (D You) 
            (AdjP (Adj silly)) 
            (AdjP (Adj young)) 
            (N buffalo)
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_06(self):
        sentence = "Cities are only for people"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N Cities))
            (T [-past])
            (VP (V are) (AdvP (Adv only)) (PP (P for) (NP (N people)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_07(self):
        sentence = "They are not for buffalos or for horses"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (N They))
        (T [-past])
        (VP
          (V are)
          (NegP (Neg not))
          (PP
            (PP (P for) (NP (N buffalos)))
            (Conj or)
            (PP (P for) (NP (N horses))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_08(self):
        sentence = "The young buffalo pondered this new information thoughtfully"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (D The) (AdjP (Adj young)) (N buffalo))
        (T [+past])
        (VP
          (V pondered)
          (NP (D this) (AdjP (Adj new)) (N information))
          (AdvP (Adv thoughtfully))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_09(self):
        sentence = "I want to know why cities are not for buffalos"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N I))
            (T [-past])
            (VP
                (V want)
                (TP
                    (T to)
                    (VP
                        (V know)
                        (CP
                            (C why)
                            (TP
                                (NP (N cities))
                                [-past]
                                (VP
                                    (V are)
                                    (NegP (Neg not))
                                    (PP (P for) (NP (N buffalos)))
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True,
                                                               require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_10(self):
        sentence = "Cities do not have enough grass"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (N Cities))
            (T [-past])
            (VP
                (V do)
                (NegP (Neg not))
                (T [-past])
                (VP 
                    (V have) 
                    (NP 
                        (AdjP 
                            (Adj enough)
                        ) 
                        (N grass)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True,
                                                               require_tense=True)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_10(unittest.TestCase):

    def test_10TAD10_01(self):
        sentence = "Places that do not have grass sound very unhealthy"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP
                (NP (NNPS Places))
                (CP 
                    (C that)
                    (TP
                        (NP {tree.EMPTY_SET})
                        (T do)
                        (VP 
                            (NegP (Neg not))
                            (V have)
                            (NP (N grass))
                        )
                    )
                )
            )
            (T [-past])
            (VP
                (V sound)
                (AdjP
                    (AdvP (Adv very))
                    (Adj unhealthy)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD10_02(self):
        sentence = "I wonder why the mouse thought that cities are exciting"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N I))
        (T [-past])
        (VP
          (V wonder)
          (CP
            (C why)
            (TP
              (NP (D the) (N mouse))
              (T [+past])
              (VP
                (V thought)
                (CP
                  (C that)
                  (TP
                    (NP (N cities))
                    (T [-past])
                    (VP (V are) (AdjP (Adj exciting))))))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD10_03(self):
        sentence = 'The mare said "Mice are very different from us"'
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N mare))
            (T [+past])
            (VP
                (V said)
                (CP
                    (C {tree.EMPTY_SET})
                    (TP
                        (NP (N Mice))
                        (T [-past])
                        (VP
                            (V are)
                            (AdjP 
                                (Deg very) 
                                (Adj different) 
                                (PP (P from) (NP (N us)))
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_04(self):
        sentence = "The bedraggled young buffalo looked dejected"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP 
                (D The) 
                (AdjP (Adj bedraggled)) 
                (AdjP (Adj young)) 
                (N buffalo)
            )
            (T [+past])
            (VP (V looked) (AdjP (Adj dejected))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_05(self):
        sentence = "The old mare took pity upon the inexperienced buffalo"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (AdjP (Adj old)) (N mare))
            (T [+past])
            (VP
                (V took)
                (NP 
                    (N pity)
                    (PP 
                        (P upon) 
                        (NP 
                            (D the) 
                            (AdjP (Adj inexperienced)) 
                            (N buffalo)
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_06(self):
        sentence = "The eager buffalo reminded her of herself in her younger days"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (AdjP (Adj eager)) (N buffalo))
            (T [+past])
            (VP
                (V reminded)
                (NP (N her))
                (PP 
                    (P of) 
                    (NP 
                        (N herself)
                        (PP 
                            (P in) 
                            (NP 
                                (D her) 
                                (AdjP (Adj younger))
                                (N days)
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_07(self):
        sentence = "The mare’s thoughts turned to her youthful adventures"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP 
                (NP 
                    (D The) 
                    (N mare's) 
                ) 
                (N thoughts)
            )
            (T [+past])
            (VP
                (V turned)
                (PP 
                    (P to) 
                    (NP 
                        (D her) 
                        (AdjP (Adj youthful)) 
                        (N adventures)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_08(self):
        sentence = "I can recommend an exciting place that is more friendly to buffalo"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (T can)
            (VP
                (VP
                    (V recommend)
                    (NP
                        (NP (D an) (AdjP (Adj exciting)) (N place))
                        (CP
                            (C that)
                            (TP
                                (NP {tree.EMPTY_SET})
                                (T [-past])
                                (VP
                                    (V is)
                                    (AdjP
                                        (AdvP (Adv more))
                                        (Adj friendly)
                                        (PP (P to) (NP (N buffalo)))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_09(self):
        #sentence = "The buffalo ran to the branch"
        sentence = "For you to have an adventure does not require a city"
        expected_parse_str = inspect.cleandoc("""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP (V swam) (PP (P to) (NP (D the) (N branch)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD10_10(self):
        sentence = "I would suggest the bluffs high above the river"
        expected_parse_str = inspect.cleandoc("""
        (TP
        (NP (N I))
        (T would)
        (VP
          (V suggest)
          (TP
            (NP (D the) (N bluffs))
            (AdjP (Adj high) (PP (P above) (NP (D the) (N river)))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_11(unittest.TestCase):

    def test_10TAD_01(self):
        sentence = "You will find all of the experiences a buffalo would want near the bluffs"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N You))
            (T will)
            (VP	  
                (V find)
                (NP
                    (NP (D all))
                    (PP
                        (P of)
                        (NP
                            (NP (D the) (N experiences))
                            (CP
                                (C {tree.EMPTY_SET})
                                (TP
                                    (NP (D a) (N buffalo))
                                    (T would)
                                    (VP (V want)) 
                                )
                            )
                        )
                    )
                )
                (PP 
                    (P near) 
                    (NP 
                        (D the) 
                        (N bluffs)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_02(self):
        sentence = "The bluffs have forests, prairie, storms, wind and wolves"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N bluffs))
            (T [-past])
            (VP
                (V have)
                (NP
                    (NP (N forests))
                    (NP (N prairie))
                    (NP (N storms))
                    (NP (N wind))
                    (Conj and)
                    (NP (N wolves))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_03(self):
        sentence = "The restless young buffalo perked up at these new tidings"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (AdjP (Adj restless)) (AdjP (Adj young)) (N buffalo))
            (T [+past])
            (VP
                (VP 
                    (V perked)
                    (P up)
                )
                (PP 
                    (P at) 
                    (NP 
                        (D these) 
                        (AdjP (Adj new))
                        (N tidings)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_04(self):
        sentence = "The bluffs must be a fine place indeed"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N bluffs))
            (T must)
            (VP
                (V be)
                (NP 
                    (D a) 
                    (AdjP (Adj fine)) 
                    (N place)
                )
                (AdvP (Adv indeed))
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_05(self):
        sentence = 'The mare continued “You could also search for the ancient gargantuan wisteria that all buffalo hold sacred"'
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N mare))
            (T [+past])
            (VP
                (V continued)
                (CP 
                    (C {tree.EMPTY_SET})
                    (TP
                        (NP (N You))
                        (T could)
                        (VP
                            (AdvP (Adv also))
                            (V search)
                            (PP
                                (P for)
                                (NP
                                    (D the)
                                    (AdjP (Adj ancient))
                                    (AdjP (Adj gargantuan))
                                    (N wisteria)
                                )
                                (CP
                                    (C that)
                                    (TP
                                        (NP (D all) (N buffalo))
                                        (T [-past])
                                        (VP (V hold) (AdjP (Adj sacred)))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_06(self):
        sentence = "The buffalo’s ears twitched with excitement at the prospect of a new adventure"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (NP (D The) (N buffalo's)) (N ears))
            (T [+past])
            (VP
                (V twitched)
                (PP 
                    (P with) 
                    (NP 
                        (N excitement)
                        (PP
                            (P at)
                            (NP
                                (D the) 
                                (N prospect)
                                (PP 
                                    (P of)
                                    (NP 
                                        (D a) 
                                        (AdjP (Adj new)) 
                                        (N adventure)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_07(self):
        sentence = "He straightened his shoulders with resolve"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V straightened)
                (NP (D his) (N shoulders))
                (PP (P with) (NP (N resolve)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_08(self):
        sentence = "That there was another exciting place was something he had never considered"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (CP
                (C That)
                (TP
                    (NP (N there))
                    (T [+past])
                    (VP 
                        (V was) 
                        (NP 
                            (AdjP (Adj another))
                            (AdjP (Adj exciting)) 
                            (N place)
                        )
                    )
                )
            )	
            (T [+past])
            (VP
                (V was)
                (NP 
                    (N something)
                    (CP
                        (C {tree.EMPTY_SET})
                        (TP
                            (NP (N he))
                            (T had)
                            (VP
                                (AdvP (Adv never))
                                (T [+past])
                                (V considered)
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_09(self):
        sentence = "The bison turned to the mare"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N bison))
            (T [+past])
            (VP (V turned) (PP (P to) (NP (D the) (N mare)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_10(self):
        sentence = "I cannot thank you enough"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (T can)
            (VP
                (NegP (Neg not))
                (V thank) 
                (NP (N you)) 
                (AdvP (Adv enough))
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_12(unittest.TestCase):

    def test_10TAD_01(self):
        sentence = "The old mare told the buffalo how he could find the bluffs"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (NP (D The) (AdjP (Adj old)) (N mare)))
            (T [+past])
            (VP
                (V told)
                (NP (D the) (N buffalo))
                (CP
                    (C how)
                    (TP
                        (NP (N he))
                        (T could)
                        (VP 
                            (V find) 
                            (NP 
                                (D the) 
                                (N bluffs)
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_02(self):
        sentence = "The mare was sure that he would find the adventure he longed for"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N mare))
            (T [+past])
            (VP
                (V was)
                (AdjP (Adj sure))
                (CP
                    (C that)
                    (TP
                        (NP (N he))
                        (V would)
                        (VP
                            (V find)
                            (NP 
                                (D the) 
                                (N adventure)
                            )
                            (CP
                                (C {tree.EMPTY_SET})
                                (TP
                                    (NP (N he))
                                    (T [+past])
                                    (VP (V longed) (PP (P for)))
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_03(self):
        sentence = "The mare’s thoughts turned to her father’s advice when she was a filly"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (NP (D The) (N mare's)) (N thoughts))
            (T [+past])
            (VP
                (V turned)
                (PP 
                    (P to) 
                    (NP 
                        (NP (D her) (N father's)) 
                        (N advice)
                    )
                    (CP
                        (C (WRB when))
                        (TP 
                            (NP (N she)) 
                            (T [+past]) 
                            (VP 
                                (V was) 
                                (NP 
                                    (D a) 
                                    (N filly)
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_04(self):
        sentence = "Her father had warned her that she should think carefully about adventures"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D Her) (N father))
            (T had)
            (VP
                (V warned)
                (NP (N her))
                (CP
                    (C that)
                    (TP
                        (NP (N she))
                        (T should)
                        (VP
                            (V think)
                            (AdvP (Adv carefully)
                                  (PP (P about) (NP (N adventures)))
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_05(self):
        sentence = "Unplanned exploits could be very dangerous for young animals"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (AdjP (Adj Unplanned)) (N exploits))
            (T could)
            (VP
                (V be)
                (AdvP (Adv very))
                (Adj dangerous)
                (PP (P for) (NP (AdjP (Adj young)) (N animals)))
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_06(self):
        sentence = "Meanwhile, the buffalo trotted off into the wilderness"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (AdvP (Adv Meanwhile))
        (, ,)
        (NP (D the) (N buffalo))
        (T [+past])
        (VP
          (V trotted)
          (PP (P off) (PP (P into) (NP (D the) (N wilderness))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_07(self):
        sentence = "That he would not find adventure never occurred to him"
        sentence = "boy meets world"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (CP
                (C That)
                (TP
                    (NP (N he))
                    (T would)
                    (VP
                        (NegP (Neg not))
                        (V find)
                        (NP (N adventure))
                    )
                )
            )
            (T [+past])
            (VP
                (AdvP (Adv never))
                (V occurred)
                (PP 
                    (P to)
                    (NP (N him))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_08(self):
        sentence = "He was very sure of himself for one who was so young"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V was)
                (AdvP 
                    (Adv very) 
                    (Adj sure) 
                    (PP (P of) (NP (N himself)))
                    (PP
                        (P for)
                        (NP 
                            (N one)
                            (CP
                                (C {tree.EMPTY_SET})
                                (TP
                                    (NP 
                                        (N who)
                                        (T [+past])
                                        (VP 
                                            (V was) 
                                            (AdjP 
                                                (AdvP (Adv so)) 
                                                (Adj young)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_09(self):
        sentence = "The doughty buffalo came to a tall grassy slope ere long"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (AdjP (Adj doughty)) (N buffalo))
            (T [+past])
            (VP
                (V came)
                (PP
                    (P to)
                    (NP
                        (D a)
                        (AdjP (Adj tall))
                        (AdjP (Adj grassy))
                        (N slope)
                    )
                )
                (PP 
                    (P ere)
                    (NP (N long))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_10(self):
        sentence = "The slope soon became precipitously steep"
        sentence = "boy meets world"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP 
                (D The)
                (N Slope)
            )
            (T [+past])
            (VP
                (AdvP (Adv soon))
                (V became)
                (AdjP 
                    (AdvP (Adv precipitously))
                    (Adj steep)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)


class TestTenTAD_13(unittest.TestCase):

    def test_10TAD_01(self):
        sentence = "The buffalo struggled mightily while he climbed the hill"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (D The) (N buffalo))
        (T [+past])
        (VP
          (V struggled)
          (AdvP (Adv mightily))
          (CP
            (C while)
            (TP
              (NP (N he))
              (T [+past])
              (VP (V climbed) (NP (D the) (N hill)))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_02(self):
        sentence = "He longed for there to be a spring with fresh water"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
              (V longed)
              (CP
                (C for)
                (TP
                  (NP (N there))
                  (T to)
                  (VP
                    (V be)
                    (NP
                        (D a) 
						(N spring)
                        (PP (P with) (NP (AdjP (Adj fresh)) (N water)))
                    )
                  )
                )
              )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_03(self):
        sentence = "The buffalo grew gloomier and gloomier"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP
                (V grew)
                (AdjP (AdjP (adj gloomier)) (Conj and) (AdjP (Adj gloomier)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_04(self):
        sentence = "I should not have come by myself"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (V should)
            (VP
                (NegP (Neg not))
                (V have)
                (VP
                    (V come)
                    (PP (P by) (NP (N myself)))
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_05(self):
        sentence = "I wish I had a friend with me"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N I))
        (T [-past])
        (VP
          (V wish)
          (CP
            (C ∅)
            (TP
              (NP (N I))
              (T [+past])
              (VP
                (V had)
                (NP (NP (D a) (N friend)) (PP (P with) (NP (N me)))))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_06(self):
        sentence = "Suddenly, he cocked his head alertly"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (AdvP (Adv Suddenly))
            (NP (N he))
            (T [+past])
            (VP 
                (V cocked) 
                (NP (D his) (N head)) 
                (AdvP (Adv alertly))
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_07(self):
        sentence = "I hear the sound of water in the distance"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N I))
            (T [-past])
            (VP
                (V hear)
                (NP 
                    (D the) (N sound)
                    (PP
                        (P of)
                        (N water)
                    )
                )
                (PP 
                    (P in) 
                    (NP 
                        (D the) 
                        (N distance)
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_08(self):
        sentence = "The thought that he would soon be drinking fresh water buoyed the buffalo’s spirits"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP
                (D The) 
                (N thought)
                (CP
                    (C that)
                    (TP
                        (NP (N he))
                        (T would)
                        (VP
                            (AdvP (Adv soon))
                            (V be)
                            (VP 
                                (V drinking) 
                                (NP (AdjP (Adj fresh)) (N water))
                            )
                        )
                    )
                )
            )
            (T [+past])
            (VP 
                (V buoyed)
                (NP 
                    (NP 
                        (D the)
                        (N buffalo's)
                    ) 
                    (N spirits)
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_09(self):
        sentence = "He scrambled energetically up the hill toward the water"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V scrambled)
                (AdvP (Adv energetically))
                (PP
                    (P up)
                    (NP (D the) (N hill))
                )
                (PP (P toward) (NP (D the) (N water)))
            )
        )
        """)

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_10(self):
        sentence = "He soon came to a glistening lake that was surrounded by various trees"
        #sentence = "boy meets world"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (AdvP (Adv soon))
                (V came)
                (PP
                    (P to)
                    (NP
                        (D a) 
                        (Adj glistening)
                        (N lake)
                        (CP
                            (C that)
                            (TP
                                (NP (N {tree.EMPTY_SET}))
                                (T was)
                                (VP
                                    (V surrounded)
                                    (PP 
                                        (P by) 
                                        (NP 
                                            (AdjP (Adj various)) 
                                            (N trees)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=False)
        self.assertEqual(actual_tree, expected_tree)

class TestTenTAD_14(unittest.TestCase):

    def test_10TAD_01(self):
        sentence = "A small stream trickled into the lake"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (D A) (AdjP (Adj small)) (N stream))
        (T [+past])
        (VP (V trickled) (PP (P into) (NP (D the) (N lake)))))
        """)

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_02(self):
        sentence = "The lake was glassy smooth except for the ripples from the stream"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N lake))
            (T [+past])
            (VP
                (V was)
                (AdjP
                    (AdvP (Adv glassy))
                    (Adj smooth)
                    (PP 
                        (P except) 
                        (PP 
                            (P for) 
                            (NP (D the) (N ripples))
                            (PP (P from) (NP (D the) (N stream)))
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD_03(self):
        sentence = "The buffalo cautiously walked toward the lake"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (D The) (N buffalo))
        (T [+past])
        (VP
          (AdvP (Adv cautiously))
          (V walked)
          (PP (P toward) (NP (D the) (N lake)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_04(self):
        sentence = "He scanned the area for potential dangers"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N He))
        (T [+past])
        (VP
          (V scanned)
          (NP (D the) (N area))
          (PP (P for) (NP (AdjP (Adj potential)) (N dangers)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_05(self):
        sentence = "He then bent his head and drank deeply"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N He))
        (T [-past])
        (VP
          (VP (AdvP (Adv then)) (V bent) (NP (D his) (N head)))
          (Conj and)
          (VP (V drank) (AdvP (Adv deeply)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_06(self):
        sentence = "The buffalo suddenly saw himself in his reflection from the lake"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (D The) (N buffalo))
            (T [+past])
            (VP
                (AdvP (Adv suddenly))
                (V saw)
                (NP (N himself))
                (PP 
                    (P in) 
                    (NP 
                        (D his) 
                        (N reflection)
                        (PP 
                            (P from) 
                            (NP 
                                (D the) 
                                (N lake)
                            )
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_07(self):
        sentence = "I look terribly disheveled"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N I))
        (T [-past])
        (VP (V look) (AdjP (AdvP (Adv terribly)) (Adj disheveled))))
        """)

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_08(self):
        sentence = "He waded into the water to wash"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
            (NP (N He))
            (T [+past])
            (VP
                (V waded)
                (PP (P into) (NP (D the) (N water)))
                (CP 
                    (C {tree.EMPTY_SET})
                    (TP 
                        (NP 
                            (N {tree.EMPTY_SET})
                            (T to) 
                            (V wash)
                        )
                    )
                )
            )
        )""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_09(self):
        sentence = "The water felt glorious on the buffalo’s pelt"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (D The) (N water))
        (T [+past])
        (VP
          (V felt)
          (NP
            (NP (AdjP (Adj glorious)))
            (PP (P on) (NP (NP (D the) (N buffalo's)) (N pelt))))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD_10(self):
        sentence = "I feel like myself again"
        expected_parse_str = inspect.cleandoc(f"""
        (TP
        (NP (N I))
        (T [-past])
        (VP (V feel) (PP (P like) (NP (N myself))) (AdvP (Adv again))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 10, True, require_tense=True)
        self.assertEqual(actual_tree, expected_tree)


class Quiz1(unittest.TestCase):

    def test_gps6_sentence_a(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
        parse_str = inspect.cleandoc("""
        (TP (NP (D The) (N dog)) (T should) (VP (V put) (NP (D his) (AdjP (Adj squeaky)) (N toy)) (PP (P on) (NP (D the) (AdjP (Adj fuzzy)) (N rug)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sa")

    def test_gps6_sentence_b(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
        parse_str = inspect.cleandoc("""
        (TP
          (NP (D The) (AdjP (AdvP (Adv very)) (Adj stormy)) (N weather))
          (T has)
          (VP
            (V swept)
            (NP (D the) (N lawnchairs))
            (PP (P into) (NP (D the) (N lake)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    def test_gps6_sentence_c(self):
        sentence = "Scholars wonder if the library might contain the rare books"
        parse_str = inspect.cleandoc("""
        (TP
          (NP (N Scholars))
          (VP
            (V wonder)
            (CP
              (C if)
              (TP
                (NP (D the) (N library))
                (T might)
                (VP (V contain) (NP (D the) (AdjP (Adj rare)) (N books)))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    #def test_gps6_rules_a(self):

    def test_quiz1_constit_sentence_a(self):
        sentence = "Jouri wrote a book in her spare time"
        parse_str = inspect.cleandoc("""
        (TP 
           (NP (N Jouri))
           (T [+past])
           (VP 
              (V wrote) 
              (NP (D a) (N book)) 
              (PP 
                 (P in) 
                 (NP 
                    (D her) 
                    (AdjP (Adj spare)) 
                    (N time))))) """)

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_a")

    def test_quiz1_constit_sentence_b(self):
        sentence = "The car in the tunnel stalled during rush hour"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (D The) 
                (N car) 
                (PP 
                    (P in) 
                    (NP 
                        (D the)
                        (N tunnel)
                    )
                )
            ) 
            (VP 
                (V stalled) 
                (PP 
                    (P during) 
                    (NP 
                        (N rush) 
                        (N hour)
                    )
                )
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_b")

    def test_quiz1_constit_sentence_c(self):
        sentence = "The neighbor yelled at the kids for no good reason"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP (D The) (N neighbor)) 
            (T [+past])
            (VP 
                (V yelled) 
                (PP (P at) (NP (D the) (N kids))) 
                (PP (P for) (NP (D no) (AdjP (Adj good)) (N reason))))) """)

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_c")

    def test_quiz1_constit_sentence_d(self):
        sentence = "The book on the shelf contains many illustrations in color"

        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (D The) 
                (N book) 
                (PP 
                    (P on) 
                    (NP (D the) (N shelf))
                )
            ) 
            (VP 
                (V contains) 
                (NP 
                    (NP 
                        (AdjP 
                            (Adj many)
                        ) 
                        (N illustrations) 
                        (PP 
                            (P in) 
                            (NP 
                                (N color)
                            )
                        )
                    )
                )
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_d")

    # Ambiguity:
    def test_amb_sentence_A1_p1(self):
        # Paraphrase: They should discuss the violence on TV
        # Original Sentence: They should discuss violence on TV

        parse_str = inspect.cleandoc("""
        (TP
            (NP (N They)) 
            (T should) 
            (VP 
                (V discuss) 
                (NP 
                    (N violence)
                    (PP 
                        (P on)
                        (N TV)
                    )
                )
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "amb_sentence_A1_p1")

    def test_amb_sentence_A1_p2(self):
        # Paraphrase: They should discuss the violence on TV
        # Original Sentence: They should discuss violence on TV

        parse_str = inspect.cleandoc("""
        (TP
            (NP 
                (N They)
            ) 
            (T should) 
            (VP 
                (V discuss)
                (NP (N violence))
                (PP 
                    (P on) 
                    (N TV)
                )
            ) 
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "amb_sentence_A1_p2")

    # Ambiguity:
    def test_amb_sentence_A1_3(self):
        sentence = "They should get on top of a TV and discuss violence"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP (N They)) 
            (T should) 
            (VP
                (VP 
                    (VB get) 
                    (PP 
                        (P on) 
                        (NP 
                            (NP (N top)) 
                            (PP 
                                (P of) 
                                (NP (D a) (N TV))
                            )
                        )
                    )
                ) 
                (Conj and) 
                (VP (VB discuss) (NP (N violence)))
            )
        ) """)

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "amb_sentence_A1_3")

    def test_gps6_sentence_b(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
        parse_str = inspect.cleandoc("""
        (TP
          (NP (D The) (AdjP (AdvP (Adv very)) (Adj stormy)) (N weather))
          (T has)
          (VP
            (V swept)
            (NP (D the) (N lawnchairs))
            (PP (P into) (NP (D the) (N lake)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    def test_gps6_sentence_c(self):
        sentence = "Scholars wonder if the library might contain the rare books"
        parse_str = inspect.cleandoc("""
        (TP
          (NP (N Scholars))
          (VP
            (V wonder)
            (CP
              (C if)
              (TP
                (NP (D the) (N library))
                (T might)
                (VP (V contain) (NP (D the) (AdjP (Adj rare)) (N books)))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

class Quiz2(unittest.TestCase):

    def test_p1_sentence_a_pre(self):

        sentence = "The hungry students from Boston craved chowder with clams"

        print(f"STANFORD: ********************************")
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        stn_tree = next(stanford_parser.raw_parse(sentence))

        nltk_tree.pretty_print(stn_tree)
        print(stn_tree)
        rules = stn_tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(stn_tree, "quiz2_P1_sa_stanford")

        print(f"\nPDX: ********************************")
        pdx_parser = Tree(parser=stanford_parser)
        pdx_tree = pdx_parser.parse_sentence(sentence, require_tense=True)

        nltk_tree.pretty_print(pdx_tree)
        print(pdx_tree)
        rules = stn_tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        pdx_parser.write_to_file(tree, "quiz2_P1_sa_pdx_pre")

    def test_p1_sentence_a(self):

        sentence = "The hungry students from Boston craved chowder with clams"

        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (NP 
                    (D The)
                    (AdjP (Adj hungry)) 
                    (N students)
                ) 
                (PP
                    (P from) 
                    (NP (N Boston))
                )
            )
            (T [+past])
            (VP 
                (V craved)
                (NP (N chowder)) 
                (PP (P with) (NP (N clams)))
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_P1_sa_pdx_post")

    def test_p1_sentence_a_para1(self):

        sentence = "The hungry students from Boston craved chowder with clams"

        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (NP 
                    (D The)
                    (AdjP (Adj hungry)) 
                    (N students)
                ) 
                (PP
                    (P from) 
                    (NP (N Boston))
                )
            )
            (T [+past])
            (VP 
                (V craved)
                (NP 
                    (N chowder)
                    (PP (P with) (NP (N clams)))    
                ) 
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_P1_sentenceA_para1")
    def test_p1_paraphrase_a1(self):

        sentence = "The hungry students from Boston craved clam chowder"

        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (NP 
                    (D The)
                    (AdjP (Adj hungry)) 
                    (N students)
                ) 
                (PP
                    (P from) 
                    (NP (N Boston))
                )
            )
            (T [+past])
            (VP 
                (V craved)
                (NP (NP (N clam)) (N chowder))
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "test_p1_paraphrase_a1")

    def test_p1_paraphrase_b2(self):

        sentence = "The happy leprechaun danced in Kilkenny and kicked a pot of gold that landed in Tipperary "

        parse_str = inspect.cleandoc("""
        (TP 
            (NP (D The) (AdjP (Adj happy)) (N leprechaun))
            (T [+past])
            (VP 
                (VP (V danced) (PP (P in) (NP (N Kilkenny)))) 
                (Conj and) 
                (VP 
                    (V kicked) 
                    (NP 
                        (NP (D a) (N pot)) (PP (P of) (NP (N gold))) 
                        (CP 
                            (C that) 
                            (TP 
                                (C ∅)
                                (T [+past])
                                (VP 
                                    (V landed) 
                                    (PP (P in) (NP (N Tipperary))))))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p1_paraphrase_b1")


    def test_p1_paraphrase_b2(self):

        sentence = "The happy leprechaun danced in Kilkenny and kicked a pot of gold that landed in Tipperary "

        parse_str = inspect.cleandoc("""
        (TP  
            (NP (D The) (AdjP (Adj happy)) (N leprechaun)) 
            (T [+past])
            (VP 
                (V kicked) 
                (NP (NP (D the) (N pot)) (PP (P of) (NP (N gold)))) 
                (PP (P from) (NP (N Kilkenny))) 
                (PP (P to) (NP (N Tipperary)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p1_paraphrase_b1")



    def test_p1_paraphrase_c1(self):

        sentence = "Jaya said with gusto that Thando sang the aria"

        parse_str = inspect.cleandoc("""
        (TP (NP (N Jaya)) (T [+past])(VP (V said) (PP (P with) (NP (N gusto))) (CP (C that) (TP (NP (N Thando)) (T [+past]) (VP (V sang) (NP (D the) (N aria)))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p1_paraphrase_c1")

    def test_p1_sentence_c(self):

        sentence = "Jamal said that Jazmyn sang the aria from La Bohème"

        parse_str = inspect.cleandoc("""
        (TP (NP (N Jamal)) (T [+past]) (VP (V said) (CP (C that) (TP (NP (N Jazmyn)) (T [+past]) (VP (V sang) (NP (D the) (N aria)) (PP (P from) (NP (N La Bohème))))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p1_sentence_d")

    def test_p2_sentence_old(self):

        sentence = "Hermione thought that Ron had seen the glowing patronus through the thick fog"

        parse_str = inspect.cleandoc("""
        (TP1 
            (NP1 (N1 Hermione)) 
            (T1 [+past])
            (VP1 
                (V1 thought) 
                (CP 
                    (C that) 
                    (TP2 
                        (NP2 (N2 Ron)) 
                        (T had) 
                        (VP2 
                            (V2 seen) 
                            (NP3 (D3 the) (AdjP1 (Adj1 glowing)) (N3 patronus)) 
                            (PP (P through) (NP3 (D3 the) (AdjP2 (Adj2 thick)) (N3 fog))))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p2_sentence_corrected")

    def test_p2_sentence_corrected(self):

        sentence = "Hermione thought that Ron had seen the glowing patronus through the thick fog"

        parse_str = inspect.cleandoc("""
        (TP1 
            (NP1 (N1 Hermione)) 
            (T1 [+past])
            (VP1 
                (V1 thought) 
                (CP 
                    (C that) 
                    (TP2 
                        (NP2 (N2 Ron)) 
                        (T had) 
                        (VP2 
                            (V2 seen) 
                            (NP3 (D3 the) (AdjP1 (Adj1 glowing)) (N3 patronus)) 
                            (PP (P through) (NP4 (D4 the) (AdjP2 (Adj2 thick)) (N4 fog))))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p2_sentence_corrected")

    def test_p3_tree(self):

        parse_str = inspect.cleandoc("""
        (R 
            (C (B)) 
            (D
                (F)
                (E (G) (H))
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p3_tree")

    def test_p4_sentence_4b(self):

        parse_str = inspect.cleandoc("""
        (TP 
            (VP 
                (V ’ibat)
                (PP 
                    (P xchi’uk)
                    (NP 
                        (N smalal)
                    )
                )
            ) 
            (NP
                (D li)
                (N Maruche)
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p4_sentence_b")

    def test_p4_sentence_4c(self):

        parse_str = inspect.cleandoc("""
        (TP 
            (VP 
                (V Pas)
            ) 
            (NP
                (D ti)
                (N ’eklixa’une)
            )
        )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p4_sentence_c")


    def test_p6_binding_theory(self):

        sentence = "People with disabilities report that they are seeing themselves more in books"

        parse_str = inspect.cleandoc("""
        (TP (NP (NP (N People)) (PP (P with) (NP (N disabilities)))) (T [-past]) (VP (V report) (CP (C that) (TP (NP (N they)) (T [-past]) (VP (V are) (VP (V seeing) (NP (N themselves)) (AdvP (Adv more)) (PP (P in) (NP (N books)))))))))""")

        # parse_str = inspect.cleandoc("""
        # (TP
        #     (NP
        #         (NP (N People))
        #         (PP
        #             (P with)
        #             (NP (N disabilities))
        #         )
        #     )
        #     (T [-past])
        #     (VP
        #         (V report)
        #         (CP
        #             (C that)
        #             (TP
        #                 (NP (N they))
        #                 (T [-past])
        #                 (VP
        #                     (V are)
        #                     (VP
        #                         (V seeing)
        #                         (NP (N themselves))
        #                         (AdvP (Adv more))
        #                         (PP (P in) (NP (N books)))
        #                     )
        #                 )
        #             )
        #         )
        #     )
        # )""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz2_p6_binding_theory")


class FunSentences(unittest.TestCase):

    def test_weird_01(self):
        sentence = "Is it weird how saying sentences backward create backward sentences saying how weird it is"
        expected_parse_str = inspect.cleandoc(f"""
          (TP
            (C {tree.EMPTY_SET})
            (VP
              (V Is)
              (TP
                (NP (N it))
                (AdjP (Adj weird))
                (CP
                  (C how)
                  (TP
                    (TP 
                      (C {tree.EMPTY_SET})
                      (VP (V saying) (NP (N sentences)))
                      (AdvP (Adv backward))
                    )
                    (VP
                      (V create)
                      (NP
                        (AdvP (Adv backward))
                        (N sentences)
                        (VP
                          (V saying)
                          (CP
                            (C how) 
                            (TP 
                              (NP 
                                (AdjP (Adj weird))
                                (N it)) 
                              (VP (V is))
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        """)

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=1, require_tense=False, debug=True)


        self.assertEqual(expected_tree, actual_tree)

    def test_weird_02(self):
        sentence = "Is it weird how saying sentences backward create backward sentences saying how weird it is"
        parse_str = inspect.cleandoc("""
        (TP (NP (D The) (N dog)) (T should) (VP (V put) (NP (D his) (AdjP (Adj squeaky)) (N toy)) (PP (P on) (NP (D the) (AdjP (Adj fuzzy)) (N rug)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "is_it_weird")

    def test_gps6_sentence_b(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
        parse_str = inspect.cleandoc("""
        (TP
          (NP (D The) (AdjP (AdvP (Adv very)) (Adj stormy)) (N weather))
          (T has)
          (VP
            (V swept)
            (NP (D the) (N lawnchairs))
            (PP (P into) (NP (D the) (N lake)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    def test_gps6_sentence_c(self):
        sentence = "Scholars wonder if the library might contain the rare books"
        parse_str = inspect.cleandoc("""
        (TP
          (NP (N Scholars))
          (VP
            (V wonder)
            (CP
              (C if)
              (TP
                (NP (D the) (N library))
                (T might)
                (VP (V contain) (NP (D the) (AdjP (Adj rare)) (N books)))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    #def test_gps6_rules_a(self):

    def test_quiz1_constit_sentence_a(self):
        sentence = "Jouri wrote a book in her spare time"
        parse_str = inspect.cleandoc("""
        (TP 
           (NP (N Jouri))
           (T [+past])
           (VP 
              (V wrote) 
              (NP (D a) (N book)) 
              (PP 
                 (P in) 
                 (NP 
                    (D her) 
                    (AdjP (Adj spare)) 
                    (N time))))) """)

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_a")

    def test_quiz1_constit_sentence_b(self):
        sentence = "The car in the tunnel stalled during rush hour"
        parse_str1 = inspect.cleandoc("""
        (TP 
            (NP 
                (D The) 
                (AdjP 
                    (AdvP (Adv very)) 
                    (Adj stormy)
                ) 
                (N weather)
            ) 
            (VP 
                (V has) 
                (VP 
                    (V swept)
                    (NP 
                        (D the) 
                        (N lawnchairs)
                    ) 
                    (PP 
                        (P into) 
                        (NP 
                            (D the) 
                            (N lake)
                        )
                    )
                )
            )
        )""")

        parse_str = inspect.cleandoc("""
        (TP 
            (NP (D The) (N car)) 
            (PP 
                (P in) 
                (NP (NP (D the) (N tunnel)) 
                (VP 
                    (V stalled) 
                    (PP (P during) (NP (N rush) (N hour)))))))""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_b")

    def test_quiz1_constit_sentence_c(self):
        sentence = "The neighbor yelled at the kids for no good reason"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP (D The) (N neighbor)) 
            (T [+past])
            (VP 
                (V yelled) 
                (PP (P at) (NP (D the) (N kids))) 
                (PP (P for) (NP (D no) (AdjP (Adj good)) (N reason))))) """)

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_c")

    def test_quiz1_constit_sentence_d(self):
        sentence = "The book on the shelf contains many illustrations in color"
        parse_str1 = inspect.cleandoc("""
        (TP 
            (NP 
                (D The) 
                (AdjP 
                    (AdvP (Adv very)) 
                    (Adj stormy)
                ) 
                (N weather)
            ) 
            (VP 
                (V has) 
                (VP 
                    (V swept)
                    (NP 
                        (D the) 
                        (N lawnchairs)
                    ) 
                    (PP 
                        (P into) 
                        (NP 
                            (D the) 
                            (N lake)
                        )
                    )
                )
            )
        )""")

        parse_str = inspect.cleandoc("""
        (TP 
            (NP 
                (NP (D The) (N book)) 
                (PP (P on) (NP (D the) (N shelf)))) 
            (VP 
                (V contains) 
                (NP 
                    (NP 
                        (AdjP (Adj many)) (N illustrations)) 
                    (PP (P in) (NP (N color))))))""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_b")

    # Ambiguity:
    def test_amb_sentence_A1_2(self):
        sentence = "They should get on top of a TV and discuss violence"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP (D There)) 
            (T should) 
            (VP 
                (V be) 
                (NP (NP (D a) (NP (N TV)) (N show)))
                (CP 
                    (C that) 
                    (TP 
                        (NP (N Ø))
                        (VP (V discusses) (NP (N violence)))
                    )
                )
            )
        )
        """)

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "amb_sentence_A1_2")

    # Ambiguity:
    def test_amb_sentence_A1_3(self):
        sentence = "They should get on top of a TV and discuss violence"
        parse_str = inspect.cleandoc("""
        (TP 
            (NP (N They)) 
            (T should) 
            (VP
                (VP 
                    (VB get) 
                    (PP 
                        (P on) 
                        (NP 
                            (NP (N top)) 
                            (PP 
                                (P of) 
                                (NP (D a) (N TV))
                            )
                        )
                    )
                ) 
                (Conj and) 
                (VP (VB discuss) (NP (N violence)))
            )
        ) """)

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "amb_sentence_A1_3")

    def test_gps6_sentence_b(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
        parse_str = inspect.cleandoc("""
        (TP
          (NP (D The) (AdjP (AdvP (Adv very)) (Adj stormy)) (N weather))
          (T has)
          (VP
            (V swept)
            (NP (D the) (N lawnchairs))
            (PP (P into) (NP (D the) (N lake)))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    def test_gps6_sentence_c(self):
        sentence = "Scholars wonder if the library might contain the rare books"
        parse_str = inspect.cleandoc("""
        (TP
          (NP (N Scholars))
          (VP
            (V wonder)
            (CP
              (C if)
              (TP
                (NP (D the) (N library))
                (T might)
                (VP (V contain) (NP (D the) (AdjP (Adj rare)) (N books)))))))""")

        tree = nltk_tree.fromstring(parse_str)

        print(tree)

        rules = tree.productions()

        rules = list(dict.fromkeys(rules))
        print("\nRules:")
        for r in rules:
            print(r)

        #Tree.pretty_productions(rules)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")


