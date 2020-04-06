# from nltk.parse import ShiftReduceParser
# sr = ShiftReduceParser(grammar)
# sentence1 = 'the cat chased the dog'.split()
# sentence2 = 'the cat chased the dog on the rug'.split()
#
# for t in sr.parse(sentence1):
#     print(t)
#
# # (S (NP the (N cat)) (VP (V chased) (NP the (N dog))))

# import stanfordnlp
# #stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
# model_path = 'C:\\workspace_courses\\LING511\\tree_generator\\stanfordnlp_resources'
# nlp = stanfordnlp.Pipeline(models_dir=model_path)  # This sets up a default neural pipeline in English
# doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
# doc.sentences[0].print_dependencies()

#parser = nltk.parse.corenlp.CoreNLPParser()   (model_path='C:\\workspace_courses\\LING511\\tree_generator')
#parser = nltk.CoreNLPParser()

import os
from nltk.parse import stanford
from nltk.draw.tree import TreeView
from PIL import Image

# pip3 install Ghostscript
# Download and install Ghostscript:
# https://www.ghostscript.com/download/gsdnld.html
# Add ghostscript install directory bin folder to PATH environment variable
# On windows, for example, your ghostscript install directory bin folder might be:
#   C:\Program Files\gs\gs9.52
# Add that line to the path environment variable

os.environ['STANFORD_PARSER'] = 'C:\\workspace_courses\\LING511\\tree_generator'
os.environ['STANFORD_MODELS'] = 'C:\\workspace_courses\\LING511\\tree_generator'

parser = stanford.StanfordParser(model_path="C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz")
#sentences = parser.raw_parse_sents(("They quickly trampled the grass", "The ground above her shook as the buffalo went past"))
#sentences = parser.raw_parse_sents(("She dived into a hole in the ground in front of her", "The birds gave the other animals a warning cry"))

sentences = parser.raw_parse_sents(
    (
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
    )
)

print(sentences)

def save_as_png(canvas, filename):
    # save postscipt image
    canvas.postscript(file = filename + '.eps')
    # use PIL to convert to PNG
    img = Image.open(filename + '.ps')
    img.save(filename + '.png', 'png')

# Output trees to file
i = 0
for line in sentences:
    for tree in line:
        #sentence.draw()
        #t = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')
        i += 1
        #t = Tree(sentence)
        filename = f"tree_{i}"
        if os.path.exists(f"tree_{i}.ps"):
            os.remove(f"tree_{i}.ps")
        if os.path.exists(f"tree_{i}.jpg"):
            os.remove(f"tree_{i}.jpg")
        TreeView(tree)._cframe.print_to_file(f"{filename}.ps")
        #os.system(f"convert {filename}.ps {filename}.png")
        #save_as_png()
        im = Image.open(f"{filename}.ps")
        rgb_im = im.convert('RGB')
        rgb_im.save(f"{filename}.jpg")