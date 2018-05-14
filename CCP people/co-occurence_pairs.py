import csv
import pandas as pd
import os
from collections import Counter
from nltk.tag.stanford import CoreNLPNERTagger
from glob import glob

# to see the results of the NER tagger
# first run the command:
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# afterwards, run this script

ner_tagger = CoreNLPNERTagger()


# get all the names and its attached tags
def get_entities(tagger_output):
    current_entity = []
    ents = []
    for token, tag in tagger_output:
        if tag == 'PERSON':
            current_entity.append((token, tag))
        else:
            # accounts for appending "first" and "last" names
            if current_entity:
                ents.append(current_entity)
                current_entity = []
    if current_entity:
        ents.append(current_entity)

    return ['%s_%s' % ((' '.join([tok for tok, tag in entity])).title(), entity[0][1]) for entity in ents]


# write down the document and its names per row
with open('all_names.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, lineterminator='\n')
    for f in glob(os.path.join("ccpminutes", '*txt')):
        with open(f, encoding='utf-8') as fin:
            entities = Counter()
            for line in fin:
                if line.split():
                    try:
                        tagged_line = ner_tagger.tag(line.split())
                        entities += Counter(get_entities(tagged_line))
                    except:
                        pass
        filename = f.split('\\')[1]
        writer.writerow([filename] + [name.split('_')[0] for name in entities.keys()])


# chunk and concatenate the large file so that it can be read faster
reader = pd.read_csv('co-occurrence_pairs_counted.csv', chunksize=10000, iterator=True, index_col=0)
co_occurrences = pd.concat([x for x in reader])

# take out all the dupes
dupes = []
for i, row in co_occurrences.iterrows():
    combo2 = co_occurrences[(co_occurrences.name1 == row.name2) & (co_occurrences.name2 == row.name1)]
    if (not combo2.empty) and (i not in dupes):
        co_occurrences.loc[i, 'co_occurrence'] += combo2.co_occurrence.values.astype(int)[0]
        dupes.append(combo2.index.astype(int)[0])
    if i % 100000 == 0:
        print("Current row: " + str(i))
        print("Size of dupe list " + str(len(dupes)))

co_occurrences = co_occurrences.drop(co_occurrences.index[dupes]).reset_index(drop=True)
co_occurrences.to_csv('co-occurrences_pairs_no_dupes.csv')
