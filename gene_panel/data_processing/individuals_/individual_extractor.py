import pandas as pd
import os

super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)

sdf = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_sample.csv', encoding = 'latin-1', dtype = str, low_memory = False)
mdf = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_mutant.csv', encoding = 'latin-1', dtype = str, low_memory = False)

print(len(sdf), len(mdf))
dir = '/media/data/thanhnb/COSMIC_individual_/cosmic_individuals'
os.makedirs(dir, exist_ok=True)

sampling = sdf.sort_values(['CLASS','ethnicity', 'id_individual']).reset_index(drop=True)
print(sampling.groupby(['CLASS']).agg(Number = ('id_individual', 'nunique')))
samples = dict(sampling.groupby(['CLASS','ethnicity', 'id_individual']).size())
s_begin = 0
for key, value in samples.items():
    # /media/data/thanhnb/MyProgram/cosmic_individuals/thyroid/_Turkish/_1681046
    sam_dir = dir+f'/{key[0]}/_{key[1]}/_{key[2]}'
    # print(sam_dir)
    os.makedirs(sam_dir, exist_ok= True)
    s_end = s_begin + value
    sresult = sampling.iloc[s_begin:s_end]
    sresult.to_csv(sam_dir+f'/_{key[2]}_sample_features.csv', mode = 'w', index = False)
    s_begin = s_end


mutanted = mdf.sort_values(['CLASS','ethnicity', 'id_individual']).reset_index(drop=True)
print(mutanted.groupby(['CLASS']).size())
variants = dict(mutanted.groupby(['CLASS','ethnicity', 'id_individual']).size())
v_begin = 0
for key, value in variants.items():
    # /media/data/thanhnb/MyProgram/cosmic_individuals/thyroid/_Turkish/_1681046
    var_dir = dir+f'/{key[0]}/_{key[1]}/_{key[2]}'
    # print(var_dir)
    os.makedirs(var_dir, exist_ok= True)
    v_end = v_begin + value
    vresult = mutanted.iloc[v_begin:v_end]
    vresult.to_csv(var_dir+f'/_{key[2]}_variants.csv', mode = 'w', index = False)
    v_begin = v_end
