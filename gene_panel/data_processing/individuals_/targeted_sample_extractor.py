import pandas as pd
import os
from asian_ethnicity import asian_ethnicity as a_e
# from classifier import targeted_classes
targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/classifier.csv', dtype = str, low_memory = False)
super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
df = pd.read_table('/media/data3/biodataset/COSMIC/v98/GRCh37/CosmicSample.tsv', encoding = 'latin-1', dtype = str, low_memory = False)
df = df.merge(targeted_classes[['COSMIC_PHENOTYPE_ID', 'CLASS']], left_on = 'cosmic_phenotype_id', right_on = 'COSMIC_PHENOTYPE_ID').drop_duplicates()
dir = '/media/data/thanhnb/COSMIC_individual_/out/individuals_'
os.makedirs(dir, exist_ok=True)
df.to_csv(dir+'/targeted_sample.csv',mode = 'w', index = False)
print(df)
df = df[df['ethnicity'].isin(a_e)]
df.to_csv(dir+'/targeted_asian_sample.csv',mode = 'w', index = False)
print(df)