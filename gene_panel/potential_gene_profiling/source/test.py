import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as ae

from paths import dpaths as dp, dyes_no as yn

classes = ['lung','breast','thyroid','colorectal','hepatocellular']
data = pd.read_csv(dp['msample'], encoding = 'latin-1', dtype = str)
print(dp['output']+'sample_name.csv')
data['SAMPLE_NAME'].drop_duplicates().to_csv(dp['output']+'sample_name.csv')
# print(chunk.columns)
exit()
for c in classes:
    print(f'---------start {c}----------')
    data = pd.read_csv(dp[c]+'/asiancdpmut.csv', encoding = 'latin-1', dtype = str)
    data['GENE_SYMBOL'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
    print(data)
    print(data['COSMIC_SAMPLE_ID'].nunique())
    print(len(data[['ETHNICITY']].drop_duplicates()))
    print(data[['ETHNICITY']].groupby(['ETHNICITY']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(len(data[['GENE_SYMBOL']].drop_duplicates()))
    print(data[['GENE_SYMBOL']].groupby(['GENE_SYMBOL']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(data[['GENE_SYMBOL', 'MUTATION_CDS']].drop_duplicates())
    print(data[['GENE_SYMBOL', 'MUTATION_CDS']].groupby(['GENE_SYMBOL', 'MUTATION_CDS']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(f'---------end {c}----------')
# print(result)
