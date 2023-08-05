import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
import concurrent.futures

chunks = pd.read_csv(dp['sup_codmut'], encoding = 'latin-1', dtype = str, low_memory = False, chunksize = 10**6)
sdf = pd.read_csv(dp['asample'], encoding = 'latin-1',usecols = ['COSMIC_SAMPLE_ID','ETHNICITY','ID_INDIVIDUAL'], dtype = str, low_memory = False)

res = pd.DataFrame()
for chunk in chunks:
    df = chunk.merge(sdf)
    res = pd.concat([res,df], axis = 0).reset_index(drop = True)
    print(res)
res.to_csv(dp['sup_acodmut'], encoding = 'latin-1', mode = 'w', index = False)
print(res)