import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
hdr = pd.read_csv(dp['mcmexport'], encoding = 'latin-1', nrows = 0)
print((hdr.columns))

chunks = pd.read_csv(dp['mcmexport'], encoding = 'latin-1', dtype = str, low_memory = False, chunksize = 10**6)
# print(cdpmtt)

s = pd.read_csv(dp['msample'], encoding = 'latin-1',usecols = ['COSMIC_SAMPLE_ID','ETHNICITY','IS_ASIAN'], dtype = str, low_memory = False)

_chunk = 0
results = pd.DataFrame(columns = hdr.columns, dtype = str)
for chunk in chunks:
    # print(chunk.columns)
    result = chunk.merge(s).drop_duplicates()
    print(_chunk)
    # print(result)
    results = pd.concat([results, result])
    _chunk += 1
    if _chunk == 1: 
        results.to_csv(dp['ethcodmut'], encoding = 'latin-1', mode = 'w', index = False)
        results = pd.DataFrame(columns = hdr.columns, dtype = str)    
    else : 
        results.to_csv(dp['ethcodmut'], encoding = 'latin-1', mode = 'a', header = False, index = False)
        # print(results)
        results = pd.DataFrame(columns = hdr.columns, dtype = str)
# print(s.columns)
# print(s)
# epoint = cdpmtt.merge(s).drop_duplicates()
# print(epoint)
# print(epoint.ETHNICITY.unique())
# print(epoint.IS_ASIAN.unique())
# print(epoint[epoint.IS_ASIAN == '0'])
# epoint
