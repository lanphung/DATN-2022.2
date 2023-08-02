import pandas as pd
import os, csv, re

# from classifier import targeted_classes

super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
out = root+'/out'
data = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_mutant.csv', usecols = ['Gene name', 'CLASS'], dtype = str)

data['Gene name'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
genes = data.drop_duplicates()
print(re.sub(r'_ENST\d+', '', 'TET2_ENST00000380013'))
# with open(out+'/gen_set.csv', mode = 'w') as f:
#     f.write(str(set(data))) 
genes.rename(columns = {'Gene name': 'LIST'}, inplace = True)
genes['CLASS'].replace('colorectal', 'large_intestine', inplace = True)
genes.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/asian_gen_set.csv', mode = 'w', index = False)
print(genes['LIST'].nunique())
data2 = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_mutation.csv', usecols = ['Gene name', 'CLASS'], dtype = str)
print(data2)
data2['Gene name'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
print(data2)
genes2 = data2.drop_duplicates()
print(genes2)

print(re.sub(r'_ENST\d+', '', 'TET2_ENST00000380013'))
# with open(out+'/gen_set.csv', mode = 'w') as f:
#     f.write(str(set(data))) 
genes2.rename(columns = {'Gene name': 'LIST'}, inplace = True)
print(genes2['LIST'].nunique())
genes2['CLASS'].replace('colorectal', 'large_intestine', inplace = True)
genes2.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/gen_set.csv', mode = 'w', index = False)