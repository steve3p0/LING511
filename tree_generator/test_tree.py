import nose
from unittest import TestCase
from tree import Tree
from nltk.parse import stanford

model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"


class TestTree(TestCase):
    def test_10TAD_2(self):
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

    def test_tree_to_string(self):
        self.fail()

    def test_write_to_file(self):
        self.fail()

    def test_parse_sentence(self):
        self.fail()

    def test_parse_sentences(self):
        self.fail()
