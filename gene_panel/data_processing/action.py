import pandas as pd
import os
# from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
# from classifier import COSO_targeted_classes
clsfr = pd.read_csv(dp['classifier'], encoding = 'latin-1', dtype = str, usecols = ['COSMIC_PHENOTYPE_ID', 'CLASS', 'NAME'])
action = pd.read_table(dp['action'], encoding = 'latin-1', dtype = str)
# action = action.drop()
action.rename(columns = {'CLASSIFICATION_ID': 'COSMIC_PHENOTYPE_ID', 'GENE':'GENE_SYMBOL'}, inplace = True)
print(clsfr.columns)
print(action.columns)
print(action)
maction = action.merge(clsfr).drop_duplicates()
maction.to_csv(dp['maction'],mode = 'w', encoding = 'latin-1', index = False)
print(maction)
classes = ['lung','breast','thyroid','colorectal','hepatocellular']
for c in classes:
    print(f'---------start {c}----------')
    data = maction[maction.CLASS == c]
    # data['GENE_SYMBOL'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
    print(data.TRIAL_ID.nunique())
#     print(data['COSMIC_SAMPLE_ID'].nunique())
# #     print(len(data[['ETHNICITY']].drop_duplicates()))
# #     print(data[['ETHNICITY']].groupby(['ETHNICITY']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
#     print(len(data[['GENE_SYMBOL']].drop_duplicates()))
#     print(data[['GENE_SYMBOL']].groupby(['GENE_SYMBOL']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
#     print(len(data[['GENE_SYMBOL', 'CDS_MUTATION']].drop_duplicates()))
#     print(data[['GENE_SYMBOL', 'CDS_MUTATION']].groupby(['GENE_SYMBOL', 'CDS_MUTATION']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(f'---------end {c}----------')