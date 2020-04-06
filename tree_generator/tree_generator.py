import os
from nltk.parse import stanford
from nltk.draw.tree import TreeView
from PIL import Image

os.environ['STANFORD_PARSER'] = 'C:\\workspace_courses\\LING511\\tree_generator'
os.environ['STANFORD_MODELS'] = 'C:\\workspace_courses\\LING511\\tree_generator'
model_path = "C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz"

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


def write_to_file(tree, filename):
    if os.path.exists(f"{filename}.ps"):
        os.remove(f"{filename}.ps")
    if os.path.exists(f"{filename}.png"):
        os.remove(f"{filename}.png")
    TreeView(tree)._cframe.print_to_file(f"{filename}.ps")

    with Image.open(f"{filename}.ps") as img:
        img.load(scale=4)
        img.save(f"{filename}.png")

    try:
        os.remove(f"{filename}.ps")
    except OSError as e:  # name the Exception `e`
        print("Failed with:", e.strerror)  # look what it says


def parse_trees(sentences):
    # Output trees to file
    parser = stanford.StanfordParser(model_path=model_path)
    trees = parser.raw_parse_sents(sentences)

    i = 0
    for line in trees:
        for tree in line:
            i += 1
            filename = f"tree_{i}"
            write_to_file(tree, filename)


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

# sentences = ["He thought that other places must be more interesting"]

parse_trees(sentences)

