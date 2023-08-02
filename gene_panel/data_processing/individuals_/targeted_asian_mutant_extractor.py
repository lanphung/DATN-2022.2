import pandas as pd
import os
super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
chunks = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_mutation.csv', encoding = 'latin-1', dtype = str, low_memory = False, chunksize = 10**6)
sdf = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_sample.csv', encoding = 'latin-1',
                    dtype = str, low_memory = False, usecols = ['sample_id','ethnicity','id_individual']).drop_duplicates()
dir = '/media/data/thanhnb/COSMIC_individual_/out'
os.makedirs(dir, exist_ok=True)
res = pd.DataFrame()
for chunk in chunks:
    df = chunk.merge(sdf, left_on = 'ID_sample', right_on = 'sample_id').drop('sample_id', axis = 1)
    res = pd.concat([res,df], axis = 0).reset_index(drop = True)
    print(res)

res.to_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_mutant.csv',mode = 'w', index = False)
print(res)