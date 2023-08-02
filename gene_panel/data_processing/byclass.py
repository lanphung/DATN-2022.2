import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
hdr = pd.read_csv(dp['ethcodmut'], encoding = 'latin-1', nrows = 0)
print(hdr)
chunks = pd.read_csv(dp['ethcodmut'], encoding = 'latin-1', dtype = str, low_memory = False, chunksize = 5*10**5)
# print(cdpmtt)
_chunk = 0
results = pd.DataFrame(columns = hdr.columns, dtype = str)
classes = ['lung','breast','thyroid','colorectal','hepatocellular']
for c in classes:
    hdr.to_csv(dp[c]+'/codingpointmutation.csv', encoding = 'latin-1', mode = 'w', index = False)
    hdr.to_csv(dp[c]+'/asiancdpmut.csv', encoding = 'latin-1', mode = 'w', index = False)
for chunk in chunks:
    # print(chunk.columns)

    for c in classes:
        result = chunk[chunk.CLASS == c]
        result.to_csv(dp[c]+'/codingpointmutation.csv', encoding = 'latin-1', mode = 'a', header = False,index = False)
        result[result.IS_ASIAN == yn['yes']].to_csv(dp[c]+'/asiancdpmut.csv', encoding = 'latin-1', mode = 'a', header = False,index = False)
    # print(result)
