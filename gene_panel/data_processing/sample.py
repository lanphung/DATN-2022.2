import pandas as pd
import os
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn

clsfr = pd.read_csv(dp['classifier'], encoding = 'latin-1', dtype = str)
sp = pd.read_table(dp['csample'], encoding = 'latin-1', dtype = str)
print(sp)
# print(sp)
# print(len(sp.sample_id.unique()))

sp.columns = map(lambda x: str(x).upper(), sp.columns)
sp.rename(columns = {'SAMPLE_ID': 'COSMIC_SAMPLE_ID'}, inplace = True)
sp.drop(columns = ['PRIMARY_SITE', 'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2', 'HISTOLOGY_SUBTYPE_3','NCI_CODE'], inplace = True)

# print(len(sp.ETHNICITY.unique()))
# print(sp.groupby('ETHNICITY').size().reset_index(name = 'Number').sort_values('Number', ascending = False))
sp.COSMIC_PHENOTYPE_ID = 'COSO' + sp.COSMIC_PHENOTYPE_ID
sp = sp.merge(clsfr[['COSMIC_PHENOTYPE_ID', 'CLASS', 'NAME']]).drop_duplicates()
# print(sp)
tags = ['breast', 'colorectal', 'hepatocellular', 'lung', 'thyroid']
for tag in tags:
       print(sp[sp['CLASS'] == tag])
sp['IS_ASIAN'] = yn['no']
sp.loc[sp['ETHNICITY'].isin(ae), 'IS_ASIAN'] = yn['yes']
# print(sp)
sp.to_csv(dp['msample'],mode = 'w', encoding = 'latin-1', index = False)
asp = (sp[sp.IS_ASIAN == yn['yes']])
for tag in tags:
       print(asp[asp['CLASS'] == tag])
# print(sp.columns)
# print(sp)
# print(sp[sp['IS_ASIAN'] == yn['yes']])

"""
Index(['COSMIC_SAMPLE_ID', 'SAMPLE_NAME', 'ID_TUMOUR', 'ID_INDIVIDUAL',
       'THERAPY_RELATIONSHIP', 'SAMPLE_DIFFERENTIATOR',
       'MUTATION_ALLELE_SPECIFICATION', 'MSI', 'AVERAGE_PLOIDY',
       'WHOLE_GENOME_SCREEN', 'WHOLE_EXOME_SCREEN', 'SAMPLE_REMARK',
       'DRUG_RESPONSE', 'GRADE', 'AGE_AT_TUMOUR_RECURRENCE', 'STAGE',
       'CYTOGENETICS', 'METASTATIC_SITE', 'TUMOUR_SOURCE', 'TUMOUR_REMARK',
       'AGE', 'ETHNICITY', 'ENVIRONMENTAL_VARIABLES', 'GERMLINE_MUTATION',
       'THERAPY', 'FAMILY', 'NORMAL_TISSUE_TESTED', 'GENDER',
       'INDIVIDUAL_REMARK', 'SAMPLE_TYPE', 'COSMIC_PHENOTYPE_ID'],
      dtype='object')


       COSMIC_SAMPLE_ID SAMPLE_NAME ID_TUMOUR ID_INDIVIDUAL  ... COSMIC_PHENOTYPE_ID       CLASS                                               NAME IS_ASIAN
0                686999      E17038    615159        596198  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        0
1                700943      S21968    628164        609203  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
2                701342      S22550    628516        609555  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        0
3                877185       E7873    796400        778913  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        0
4                982981      982981    898700        879837  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
...                 ...         ...       ...           ...  ...                 ...         ...                                                ...      ...
602543          1093856     1093856   1008562        984267  ...       COSO111686078  colorectal  Mucosal Melanoma of the Digestive System (Code...        1
602544          1803421     1803421   1705110       1636384  ...       COSO299710779        lung  Combined Lung Small Cell Carcinoma and Lung Ad...        0
602545          1803422     1803422   1705110       1636384  ...       COSO299710779        lung  Combined Lung Small Cell Carcinoma and Lung Ad...        0
602546          2348826     2348826   2213311       2068002  ...        COSO52755657        lung        Lung Atypical Carcinoid Tumor (Code C45551)        0
602547          1939619     1939619   1826543       1738979  ...       COSO339018850      breast                      Dysplastic Nevus (Code C3694)        0

[602548 rows x 34 columns]


       COSMIC_SAMPLE_ID SAMPLE_NAME ID_TUMOUR ID_INDIVIDUAL  ... COSMIC_PHENOTYPE_ID       CLASS                                               NAME IS_ASIAN
1                700943      S21968    628164        609203  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
4                982981      982981    898700        879837  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
5                700929      S21955    628150        609189  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
7                708696      S29493    634793        615832  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
12               708779      S29569    634874        615913  ...        COSO29914830        lung          Lung Squamous Cell Carcinoma (Code C3493)        1
...                 ...         ...       ...           ...  ...                 ...         ...                                                ...      ...
602490          2923142      AD1418   2776529       2611498  ...      COSO1002921832        lung              Lung Squamous Dysplasia (Code C84971)        1
602503          2862375     2862375   2717561       2553801  ...       COSO300110621        lung           Lung Pleomorphic Carcinoma (Code C45542)        1
602504          2862379     2862379   2717565       2553805  ...       COSO300110621        lung           Lung Pleomorphic Carcinoma (Code C45542)        1
602530          2862087     2862087   2717289       2553530  ...        COSO30016622        lung             Lung Giant Cell Carcinoma (Code C4452)        1
602543          1093856     1093856   1008562        984267  ...       COSO111686078  colorectal  Mucosal Melanoma of the Digestive System (Code...        1

[115261 rows x 34 columns]
"""