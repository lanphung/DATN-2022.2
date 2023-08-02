import pandas as pd
import numpy as np
import os
from paths import dpaths as dp
clsfct = pd.read_csv(dp['classification'], encoding = 'latin-1', dtype = str)
# print(clsfct)
""" classification.csv header
'COSMIC_PHENOTYPE_ID', 
'SITE_PRIMARY', 'SITE_SUBTYPE1', 'SITE_SUBTYPE2', 'SITE_SUBTYPE3',
'HISTOLOGY', 'HIST_SUBTYPE1', 'HIST_SUBTYPE2', 'HIST_SUBTYPE3',
'SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC', 'SITE_SUBTYPE3_COSMIC',
'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC', 'HIST_SUBTYPE3_COSMIC',
'NCI_CODE', 'EFO'   
"""
ctags = ['COSMIC_PHENOTYPE_ID', 'SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC', 'SITE_SUBTYPE3_COSMIC',
'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC', 'HIST_SUBTYPE3_COSMIC', 'NCI_CODE', 'EFO']
keywds = {
    'lung': ['lung'],
    'breast': ['breast'],
    'thyroid': ['thyroid'],
    'colorectal': ['large_intestine','colorectal','rectum','colon'],
    'hepatocellular': ['hepatocellular_carcinoma', 'hepatocellular', 'hepatocellular_hepatoma']
}
# print(keywds.values())
dclasses = {}
for key, values in keywds.items():
    dclasses[key] = clsfct.query(f" SITE_PRIMARY in {values} or SITE_SUBTYPE1 in {values} or SITE_SUBTYPE2 in {values} or SITE_SUBTYPE3 in {values} or HISTOLOGY in {values} or HIST_SUBTYPE1 in {values} ")
    dclasses[key]['CLASS'] = key
classes = pd.concat(dclasses.values(), axis = 0).drop_duplicates().reset_index(drop = True)
print(dclasses)
cnt = 0
for value in dclasses.values():
    cnt += len(value) 
print(cnt)
dclasses = {}
for key, values in keywds.items():
    dclasses[key] = clsfct.query(f" SITE_PRIMARY in {values} or SITE_SUBTYPE1 in {values} or SITE_SUBTYPE2 in {values} or SITE_SUBTYPE3 in {values} or HISTOLOGY in {values} or HIST_SUBTYPE1 in {values} ")[ctags].drop_duplicates()
    dclasses[key]['CLASS'] = key
classes = pd.concat(dclasses.values(), axis = 0).drop_duplicates().reset_index(drop = True)
# print(dclasses)
# print(len(classes['COSMIC_PHENOTYPE_ID'].unique()))
renamed_cols = ['COSMIC_PHENOTYPE_ID', 'PRIMARY_SITE', 'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2', 'HISTOLOGY_SUBTYPE_3', 'NCI_CODE', 'EFO', 'CLASS']
classes.columns = renamed_cols
print((classes.columns))
print(classes)
# COSO_classes.to_csv(dp['COSO_classifier'], index = False)
classes.to_csv(dp['classifier'], index = False)
classes['NCI_CODE'].drop_duplicates().to_csv(dp['nci'], encoding = 'latin-1', index = False)

# def printlen(classes):
#     for clss in classes:
#         print(f"số lượng kiểu hình bệnh thuộc lớp {clss['CLASS'].unique()}: {len(clss)}")
# printlen([lung_classes, breast_classes, thyroid_classes, colorectal_classes, hepatocellular_classes])