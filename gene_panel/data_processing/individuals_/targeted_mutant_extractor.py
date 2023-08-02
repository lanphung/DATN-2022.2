import pandas as pd
import os, csv
from asian_ethnicity import asian_ethnicity as a_e
# from classifier import targeted_classes
targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/classifier.csv', dtype = str, low_memory = False)
super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)

right_tags = ['SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC', 'SITE_SUBTYPE3_COSMIC',
              'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC', 'HIST_SUBTYPE3_COSMIC']
left_tags = ['Primary site', 'Site subtype 1', 'Site subtype 2', 'Site subtype 3',
             'Primary histology', 'Histology subtype 1', 'Histology subtype 2', 'Histology subtype 3']
dir = '/media/data/thanhnb/COSMIC_individual_/out/individuals_/'
tags = ['Gene name', 'Accession Number', 'Gene CDS length',
        'HGNC ID', 'Sample name', 'ID_sample', 'ID_tumour',
        'Primary site', 'Site subtype 1', 'Site subtype 2', 'Site subtype 3',
        'Primary histology', 'Histology subtype 1', 'Histology subtype 2', 'Histology subtype 3',
        'Genome-wide screen', 'GENOMIC_MUTATION_ID', 'LEGACY_MUTATION_ID', 'MUTATION_ID',
        'Mutation CDS', 'Mutation AA', 'Mutation Description', 'Mutation zygosity',
        'LOH', 'GRCh', 'Mutation genome position', 'Mutation strand', 'Resistance Mutation',
        'Mutation somatic status', 'Pubmed_PMID', 'ID_STUDY', 'Sample Type', 'Tumour origin',
        'Age', 'HGVSP', 'HGVSC', 'HGVSG', 'COSMIC_PHENOTYPE_ID', 'CLASS']
with open (dir+'/targeted_mutation.csv', mode = 'w', newline = '') as f:
    tsv_writer = csv.writer(f) #put the lines to a variable.
    tsv_writer.writerow(tags)
# gene_set = {}    
chunks = pd.read_table('/media/data3/biodataset/COSMIC/v98/GRCh37/CosmicMutantExport.tsv', encoding = 'latin-1', dtype = str, low_memory = False, chunksize = 5*10**6)
for chunk in chunks:
    # gen_set = gen_set|set(chunk['Gene name'])
    result = chunk.merge(targeted_classes, left_on = left_tags, right_on = right_tags).drop(right_tags, axis = 1)
    result.to_csv(dir+'/targeted_mutation.csv', mode = 'a', index = False, header = False)

# current = next(df)
# result = current.merge(targeted_classes, left_on = left_tags, right_on = right_tags).drop(right_tags, axis = 1)
# print(result)