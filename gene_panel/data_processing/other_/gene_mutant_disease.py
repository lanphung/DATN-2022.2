import pandas as pd
import os, csv, re
from asian_ethnicity import asian_ethnicity as a_e
# from classifier import targeted_classes
targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/classifier.csv')
super_dir = os.path.dirname(__file__)
root = os.path.dirname(super_dir)
out = root+'/out'
data = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/individuals_/targeted_asian_mutant.csv', usecols = ['Gene name','ID_sample', 'Accession Number', 'GENOMIC_MUTATION_ID', 'Mutation CDS','Mutation AA', 'CLASS'], dtype = str)
data['Gene name'].replace(to_replace = r'_ENST\d+', value = '', regex = True, inplace = True)
"""
Gene name,Accession Number,Gene CDS length,HGNC ID,Sample name,ID_sample,ID_tumour,
Primary site,Site subtype 1,Site subtype 2,Site subtype 3,
Primary histology,Histology subtype 1,Histology subtype 2,Histology subtype 3,
Genome-wide screen,GENOMIC_MUTATION_ID,LEGACY_MUTATION_ID,MUTATION_ID,
Mutation CDS,Mutation AA,Mutation Description,Mutation zygosity,LOH,GRCh,
Mutation genome position,Mutation strand,Resistance Mutation,Mutation somatic status,
Pubmed_PMID,ID_STUDY,Sample Type,Tumour origin,Age,HGVSP,HGVSC,HGVSG,COSMIC_PHENOTYPE_ID,
CLASS,id_individual,ethnicity
"""
rs = data.groupby(['Gene name', 'GENOMIC_MUTATION_ID', 'Mutation CDS','Mutation AA', 'CLASS'],
                    as_index=False).size().sort_values('size', ascending = False)
rs = data.groupby(['Gene name', 'GENOMIC_MUTATION_ID', 'Mutation CDS','Mutation AA', 'CLASS'],
                    as_index=False).ID_sample.agg({'size': 'nunique'}).sort_values('size', ascending = False)

print(rs)
exit()
rs.to_csv('/media/data/thanhnb/COSMIC_individual_/out/other_/g_m_d.csv')
"""
sample_id,sample_name,id_tumour,id_individual,
primary_site,site_subtype_1,site_subtype_2,site_subtype_3,
primary_histology,histology_subtype_1,histology_subtype_2,histology_subtype_3,
therapy_relationship,sample_differentiator,mutation_allele_specification,msi,
average_ploidy,whole_genome_screen,whole_exome_screen,sample_remark,drug_response,
grade,age_at_tumour_recurrence,stage,cytogenetics,metastatic_site,tumour_source,
tumour_remark,age,ethnicity,environmental_variables,germline_mutation,therapy,
family,normal_tissue_tested,gender,individual_remark,nci_code,sample_type,cosmic_phenotype_id,CLASS

"""
data1 = pd.read_csv('/media/data3/biodataset/COSMIC/v98/CosmicResistanceMutations.tsv', dtype = str)

