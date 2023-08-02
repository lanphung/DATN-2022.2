import pandas as pd
import os
super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
df = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/classification.csv', encoding = 'latin-1', dtype = str, low_memory = False)
print(df)
""" classification.tsv header
'COSMIC_PHENOTYPE_ID', 
'SITE_PRIMARY', 'SITE_SUBTYPE1', 'SITE_SUBTYPE2', 'SITE_SUBTYPE3',
'HISTOLOGY', 'HIST_SUBTYPE1', 'HIST_SUBTYPE2', 'HIST_SUBTYPE3',
'SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC', 'SITE_SUBTYPE3_COSMIC',
'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC', 'HIST_SUBTYPE3_COSMIC',
'NCI_CODE', 'EFO'   
"""
cosmic_tags = ['COSMIC_PHENOTYPE_ID', 'SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC', 'SITE_SUBTYPE3_COSMIC',
'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC', 'HIST_SUBTYPE3_COSMIC']
relate_to_lung = ((df['SITE_PRIMARY'] == 'lung') 
    | (df['SITE_SUBTYPE1'] == 'lung') 
    | (df['SITE_SUBTYPE2'] == 'lung') 
    | (df['SITE_SUBTYPE3'] == 'lung'))
lung_classes = df[relate_to_lung][cosmic_tags].drop_duplicates()
lung_classes['CLASS'] = 'lung'
relate_to_breast = ((df['SITE_PRIMARY'] == 'breast') 
    | (df['SITE_SUBTYPE1'] == 'breast') 
    | (df['SITE_SUBTYPE2'] == 'breast') 
    | (df['SITE_SUBTYPE3'] == 'breast'))
breast_classes = df[relate_to_breast][cosmic_tags].drop_duplicates()
breast_classes['CLASS'] = 'breast'
relate_to_thyroid = ((df['SITE_PRIMARY'] == 'thyroid') 
    | (df['SITE_SUBTYPE1'] == 'thyroid') 
    | (df['SITE_SUBTYPE2'] == 'thyroid') 
    | (df['SITE_SUBTYPE3'] == 'thyroid'))
thyroid_classes = df[relate_to_thyroid][cosmic_tags].drop_duplicates()
thyroid_classes['CLASS'] = 'thyroid'
colorectal_tags = ['large_intestine','colorectal','rectum','colon']
relate_to_colorectal = ((df['SITE_PRIMARY'].isin(colorectal_tags)) 
    | (df['SITE_SUBTYPE1'].isin(colorectal_tags)) 
    | (df['SITE_SUBTYPE2'].isin(colorectal_tags)) 
    | (df['SITE_SUBTYPE3'].isin(colorectal_tags)))
colorectal_classes = df[relate_to_colorectal][cosmic_tags].drop_duplicates()
colorectal_classes['CLASS'] = 'colorectal'
hepato_tags = ['hepatocellular_carcinoma', 'hepatocellular', 'hepatocellular_hepatoma']
relate_to_hepatocellular = ((df['HIST_SUBTYPE1'].isin(hepato_tags))
    | (df['SITE_PRIMARY'] == 'hepatoma'))
hepatocellular_classes = df[relate_to_hepatocellular][cosmic_tags].drop_duplicates()
hepatocellular_classes['CLASS'] = 'hepatocellular'
# print(df[relate_to_hepatocellular])

COSO_targeted_classes = pd.concat([lung_classes, breast_classes, thyroid_classes, colorectal_classes, hepatocellular_classes], axis = 0).reset_index(drop = True)
targeted_classes = pd.DataFrame(COSO_targeted_classes)
targeted_classes['COSMIC_PHENOTYPE_ID'] = targeted_classes['COSMIC_PHENOTYPE_ID'].str.replace('COSO','')
COSO_targeted_classes.to_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/COSO_classifier.csv', index = False)
targeted_classes.to_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/classifier.csv', index = False)
print(targeted_classes)
# def printlen(classes):
#     for clss in classes:
#         print(f"số lượng kiểu hình bệnh thuộc lớp {clss['CLASS'].unique()}: {len(clss)}")
# printlen([lung_classes, breast_classes, thyroid_classes, colorectal_classes, hepatocellular_classes])