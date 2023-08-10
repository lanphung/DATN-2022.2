import pandas as pd
import os
# from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
# from classifier import COSO_targeted_classes
clsfr = pd.read_csv(dp['classifier'], encoding = 'latin-1', dtype = str, usecols = ['COSMIC_PHENOTYPE_ID', 'CLASS'])
action = pd.read_table(dp['action'], encoding = 'latin-1', dtype = str)
action.rename(columns = {'CLASSIFICATION_ID': 'COSMIC_PHENOTYPE_ID', 'GENE':'GENE_SYMBOL'}, inplace = True)
maction = action.merge(clsfr).drop_duplicates()
maction.loc[maction['CLASS']=='hepatocellular', 'CLASS']='hepatocellular_carcinoma'
maction.loc[maction['CLASS']=='colorectal', 'CLASS']='large_intestine'
maction.rename(columns = {'GENE_SYMBOL': 'GENE', 'CLASS':'disease_type'}, inplace = True)
maction.to_csv(dp['maction'],mode = 'w', encoding = 'latin-1', index = False)
