import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as ae
from paths import dpaths as dp, dyes_no as yn
import concurrent.futures
# from classifier import targeted_classes
uses = ['COSMIC_PHENOTYPE_ID', 'PRIMARY_SITE', 'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2', 'HISTOLOGY_SUBTYPE_3', 'CLASS', 'NAME']
clsfr = pd.read_csv(dp['classifier'], encoding = 'latin-1', dtype = str, low_memory = False, usecols = uses)
# clsfr.to_csv(dp['mcmexport'], mode = 'a', index = False)
# exit()
sz = 10**7
hdr = pd.read_table(dp['cmexport'], encoding = 'latin-1', nrows = 0)
old_names = ['Gene name', 'Accession Number',
        'Sample name', 'ID_sample', 'ID_STUDY']
        # 'Genome-wide screen', 'Mutation CDS', 'Mutation AA',
new_names = ['GENE_SYMBOL', 'TRANSCRIPT_ACCESSION',
        'SAMPLE_NAME', 'COSMIC_SAMPLE_ID', 'COSMIC_STUDY_ID']
hdr.rename(columns = dict(zip(old_names, new_names)), inplace = True)
hdr.columns = map(lambda x: str(x).upper().replace(' ','_'), hdr.columns)    

print(hdr.columns)
# chunks = pd.read_table(dp['cmexport'], encoding = 'latin-1', dtype = str, low_memory = False, names = hdr.columns, nrows = 100, skiprows = 1)
# print(chunks)

chunks = pd.read_table(dp['cmexport'], encoding = 'latin-1', dtype = str,names = hdr.columns, low_memory = False, chunksize = 10**6)

_chunk = 0
results = pd.DataFrame(columns = hdr.columns, dtype = str)
for chunk in chunks:
    # print(chunk.columns)      
    result = chunk.merge(clsfr).drop_duplicates()
    print(_chunk)
    # print(result)
    results = pd.concat([results, result]).drop(columns = ['ID_TUMOUR', 
            'PRIMARY_SITE', 'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
            'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2', 'HISTOLOGY_SUBTYPE_3'])
    _chunk += 1
    if _chunk == 10: 
        results.to_csv(dp['mcmexport'], encoding = 'latin-1', mode = 'w', index = False)
        results = pd.DataFrame(columns = hdr.columns, dtype = str)    
    elif (_chunk)%10 == 0: 
        results.to_csv(dp['mcmexport'], encoding = 'latin-1', mode = 'a', header = False, index = False)
        print(results)
        results = pd.DataFrame(columns = hdr.columns, dtype = str)

if not _chunk%10 == 0: 
        results.to_csv(dp['mcmexport'], encoding = 'latin-1', mode = 'a', header = False, index = False)
        print(results)
        results = pd.DataFrame(columns = hdr.columns, dtype = str)


"""
49459828
Index(['GENE_NAME', 'ACCESSION_NUMBER', 'GENE_CDS_LENGTH', 'HGNC_ID',
       'SAMPLE_NAME', 'ID_SAMPLE', 'ID_TUMOUR', 'PRIMARY_SITE',
       'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
       'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2',
       'HISTOLOGY_SUBTYPE_3', 'GENOME-WIDE_SCREEN', 'GENOMIC_MUTATION_ID',
       'LEGACY_MUTATION_ID', 'MUTATION_ID', 'MUTATION_CDS', 'MUTATION_AA',
       'MUTATION_DESCRIPTION', 'MUTATION_ZYGOSITY', 'LOH', 'GRCH',
       'MUTATION_GENOME_POSITION', 'MUTATION_STRAND', 'RESISTANCE_MUTATION',
       'MUTATION_SOMATIC_STATUS', 'PUBMED_PMID', 'ID_STUDY', 'SAMPLE_TYPE',
       'TUMOUR_ORIGIN', 'AGE', 'HGVSP', 'HGVSC', 'HGVSG'],
      dtype='object')
0
                       GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO           CLASS                                               NAME
0       ADAMTS13_ENST00000371910  ENST00000371910.1             672    1366  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
1                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
2                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
3                          MRPS9  ENST00000258455.3            1191   14501  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
4          PGBD1_ENST00000259883  ENST00000259883.3            2430   19398  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
...                          ...                ...             ...     ...  ...      ...                                   ...             ...                                                ...
272090   RPS6KA4_ENST00000528057  ENST00000528057.1            2298   10433  ...    C4247  http://www.ebi.ac.uk/efo/EFO_1001972          breast  Undifferentiated Pleomorphic Sarcoma (Code C4247)
272091     EPHA3_ENST00000452448  ENST00000452448.2            1620    3387  ...    C3758  http://www.ebi.ac.uk/efo/EFO_0000762  hepatocellular                Hepatocellular Adenoma (Code C3758)
272092     DACH1_ENST00000359684  ENST00000359684.2            2283    2663  ...    C5665                                   NaN            lung  Atypical Adenomatous Lung Hyperplasia (Code C5...
272093     DACH1_ENST00000359684  ENST00000359684.2            2283    2663  ...    C5665                                   NaN            lung  Atypical Adenomatous Lung Hyperplasia (Code C5...
272094    INPP4B_ENST00000308502  ENST00000308502.4            2775    6075  ...   C53553  http://www.ebi.ac.uk/efo/EFO_1000143          breast  Breast Carcinoma by Gene Expression Profile (C...

[272095 rows x 42 columns]
1
                    GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO       CLASS                                               NAME
0                       MYO10  ENST00000513610.1            6177    7593  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
1                       MYO10  ENST00000513610.1            6177    7593  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
2       QRFPR_ENST00000334383  ENST00000334383.5             777   15565  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
3                       KRT77  ENST00000341809.3            1737   20411  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
4                       KRT77  ENST00000341809.3            1737   20411  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
...                       ...                ...             ...     ...  ...      ...                                   ...         ...                                                ...
276822                   BCL6  ENST00000406870.2            2121    1001  ...    C4247  http://www.ebi.ac.uk/efo/EFO_1001972        lung  Undifferentiated Pleomorphic Sarcoma (Code C4247)
276823  FGFR1_ENST00000341462  ENST00000341462.5            2469    3688  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
276824   TCF3_ENST00000344749  ENST00000344749.5            1956   11633  ...    C4684                                   NaN      breast  Nasal Type Extranodal NK/T-Cell Lymphoma (Code...
276825  PTPRS_ENST00000372412  ENST00000372412.4            5850    9681  ...    C4684                                   NaN      breast  Nasal Type Extranodal NK/T-Cell Lymphoma (Code...
276826   TCF3_ENST00000344749  ENST00000344749.5            1956   11633  ...   C96156                                   NaN  colorectal  Colorectal Neuroendocrine Carcinoma (Code C96156)

[276827 rows x 42 columns]
2
                     GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                           EFO       CLASS                                           NAME
0         NFIA_ENST00000371191  ENST00000371191.1            1599    7784  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
1        EPHA6_ENST00000470610  ENST00000470610.2            1644   19296  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
2                        NLGN1  ENST00000457714.1            2472   14291  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
3                        NLGN1  ENST00000457714.1            2472   14291  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
4        EPHA6_ENST00000470610  ENST00000470610.2            1644   19296  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
...                        ...                ...             ...     ...  ...      ...                                           ...         ...                                            ...
284541  PIK3R1_ENST00000336483  ENST00000336483.5            1365    8979  ...   C40395                                           NaN      breast  Breast Malignant Myoepithelioma (Code C40395)
284542    NBAS_ENST00000441750  ENST00000441750.1            6756   15625  ...    C2926          http://www.ebi.ac.uk/efo/EFO_0003060        lung     Lung Non-Small Cell Carcinoma (Code C2926)
284543   PKHD1_ENST00000340994  ENST00000340994.4           10191    9016  ...    C2965          http://www.ebi.ac.uk/efo/EFO_0000384  colorectal                     Crohn Disease (Code C2965)
284544   FGFR2_ENST00000478859  ENST00000478859.1            1782    3689  ...    C2918  http://purl.obolibrary.org/obo/MONDO_0004379      breast           Female Breast Carcinoma (Code C2918)
284545   FGFR2_ENST00000478859  ENST00000478859.1            1782    3689  ...    C4088  http://purl.obolibrary.org/obo/MONDO_0008093      breast                   Epidermal Nevus (Code C4088)

[284546 rows x 42 columns]
3
                   GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                     EFO   CLASS                                               NAME
0       WWOX_ENST00000406884  ENST00000406884.2             705   12799  ...    C4017    http://www.ebi.ac.uk/efo/EFO_0006318  breast               Breast Ductal Carcinoma (Code C4017)
1                      MINK1  ENST00000355280.6            3999   17565  ...    C4017    http://www.ebi.ac.uk/efo/EFO_0006318  breast               Breast Ductal Carcinoma (Code C4017)
2                      PDE8A  ENST00000310298.4            2490    8793  ...    C4017    http://www.ebi.ac.uk/efo/EFO_0006318  breast               Breast Ductal Carcinoma (Code C4017)
3                      PDE8A  ENST00000310298.4            2490    8793  ...    C4017    http://www.ebi.ac.uk/efo/EFO_0006318  breast               Breast Ductal Carcinoma (Code C4017)
4                      PDE8A  ENST00000310298.4            2490    8793  ...    C4017    http://www.ebi.ac.uk/efo/EFO_0006318  breast               Breast Ductal Carcinoma (Code C4017)
...                      ...                ...             ...     ...  ...      ...                                     ...     ...                                                ...
280127  AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...    C3863    http://www.ebi.ac.uk/efo/EFO_1000306  breast          Breast Intraductal Papilloma (Code C3863)
280128  AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...  C187405                                     NaN  breast  Invasive Breast Lobular Carcinoma with Extrace...
280129  AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...   C85032  http://www.orpha.net/ORDO/Orphanet_744    lung                     Proteus Syndrome (Code C85032)
280130  AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...    C4455                                     NaN    lung                          Lung Adenoma (Code C4455)
280131  MLH1_ENST00000435176  ENST00000435176.1            1977    7127  ...   C53553    http://www.ebi.ac.uk/efo/EFO_1000143  breast  Breast Carcinoma by Gene Expression Profile (C...

[280132 rows x 42 columns]
                       GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                     EFO   CLASS                                               NAME
0       ADAMTS13_ENST00000371910  ENST00000371910.1             672    1366  ...    C3512    http://www.ebi.ac.uk/efo/EFO_0000571    lung                   Lung Adenocarcinoma (Code C3512)
1                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512    http://www.ebi.ac.uk/efo/EFO_0000571    lung                   Lung Adenocarcinoma (Code C3512)
2                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512    http://www.ebi.ac.uk/efo/EFO_0000571    lung                   Lung Adenocarcinoma (Code C3512)
3                          MRPS9  ENST00000258455.3            1191   14501  ...    C3512    http://www.ebi.ac.uk/efo/EFO_0000571    lung                   Lung Adenocarcinoma (Code C3512)
4          PGBD1_ENST00000259883  ENST00000259883.3            2430   19398  ...    C3512    http://www.ebi.ac.uk/efo/EFO_0000571    lung                   Lung Adenocarcinoma (Code C3512)
...                          ...                ...             ...     ...  ...      ...                                     ...     ...                                                ...
280127      AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...    C3863    http://www.ebi.ac.uk/efo/EFO_1000306  breast          Breast Intraductal Papilloma (Code C3863)
280128      AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...  C187405                                     NaN  breast  Invasive Breast Lobular Carcinoma with Extrace...
280129      AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...   C85032  http://www.orpha.net/ORDO/Orphanet_744    lung                     Proteus Syndrome (Code C85032)
280130      AKT1_ENST00000555528  ENST00000555528.1            1443     391  ...    C4455                                     NaN    lung                          Lung Adenoma (Code C4455)
280131      MLH1_ENST00000435176  ENST00000435176.1            1977    7127  ...   C53553    http://www.ebi.ac.uk/efo/EFO_1000143  breast  Breast Carcinoma by Gene Expression Profile (C...

[1113600 rows x 42 columns]
thanhnb@quangnh:~/BASE/source$ python3 codingpointmutation.py 
Index(['GENE_NAME', 'ACCESSION_NUMBER', 'GENE_CDS_LENGTH', 'HGNC_ID',
       'SAMPLE_NAME', 'ID_SAMPLE', 'ID_TUMOUR', 'PRIMARY_SITE',
       'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
       'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2',
       'HISTOLOGY_SUBTYPE_3', 'GENOME-WIDE_SCREEN', 'GENOMIC_MUTATION_ID',
       'LEGACY_MUTATION_ID', 'MUTATION_ID', 'MUTATION_CDS', 'MUTATION_AA',
       'MUTATION_DESCRIPTION', 'MUTATION_ZYGOSITY', 'LOH', 'GRCH',
       'MUTATION_GENOME_POSITION', 'MUTATION_STRAND', 'RESISTANCE_MUTATION',
       'MUTATION_SOMATIC_STATUS', 'PUBMED_PMID', 'ID_STUDY', 'SAMPLE_TYPE',
       'TUMOUR_ORIGIN', 'AGE', 'HGVSP', 'HGVSC', 'HGVSG'],
      dtype='object')
0
Traceback (most recent call last):
  File "/media/data/thanhnb/BASE/source/codingpointmutation.py", line 32, in <module>
    results = pd.concat([results, result])
NameError: name 'results' is not defined. Did you mean: 'result'?
thanhnb@quangnh:~/BASE/source$ python3 codingpointmutation.py 
Index(['GENE_NAME', 'ACCESSION_NUMBER', 'GENE_CDS_LENGTH', 'HGNC_ID',
       'SAMPLE_NAME', 'ID_SAMPLE', 'ID_TUMOUR', 'PRIMARY_SITE',
       'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
       'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2',
       'HISTOLOGY_SUBTYPE_3', 'GENOME-WIDE_SCREEN', 'GENOMIC_MUTATION_ID',
       'LEGACY_MUTATION_ID', 'MUTATION_ID', 'MUTATION_CDS', 'MUTATION_AA',
       'MUTATION_DESCRIPTION', 'MUTATION_ZYGOSITY', 'LOH', 'GRCH',
       'MUTATION_GENOME_POSITION', 'MUTATION_STRAND', 'RESISTANCE_MUTATION',
       'MUTATION_SOMATIC_STATUS', 'PUBMED_PMID', 'ID_STUDY', 'SAMPLE_TYPE',
       'TUMOUR_ORIGIN', 'AGE', 'HGVSP', 'HGVSC', 'HGVSG'],
      dtype='object')
0
                       GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO           CLASS                                               NAME
0       ADAMTS13_ENST00000371910  ENST00000371910.1             672    1366  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
1                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
2                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
3                          MRPS9  ENST00000258455.3            1191   14501  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
4          PGBD1_ENST00000259883  ENST00000259883.3            2430   19398  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571            lung                   Lung Adenocarcinoma (Code C3512)
...                          ...                ...             ...     ...  ...      ...                                   ...             ...                                                ...
272090   RPS6KA4_ENST00000528057  ENST00000528057.1            2298   10433  ...    C4247  http://www.ebi.ac.uk/efo/EFO_1001972          breast  Undifferentiated Pleomorphic Sarcoma (Code C4247)
272091     EPHA3_ENST00000452448  ENST00000452448.2            1620    3387  ...    C3758  http://www.ebi.ac.uk/efo/EFO_0000762  hepatocellular                Hepatocellular Adenoma (Code C3758)
272092     DACH1_ENST00000359684  ENST00000359684.2            2283    2663  ...    C5665                                   NaN            lung  Atypical Adenomatous Lung Hyperplasia (Code C5...
272093     DACH1_ENST00000359684  ENST00000359684.2            2283    2663  ...    C5665                                   NaN            lung  Atypical Adenomatous Lung Hyperplasia (Code C5...
272094    INPP4B_ENST00000308502  ENST00000308502.4            2775    6075  ...   C53553  http://www.ebi.ac.uk/efo/EFO_1000143          breast  Breast Carcinoma by Gene Expression Profile (C...

[272095 rows x 42 columns]
1
                    GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO       CLASS                                               NAME
0                       MYO10  ENST00000513610.1            6177    7593  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
1                       MYO10  ENST00000513610.1            6177    7593  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
2       QRFPR_ENST00000334383  ENST00000334383.5             777   15565  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
3                       KRT77  ENST00000341809.3            1737   20411  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
4                       KRT77  ENST00000341809.3            1737   20411  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung                   Lung Adenocarcinoma (Code C3512)
...                       ...                ...             ...     ...  ...      ...                                   ...         ...                                                ...
276822                   BCL6  ENST00000406870.2            2121    1001  ...    C4247  http://www.ebi.ac.uk/efo/EFO_1001972        lung  Undifferentiated Pleomorphic Sarcoma (Code C4247)
276823  FGFR1_ENST00000341462  ENST00000341462.5            2469    3688  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
276824   TCF3_ENST00000344749  ENST00000344749.5            1956   11633  ...    C4684                                   NaN      breast  Nasal Type Extranodal NK/T-Cell Lymphoma (Code...
276825  PTPRS_ENST00000372412  ENST00000372412.4            5850    9681  ...    C4684                                   NaN      breast  Nasal Type Extranodal NK/T-Cell Lymphoma (Code...
276826   TCF3_ENST00000344749  ENST00000344749.5            1956   11633  ...   C96156                                   NaN  colorectal  Colorectal Neuroendocrine Carcinoma (Code C96156)

[276827 rows x 42 columns]
2
                     GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                           EFO       CLASS                                           NAME
0         NFIA_ENST00000371191  ENST00000371191.1            1599    7784  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
1        EPHA6_ENST00000470610  ENST00000470610.2            1644   19296  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
2                        NLGN1  ENST00000457714.1            2472   14291  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
3                        NLGN1  ENST00000457714.1            2472   14291  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
4        EPHA6_ENST00000470610  ENST00000470610.2            1644   19296  ...   C53556          http://www.ebi.ac.uk/efo/EFO_1000294      breast   HER2-Positive Breast Carcinoma (Code C53556)
...                        ...                ...             ...     ...  ...      ...                                           ...         ...                                            ...
284541  PIK3R1_ENST00000336483  ENST00000336483.5            1365    8979  ...   C40395                                           NaN      breast  Breast Malignant Myoepithelioma (Code C40395)
284542    NBAS_ENST00000441750  ENST00000441750.1            6756   15625  ...    C2926          http://www.ebi.ac.uk/efo/EFO_0003060        lung     Lung Non-Small Cell Carcinoma (Code C2926)
284543   PKHD1_ENST00000340994  ENST00000340994.4           10191    9016  ...    C2965          http://www.ebi.ac.uk/efo/EFO_0000384  colorectal                     Crohn Disease (Code C2965)
284544   FGFR2_ENST00000478859  ENST00000478859.1            1782    3689  ...    C2918  http://purl.obolibrary.org/obo/MONDO_0004379      breast           Female Breast Carcinoma (Code C2918)
284545   FGFR2_ENST00000478859  ENST00000478859.1            1782    3689  ...    C4088  http://purl.obolibrary.org/obo/MONDO_0008093      breast                   Epidermal Nevus (Code C4088)

[284546 rows x 42 columns]
3
^Z
[9]+  Stopped                 python3 codingpointmutation.py
thanhnb@quangnh:~/BASE/source$ python3 codingpointmutation.py 
Index(['GENE_NAME', 'ACCESSION_NUMBER', 'GENE_CDS_LENGTH', 'HGNC_ID',
       'SAMPLE_NAME', 'ID_SAMPLE', 'ID_TUMOUR', 'PRIMARY_SITE',
       'SITE_SUBTYPE_1', 'SITE_SUBTYPE_2', 'SITE_SUBTYPE_3',
       'PRIMARY_HISTOLOGY', 'HISTOLOGY_SUBTYPE_1', 'HISTOLOGY_SUBTYPE_2',
       'HISTOLOGY_SUBTYPE_3', 'GENOME-WIDE_SCREEN', 'GENOMIC_MUTATION_ID',
       'LEGACY_MUTATION_ID', 'MUTATION_ID', 'MUTATION_CDS', 'MUTATION_AA',
       'MUTATION_DESCRIPTION', 'MUTATION_ZYGOSITY', 'LOH', 'GRCH',
       'MUTATION_GENOME_POSITION', 'MUTATION_STRAND', 'RESISTANCE_MUTATION',
       'MUTATION_SOMATIC_STATUS', 'PUBMED_PMID', 'ID_STUDY', 'SAMPLE_TYPE',
       'TUMOUR_ORIGIN', 'AGE', 'HGVSP', 'HGVSC', 'HGVSG'],
      dtype='object')
0
1
2
3
4
5
6
7
8
9
                       GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO       CLASS                                        NAME
0       ADAMTS13_ENST00000371910  ENST00000371910.1             672    1366  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung            Lung Adenocarcinoma (Code C3512)
1                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung            Lung Adenocarcinoma (Code C3512)
2                          OPRL1  ENST00000349451.3            1113    8155  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung            Lung Adenocarcinoma (Code C3512)
3                          MRPS9  ENST00000258455.3            1191   14501  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung            Lung Adenocarcinoma (Code C3512)
4          PGBD1_ENST00000259883  ENST00000259883.3            2430   19398  ...    C3512  http://www.ebi.ac.uk/efo/EFO_0000571        lung            Lung Adenocarcinoma (Code C3512)
...                          ...                ...             ...     ...  ...      ...                                   ...         ...                                         ...
281678                    CTNNB1  ENST00000349496.5            2346    2514  ...    C7041                                   NaN  colorectal          Colon Tubular Adenoma (Code C7041)
281679                    CTNNB1  ENST00000349496.5            2346    2514  ...    C7041                                   NaN  colorectal          Colon Tubular Adenoma (Code C7041)
281680                    CTNNB1  ENST00000349496.5            2346    2514  ...    C5496                                   NaN  colorectal    Colon Tubulovillous Adenoma (Code C5496)
281681                    CTNNB1  ENST00000349496.5            2346    2514  ...  C136486                                   NaN        lung  Lung Adenocarcinoma In Situ (Code C136486)
281682                    CTNNB1  ENST00000349496.5            2346    2514  ...    C7041                                   NaN  colorectal          Colon Tubular Adenoma (Code C7041)

[2770616 rows x 42 columns]
10
11
12
13
14
15
16
17
18
19
                    GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO       CLASS                                               NAME
0       PARP8_ENST00000505697  ENST00000505697.2            2565   26124  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
1        EMSY_ENST00000525038  ENST00000525038.1            3972   18071  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
2        EMSY_ENST00000525038  ENST00000525038.1            3972   18071  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
3        EMSY_ENST00000525038  ENST00000525038.1            3972   18071  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
4        EMSY_ENST00000525038  ENST00000525038.1            3972   18071  ...    C5105  http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
...                       ...                ...             ...     ...  ...      ...                                   ...         ...                                                ...
295857                    KIT  ENST00000288135.5            2931    6342  ...   C27735  http://www.ebi.ac.uk/efo/EFO_1000192  colorectal  Colorectal Gastrointestinal Stromal Tumor (Cod...
295858                   GAB4  ENST00000400588.1            1725   18325  ...    C4170                                   NaN      breast                           Spiradenoma (Code C4170)
295859   HRAS_ENST00000417302  ENST00000417302.1             513    5173  ...    C3863  http://www.ebi.ac.uk/efo/EFO_1000306      breast          Breast Intraductal Papilloma (Code C3863)
295860  RUNX1_ENST00000325074  ENST00000325074.5            1407   10471  ...   C53553  http://www.ebi.ac.uk/efo/EFO_1000143      breast  Breast Carcinoma by Gene Expression Profile (C...
295861                   KRAS  ENST00000256078.4             570    6407  ...    C2965  http://www.ebi.ac.uk/efo/EFO_0000384  colorectal                         Crohn Disease (Code C2965)

[2831744 rows x 42 columns]
20
21
22
23
24
25
26
27
28
29
                    GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                           EFO       CLASS                                               NAME
0                        LTN1  ENST00000389194.2            5439   13082  ...    C5105          http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
1        KRAS_ENST00000557334  ENST00000557334.1             228    6407  ...    C5105          http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
2        KRAS_ENST00000557334  ENST00000557334.1             228    6407  ...    C5105          http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
3        KRAS_ENST00000557334  ENST00000557334.1             228    6407  ...    C5105          http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
4        PCCB_ENST00000468777  ENST00000468777.1            1713    8654  ...    C5105          http://www.ebi.ac.uk/efo/EFO_0000365  colorectal             Colorectal Adenocarcinoma (Code C5105)
...                       ...                ...             ...     ...  ...      ...                                           ...         ...                                                ...
268829   KRAS_ENST00000556131  ENST00000556131.1             132    6407  ...   C60536                                           NaN  colorectal                 Aberrant Crypt Focus (Code C60536)
268830                 CELSR2  ENST00000271332.3            8772    3231  ...    C8851                                           NaN  colorectal         Diffuse Large B-Cell Lymphoma (Code C8851)
268831                   TP53  ENST00000269305.4            1182   11998  ...   C27502                                           NaN        lung  Extraskeletal Myxoid Chondrosarcoma (Code C27502)
268832                   TP53  ENST00000269305.4            1182   11998  ...   C27502                                           NaN  colorectal  Extraskeletal Myxoid Chondrosarcoma (Code C27502)
268833  KDM5C_ENST00000404049  ENST00000404049.3            4680   11114  ...    C2918  http://purl.obolibrary.org/obo/MONDO_0004379      breast               Female Breast Carcinoma (Code C2918)

[2742949 rows x 42 columns]
30
31
32
33
34
35
36
37
38
39
                      GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                   EFO       CLASS                                      NAME
0                     LINC00923  ENST00000503874.3             363   28088  ...    C4017  http://www.ebi.ac.uk/efo/EFO_0006318      breast      Breast Ductal Carcinoma (Code C4017)
1         CSMD1_ENST00000539096  ENST00000539096.1            6330   14026  ...    C4017  http://www.ebi.ac.uk/efo/EFO_0006318      breast      Breast Ductal Carcinoma (Code C4017)
2                         LRP1B  ENST00000389484.3           13800    6693  ...    C4017  http://www.ebi.ac.uk/efo/EFO_0006318      breast      Breast Ductal Carcinoma (Code C4017)
3         PRRX1_ENST00000367760  ENST00000367760.3             654    9142  ...    C4017  http://www.ebi.ac.uk/efo/EFO_0006318      breast      Breast Ductal Carcinoma (Code C4017)
4       C2orf88_ENST00000396974  ENST00000396974.2             288   28191  ...    C4017  http://www.ebi.ac.uk/efo/EFO_0006318      breast      Breast Ductal Carcinoma (Code C4017)
...                         ...                ...             ...     ...  ...      ...                                   ...         ...                                       ...
273455   FBXO11_ENST00000405808  ENST00000405808.1             174   13590  ...   C96477  http://www.ebi.ac.uk/efo/EFO_1000504  colorectal      Rectal Tubular Adenoma (Code C96477)
273456                    ERCC2  ENST00000391945.4            2283    3434  ...    C4860                                   NaN        lung                 Lung Sarcoma (Code C4860)
273457     TP53_ENST00000420246  ENST00000420246.2            1026   11998  ...   C27456                                   NaN  colorectal  Colorectal Tubular Adenoma (Code C27456)
273458     TP53_ENST00000420246  ENST00000420246.2            1026   11998  ...    C2965                                   NaN  colorectal                Crohn Disease (Code C2965)
273459                    SNX31  ENST00000311812.2            1323   28605  ...    C3510  http://www.ebi.ac.uk/efo/EFO_0000389      breast           Cutaneous Melanoma (Code C3510)

[2778037 rows x 42 columns]
40
41
42
43
44
45
46
47
48
49
                    GENE_NAME   ACCESSION_NUMBER GENE_CDS_LENGTH HGNC_ID  ... NCI_CODE                                           EFO       CLASS                                      NAME
0                         TEC  ENST00000381501.3            1896   11719  ...    C4349          http://www.ebi.ac.uk/efo/EFO_1001949  colorectal         Colon Adenocarcinoma (Code C4349)
1       MEGF8_ENST00000251268  ENST00000251268.6            8538    3233  ...    C4349          http://www.ebi.ac.uk/efo/EFO_1001949  colorectal         Colon Adenocarcinoma (Code C4349)
2        C1QA_ENST00000402322  ENST00000402322.1             738    1241  ...    C4349          http://www.ebi.ac.uk/efo/EFO_1001949  colorectal         Colon Adenocarcinoma (Code C4349)
3        CTNS_ENST00000441220  ENST00000441220.2             879    2518  ...    C4349          http://www.ebi.ac.uk/efo/EFO_1001949  colorectal         Colon Adenocarcinoma (Code C4349)
4        MUSK_ENST00000374440  ENST00000374440.3             351    7525  ...    C4349          http://www.ebi.ac.uk/efo/EFO_1001949  colorectal         Colon Adenocarcinoma (Code C4349)
...                       ...                ...             ...     ...  ...      ...                                           ...         ...                                       ...
119862  NCOR2_ENST00000404621  ENST00000404621.1            7377    7673  ...    C2918  http://purl.obolibrary.org/obo/MONDO_0004379      breast      Female Breast Carcinoma (Code C2918)
119863                  CSMD1  ENST00000537824.1           10695   14026  ...   C53555          http://www.ebi.ac.uk/efo/EFO_0000306      breast  Luminal B Breast Carcinoma (Code C53555)
119864                  CSMD1  ENST00000537824.1           10695   14026  ...   C53555          http://www.ebi.ac.uk/efo/EFO_0000306      breast  Luminal B Breast Carcinoma (Code C53555)
119865                  CSMD1  ENST00000537824.1           10695   14026  ...   C53555          http://www.ebi.ac.uk/efo/EFO_0000306      breast  Luminal B Breast Carcinoma (Code C53555)
119866                  CSMD1  ENST00000537824.1           10695   14026  ...   C53555          http://www.ebi.ac.uk/efo/EFO_0000306      breast  Luminal B Breast Carcinoma (Code C53555)

[2616016 rows x 42 columns]
"""