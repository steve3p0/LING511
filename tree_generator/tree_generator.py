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

import nltk
import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = 'C:\\workspace_courses\\LING511\\tree_generator'
os.environ['STANFORD_MODELS'] = 'C:\\workspace_courses\\LING511\\tree_generator'

parser = stanford.StanfordParser(model_path="C:\\workspace_courses\\LING511\\tree_generator\\englishPCFG.ser.gz")
#parser = nltk.parse.corenlp.CoreNLPParser()   (model_path='C:\\workspace_courses\\LING511\\tree_generator')
#parser = nltk.CoreNLPParser()
sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
print(sentences)

# GUI
for line in sentences:
    for sentence in line:
        sentence.draw()