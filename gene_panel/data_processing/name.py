import pandas as pd
from paths import dpaths as dp

clsfr = pd.read_csv(dp['classifier'], encoding = 'latin-1', dtype = str)
name = pd.read_csv(dp['name'], encoding = 'latin-1', dtype = str)
clsfr = clsfr.merge(name)
clsfr.to_csv(dp['classifier'], encoding = 'latin-1', index = False)
print(clsfr.columns)
print(clsfr)