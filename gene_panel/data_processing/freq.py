import pandas as pd
import os, csv
from paths import dpaths as dp, dyes_no as yn
import numpy as np
classes = ['lung','breast','thyroid','colorectal','hepatocellular']
s = pd.read_csv(dp['msample'], encoding = 'latin-1', dtype = str)
s = s[s.IS_ASIAN == '1'][['COSMIC_SAMPLE_ID','ID_INDIVIDUAL']]
results = pd.DataFrame()
print(s.columns)
for c in classes:
    print(f"----- start {c} -----")
    cd = pd.read_csv(dp[c]+'/asiancdpmut.csv', encoding = 'latin-1', dtype = str, usecols = ['GENE_SYMBOL', 'COSMIC_SAMPLE_ID'])
    cd['GENE_SYMBOL'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True) 
    print(cd.columns)
    print(cd)
    r = cd.merge(s).drop_duplicates()
    total = len(r.ID_INDIVIDUAL.unique())
    print(total)
    print(r)
    result = r.drop_duplicates(subset=['GENE_SYMBOL', 'ID_INDIVIDUAL']).groupby(['GENE_SYMBOL']).size().reset_index(name='Number').sort_values('Number', ascending = False).reset_index()
    num = np.array(result['Number'])
    print(num / total)
    result['Frequency'] = pd.Series( num/ total)
    print(result)
    result['CLASS'] = c
    result.to_csv(f'/media/data/thanhnb/COSMIC_individual_/out/freq/{c}.csv', index = False)
    results = pd.concat([results,result])
    print(f"----- end {c} -----")
print(results)
results.drop(columns = 'index').to_csv(f'/media/data/thanhnb/COSMIC_individual_/out/freq/asian.csv', index = False)
    