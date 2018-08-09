import os
import csv
from glob import glob
from collections import Counter
from nltk.parse.corenlp import CoreNLPParser
""" Collecting names for both formats: all_names.csv and ccp_data.csv
Before you start this program, run the CoreNLP Server on terminal with this command:
java -mx4g -cp "stanford-corenlp-full-2018-02-27/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,ner
visit http:localhost:9000 for debugging purposes
"""


def get_entities(tagger_output):
    """ This function extracts names from the NER-tagged output string.

    Since the NER tagger does not tag full names automatically, we need to combine them.
    full_name collects all parts of a name: first, middle initial or name, and last.
    """
    full_name = []
    people = []
    for token, tag in tagger_output:
        if tag == 'PERSON':
            full_name.append(token)
        else:
            if full_name:
                people.append(full_name)
                full_name = []

    return ['%s' % ((' '.join([token for token in full_name])).title()) for full_name in people]


tagger = CoreNLPParser(tagtype='ner')

with open('ccp_people.csv', 'w', newline='') as csvfile:
    """ Collect the csv of all the names in the document
    ccp_people columns: Name, Year, Place, filename
    """
    newfile = csv.DictWriter(csvfile, fieldnames=['Person', 'Count', 'Year', 'Place', 'filename'],
                             quoting=csv.QUOTE_MINIMAL)
    newfile.writeheader()
    for f in glob(os.path.join("ccpminutes", '*.txt')):
        filename = f.split("\\")[1]
        year = filename.split(".")[0]
        place = filename.split(".")[1].split("-")[0]
        entities = Counter()
        with open(f, encoding='utf-8') as fin:
            for line in fin:
                if line.split():
                    try:
                        tagged_line = tagger.tag(line.split())
                        entities += Counter(get_entities(tagged_line))
                    except:
                        pass

        for name in entities.keys():
            newfile.writerow({'Person': name, 'Count': str(entities[name]), 'Year': year, 'Place': place,
                              'filename': filename})


with open('ccp_adjacency_list.csv', 'w', newline='') as csvfile2:
    """ Create the adjacency list for the bipartite graph
    ccp_people columns: Name, Year, Place, filename
    """
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

        newfile2.writerow([f.split("\\")[1]] + [name for name in entities.keys()])
