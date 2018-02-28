import os
import csv
from glob import glob
from collections import Counter
from nltk.tag.stanford import CoreNLPNERTagger
# before you begin this program, run the command line
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000


# Collect the csv of all the names in the document
# Format of each row: Name, Year, Place, filename

tagger = CoreNLPNERTagger()


# get all the names and its attached tags
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
    if current_entity:
        ents.append(current_entity)

    return ['%s_%s' % ((' '.join([tok for tok, tag in entity])).title(), entity[0][1]) for entity in ents]


# open a new csv file and write down the data
with open('ccp_data.csv', 'w', newline='') as csvfile:
    newfile = csv.DictWriter(csvfile, fieldnames=['Person', 'Count', 'Year', 'Place', 'filename'],
                             quoting=csv.QUOTE_MINIMAL)
    newfile.writeheader()
    for f in glob(os.path.join("ccpminutes", '*txt')):
        counter = Counter()
        # collect metadata
        filename = f.split("\\")[1]
        year = filename.split(".")[0]
        place = filename.split(".")[1].split("-")[0] # e.g. NY-10, take NY
        with open(f, encoding='utf-8') as fin:
            entities = Counter()
            for line in fin:
                if line.split():
                    try:
                        tagged_line = tagger.tag(line.split())
                        entities += Counter(get_entities(tagged_line))
                    except:
                        pass

        for name in counter.keys():
            # store names into new file
            newfile.writerow({'Person': name, 'Count': str(counter[name]), 'Year': year, 'Place': place,
                              'filename': filename})

