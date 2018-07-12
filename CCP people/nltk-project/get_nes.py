import os
import csv
from glob import glob
from collections import Counter
from nltk.parse.corenlp import CoreNLPParser, CoreNLPServer

# Collect the csv of all the names in the document
# columns: Name, Year, Place, filename
jar = 'stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1.jar'
models = 'stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1-models.jar'

# you can also access the parser by running this on your terminal:
# java -mx4g -cp "stanford-corenlp-full-2018-02-27/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
# and then accessing this on your web browser:
# https://localhost:9000/

with CoreNLPServer(path_to_jar=jar, path_to_models_jar=models, java_options=['-mx4g']) as server:
    tagger = CoreNLPParser(tagtype='ner')

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
        entities = Counter()
        for f in glob(os.path.join("ccpminutes", '*txt')):
            # collect metadata
            filename = f.split("\\")[1]
            year = filename.split(".")[0]
            place = filename.split(".")[1].split("-")[0] # e.g. NY-10, take NY
            with open(f, encoding='utf-8') as fin:
                for line in fin:
                    if line.split():
                        try:
                            tagged_line = tagger.tag(line.split())
                            # print(tagged_line)
                            entities += Counter(get_entities(tagged_line))
                        except:
                            pass
            for name in entities.keys():
                # store names into new row
                newfile.writerow({'Person': name, 'Count': str(entities[name]), 'Year': year, 'Place': place,
                                  'filename': filename})
