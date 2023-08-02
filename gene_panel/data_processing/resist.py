import pandas as pd
import os
# from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
# from classifier import COSO_targeted_classes
resist = pd.read_table(dp['resist'], encoding = 'latin-1', dtype = str)
print(resist.columns)
old_names = ['Gene Name', 'Transcript',
         'Sample ID', 'ID_STUDY']
        # 'Genome-wide screen', 'Mutation CDS', 'Mutation AA',
new_names = ['GENE_SYMBOL', 'TRANSCRIPT_ACCESSION',
         'COSMIC_SAMPLE_ID', 'COSMIC_STUDY_ID']
resist.rename(columns = dict(zip(old_names, new_names)), inplace = True)
resist.columns = map(lambda x: str(x).upper().replace(' ','_'), resist.columns)    

sample = pd.read_csv(dp['msample'], encoding = 'latin-1',usecols = ['COSMIC_SAMPLE_ID','ETHNICITY','IS_ASIAN','COSMIC_PHENOTYPE_ID', 'CLASS', 'NAME'], dtype = str, low_memory = False)

print(sample.columns)
# print(clsfr.columns)
print(resist.columns)
mresist = resist.drop(columns = ['PRIMARY_TISSUE', 'TISSUE_SUBTYPE_1', 'TISSUE_SUBTYPE_2', 
'HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2', 'SAMPLE_TYPE', 'SOMATIC_STATUS', 'CGP_STUDY']).merge(sample).drop_duplicates()
print(mresist.columns)
print(mresist)
mresist.to_csv(dp['mresist'],mode = 'w', encoding = 'latin-1', index = False)
classes = ['lung','breast','thyroid','colorectal','hepatocellular']

for c in classes:
    print(f'---------start {c}----------')
    data = mresist[mresist.CLASS == c]
    data['GENE_SYMBOL'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
    print(data)
    print(data['COSMIC_SAMPLE_ID'].nunique())
#     print(len(data[['ETHNICITY']].drop_duplicates()))
#     print(data[['ETHNICITY']].groupby(['ETHNICITY']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(len(data[['GENE_SYMBOL']].drop_duplicates()))
    print(data[['GENE_SYMBOL']].groupby(['GENE_SYMBOL']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(len(data[['GENE_SYMBOL', 'CDS_MUTATION']].drop_duplicates()))
    print(data[['GENE_SYMBOL', 'CDS_MUTATION']].groupby(['GENE_SYMBOL', 'CDS_MUTATION']).size().reset_index(name = 'Number').sort_values('Number', ascending = False))
    print(f'---------end {c}----------')
# print(action)
# maction = action.merge(clsfr).drop_duplicates()
# maction.to_csv(dp['maction'],mode = 'w', encoding = 'latin-1', index = False)
