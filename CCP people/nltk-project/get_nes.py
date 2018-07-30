import os
import csv
from glob import glob
from collections import Counter
from nltk.parse.corenlp import CoreNLPParser
# before you start this program, run the CoreNLP Server on terminal with this command:
# java -mx4g -cp "stanford-corenlp-full-2018-02-27/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,ner
# visit http:localhost:9000 for debugging purposes

# Collect the csv of all the names in the document
# columns: Name, Year, Place, filename


def get_entities(tagger_output):
    current_entity = []
    ents = []
    for token, tag in tagger_output:
        if tag == 'PERSON':
            current_entity.append((token, tag))
        else:
            if current_entity:
                ents.append(current_entity)
                current_entity = []
    return ['%s_%s' % ((' '.join([tok for tok, tag in entity])).title(), entity[0][1]) for entity in ents]


tagger = CoreNLPParser(tagtype='ner')
# open a new csv file and write down the data
# with open('ccp_data.csv', 'w', newline='') as csvfile:
#     newfile = csv.DictWriter(csvfile, fieldnames=['Person', 'Count', 'Year', 'Place', 'filename'],
#                              quoting=csv.QUOTE_MINIMAL)
#     newfile.writeheader()
#     for f in glob(os.path.join("ccpminutes", '*.txt')):
#         # collect metadata
#         filename = f.split("\\")[1]
#         year = filename.split(".")[0]
#         place = filename.split(".")[1].split("-")[0] # e.g. NY-10, take NY
#         entities = Counter()
#         with open(f, encoding='utf-8') as fin:
#             for line in fin:
#                 if line.split():
#                     try:
#                         tagged_line = tagger.tag(line.split())
#                         entities += Counter(get_entities(tagged_line))
#                     except:
#                         pass
#
#         for name in entities.keys():
#             newfile.writerow({'Person': name, 'Count': str(entities[name]), 'Year': year, 'Place': place,
#                               'filename': filename})


with open('all_names.csv', 'w', newline='') as csvfile2:
    newfile2 = csv.writer(csvfile2, quoting=csv.QUOTE_MINIMAL)
    newfile2.writerow(['File', 'People'])
    for f in glob(os.path.join("ccpminutes", '*.txt')):
        entities = Counter()
        with open(f, encoding='utf-8') as fin:
            for line in fin:
                if line.split():
                    try:
                        tagged_line = tagger.tag(line.split())
                        entities += Counter(get_entities(tagged_line))
                    except:
                        pass

        newfile2.writerow([f.split("\\")[1]] + [name.split("_PERSON")[0] for name in entities.keys()])
