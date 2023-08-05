import pandas as pd
import os, csv
from paths import dpaths as dp, dyes_no as yn
import numpy as np
classes = ['lung','breast','thyroid','colorectal','hepatocellular']
results = pd.DataFrame()
data = pd.read_csv(dp['sup_codmut'], encoding = 'latin-1', dtype = str, usecols = ['GENE_SYMBOL', 'ID_INDIVIDUAL','CLASS'])
data['GENE_SYMBOL'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
for c in classes:
    print(f"----- start {c} -----")
    cd = data[data['CLASS']==c]
    print(cd.columns)
    print(cd)
    total = len(cd['ID_INDIVIDUAL'].unique())
    print(total)
    result = cd.drop_duplicates().groupby(['GENE_SYMBOL']).size().reset_index(name='freq').sort_values('freq', ascending = False).reset_index()
    num = np.array(result['freq'])
    print(num / total)
    result['ratio'] = pd.Series( num/ total)
    print(result)
    result['CLASS'] = c
#    result.to_csv(f'/media/data/thanhnb/COSMIC_individual_/out/freq/{c}.csv', index = False)
    results = pd.concat([results,result])
    print(f"----- end {c} -----")
print(results)
results.drop(columns = 'index').to_csv(dp['wgen'], index = False)
    