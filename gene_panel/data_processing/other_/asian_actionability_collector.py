import pandas as pd
import os
# from classifier import COSO_targeted_classes
COSO_targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/COSO_classifier.csv')

super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
print(root+'/out/other_/targeted_asian_mutant.csv')
# act_df = pd.read_table('/media/data3/biodataset/COSMIC/v98/ActionabilityData.tsv', encoding = 'latin-1', dtype = str, low_memory = False)
# # print(len(df))
# # df.fillna('null', inplace = True)
# # print(df)
# # print(len(df[["TRIAL_ID", 'GENE', 'GENOMIC_MUTATION_ID', 'FUSION_ID', 'DRUG_COMBINATION','CLASSIFICATION_ID']].drop_duplicates()))

# df2 = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_mutant.csv', encoding = 'latin-1', usecols = ['GENOMIC_MUTATION_ID', 'ID_sample'], dtype = str, low_memory = False)
# df2['GENOMIC_MUTATION_ID'] = df2['GENOMIC_MUTATION_ID'].str.replace('COSV','', regex = False)
# df = act_df.dropna(subset = ['GENOMIC_MUTATION_ID'])
# muts = df2.dropna().drop_duplicates().groupby(['GENOMIC_MUTATION_ID']).size().to_frame('Size')
# print(muts)
# def count_freq(ids):
#     count = 0
#     for id in ids:
#         try:
#             # print(muts.loc[id].Size)
#             count += muts.loc[id].Size
#         except KeyError: pass
#     return count
        
# result = [x.split(' + ') for x in df['GENOMIC_MUTATION_ID']]
# freq = [count_freq(x) for x in result]
# df['ASIAN_FREQUENCY'] = freq
# res = df[df['ASIAN_FREQUENCY'] != 0].sort_values('ASIAN_FREQUENCY', ascending = False)

# print(res)
# res.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/asian_action.csv', mode = 'w', index = False)
# res = df.sort_values('ASIAN_FREQUENCY', ascending = False)
# res.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/_action.csv', mode = 'w', index = False)
# cr = pd.merge(act_df, COSO_targeted_classes, how = 'left', left_on = 'CLASSIFICATION_ID', right_on = 'COSMIC_PHENOTYPE_ID')
# qr = pd.merge(left = cr, right = res,how = 'left')
# qr = qr.drop_duplicates().reset_index(drop=True)
# qr = qr.sort_values('ASIAN_FREQUENCY', ascending = False)
# qr.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/outer_action.csv', mode = 'w', index = False)

data1 = pd.read_table('/media/data3/biodataset/COSMIC/v98/CosmicResistanceMutations.tsv', dtype = str)
data2 = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/resistance_/cosmic_world_5_cancers_resistance.csv', dtype = str)
# print(data1.columns, data2.columns)
resist = pd.merge(left = data1, right = data2,how = 'left')
resist.fillna(value = {'CLASS':'other'}, inplace = True)

resist.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/resist_.csv')
print(resist)
