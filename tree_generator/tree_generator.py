import os
from nltk.parse import stanford
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

os.environ['STANFORD_PARSER'] = 'C:\\workspace_courses\\LING511\\tree_generator'
os.environ['STANFORD_MODELS'] = 'C:\\workspace_courses\\LING511\\tree_generator'
model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"


class TreeBuilder:
    def __init__(self, parser):
        self.parser = parser

    @staticmethod
    def tree_to_string(tree):
        s = str(tree)
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

    def parse_sentence(self, sentence):
        # fromstring
        #:type remove_empty_top_bracketing: bool
        tree = next(self.parser.raw_parse(sentence))
        return tree

    def parse_sentences(self, sentences):
        i = 0
        for s in sentences:
            i += 1
            filename = f"tree_{i}"
            tree = self.parse_sentence(s)
            tree_str = self.tree_to_string(tree)
            print(tree_str)
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
    tree_builder = TreeBuilder(parser)
    tree_builder.parse_sentences(sentences)

