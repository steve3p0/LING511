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

    # tree.write_to_file(expected_tree, "tree_expected_XX")
    # tree.write_to_file(actual_tree, "tree_expected_XX")

    if debug:
        print("\n#########################################################################################")
        print(f"Test Sentence {testid}:\n {sentence}:")

        # Write output to .png file
        # tree.write_to_file(expected_tree, f"tree_expected_{testid}")
        # tree.write_to_file(actual_tree, f"tree_actual_{testid}")

        print(f"{testid}) EXPECTED: ********************************")
        nltk_tree.pretty_print(expected_tree)
        print(f"{testid}) ACTUAL: ********************************")
        nltk_tree.pretty_print(actual_tree)

        print(f"{testid}) EXPECTED: ********************************")
        print(f"Expected String: \n{str(expected_tree)}\n")
        print(f"{testid}) ACTUAL: ********************************")
        print(f"Actual String: \n{actual_tree_str}\n")

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


# 10TAD5 Isn't properly setup yet
class TestTenTreesADay5(unittest.TestCase):

    def test_10TAD4_01(self):
        sentence = "The buffalo had always lived on the grassy plains"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 1, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_02(self):
        sentence = "The buffalo longed for adventure"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 2, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_03(self):
        #sentence = "He wanted to explore the wide, wide world"
        sentence = "He wanted to explore the wide wide world"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 3, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_04(self):
        sentence = "The mouse woke the buffalo early one day"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_05(self):
        sentence = "The mouse told the buffalo that there were places far away"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_06(self):
        sentence = "The mouse’s stories were very interesting"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_07(self):
        sentence = "The buffalo decided to travel to new places"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_08(self):
        sentence = "He trotted eagerly away from his herd"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_09(self):
        sentence = "He soon came to a river"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD4_10(self):
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


class TestTenTAD_07(unittest.TestCase):

    def test_get_verb_tense(self):
        input_label = "VBD"
        expect_tense = "past"
        actual_tense = Tree.get_verb_tense(input_label)

        self.assertEqual(expect_tense, actual_tense)

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
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str,
                                                               testid=2, require_tense=True, debug=True)
        self.assertEqual(expected_tree, actual_tree)

    def test_10TAD07_03(self):
        sentence = "The river was flowing too fast for him"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 4, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_04(self):
        sentence = "Her options were very limited"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 5, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_05(self):
        sentence = "She saw a large branch on the river bank"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 6, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_06(self):
        sentence = "She swiftly grabbed the branch with her teeth"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 7, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_07(self):
        sentence = "She tossed the branch into the river"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 8, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_08(self):
        sentence = "She then yelled for him to swim to it"
        expected_parse_str = inspect.cleandoc("""
        (TP(NP (D The) (N buffalo))(VP (V longed) (PP (P for) (NP (N adventure)))))""")

        expected_tree, actual_tree = get_expected_actual_trees(sentence, expected_parse_str, 9, True)
        self.assertEqual(actual_tree, expected_tree)

    def test_10TAD07_09(self):
        sentence = "The buffalo swam to the branch"
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

    def test_10TAD07_10(self):
        sentence = "He wished that he had opposable thumbs so he could grab the branch"
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

class Quiz1(unittest.TestCase):

    def test_gps6_sentence_a(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
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
                (D The) 
                (AdjP 
                    (AdvP (Adv very)) 
                    (Adj stormy)
                ) 
                (N weather)
            ) 
            (T has)
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
        )""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sa")

    def test_gps6_sentence_b(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
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
                (D The) 
                (AdjP 
                    (AdvP (Adv very)) 
                    (Adj stormy)
                ) 
                (N weather)
            ) 
            (T has)
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
        )""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

    def test_gps6_sentence_c(self):
        sentence = "The dog should put his squeaky toy on the fuzzy rug "
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
            (NP (N Scholars)) 
            (VP 
                (V wonder) 
                (CP 
                    (C if) 
                    (TP 
                        (NP (D the) (N library)) 
                        (T might) 
                        (VP 
                            (V contain) 
                            (NP (D the) (AdjP (Adj rare)) (N books)))))))""")

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_gps6_sb")

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
            (NP (D The) (N neighbor)) 
            (VP 
                (V yelled) 
                (PP (P at) (NP (D the) (N kids))) 
                (PP (P for) (NP (D no) (AdjP (Adj good)) (N reason))))) """)

        tree = nltk_tree.fromstring(parse_str)
        print(tree)
        stanford_parser = stanford.StanfordParser(model_path=model_path)
        pdx_parser = Tree(parser=stanford_parser)
        pdx_parser.write_to_file(tree, "quiz1_constituency_sentence_b")


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



