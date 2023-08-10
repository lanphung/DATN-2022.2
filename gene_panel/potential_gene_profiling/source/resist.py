import pandas as pd
import os
import numpy as np
# from asian_ethnicity import asian_ethnicity as ae
np.seterr(all="ignore")
pd.options.mode.chained_assignment = None  # default='warn'
from paths import dpaths as dp, dyes_no as yn
# from classifier import COSO_targeted_classes
resist = pd.read_table(dp['resist'], encoding = 'latin-1', dtype = str)
print(resist.columns)
old_names = ['Gene Name', 'Transcript',
         'Sample ID', 'ID_STUDY']
new_names = ['GENE_SYMBOL', 'TRANSCRIPT_ACCESSION',
         'COSMIC_SAMPLE_ID', 'COSMIC_STUDY_ID']
resist.rename(columns = dict(zip(old_names, new_names)), inplace = True)
resist.columns = map(lambda x: str(x).upper().replace(' ','_'), resist.columns)    

sample = pd.read_csv(dp['msample'], encoding = 'latin-1',usecols = ['COSMIC_SAMPLE_ID','ETHNICITY','IS_ASIAN','COSMIC_PHENOTYPE_ID', 'CLASS', 'NAME'], dtype = str, low_memory = False)

mresist = resist.merge(sample).drop_duplicates()
mresist.loc[mresist['CLASS']=='hepatocellular', 'CLASS']='hepatocellular_carcinoma'
mresist.loc[mresist['CLASS']=='colorectal', 'CLASS']='large_intestine'
mresist.rename(columns = {'GENE_SYMBOL': 'Gene Name', 'CLASS':'disease_type','PRIMARY_TISSUE':'Primary Tissue','HISTOLOGY':'Histology','DRUG_NAME':'Drug Name','PUBMED_ID':'Pubmed Id','AA_MUTATION':'AA Mutation','CDS_MUTATION':'CDS Mutation'}, inplace = True)
print(mresist.columns)
mresist.to_csv(dp['mresist'],mode = 'w', encoding = 'latin-1', index = False)
