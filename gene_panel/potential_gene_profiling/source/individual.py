import pandas as pd
import os
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn


sp = pd.read_csv(dp['msample'], dtype = str, encoding = 'latin-1')
print(sp, sp.columns, sep = '\n')
print(sp[sp.IS_ASIAN == yn['yes']])
r1 = sp.drop_duplicates(subset=[
    'COSMIC_SAMPLE_ID', 'ID_INDIVIDUAL']).groupby(['ID_INDIVIDUAL']).size().reset_index(name='SAMPLES')
print(r1)
r2 = sp.drop_duplicates(subset=[
    'ID_TUMOUR', 'ID_INDIVIDUAL']).groupby(['ID_INDIVIDUAL']).size().reset_index(name='TUMOURS')
print(r2)
r3 = sp[['ID_INDIVIDUAL','ETHNICITY', 'GENDER', 'NAME', 'IS_ASIAN', 'CLASS']].drop_duplicates()
print(r3)
result = pd.merge(r3,r1).merge( r2).drop_duplicates()

print(result)
result.to_csv(dp['indiv'], index = False)