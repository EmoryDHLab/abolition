import pandas as pd

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
