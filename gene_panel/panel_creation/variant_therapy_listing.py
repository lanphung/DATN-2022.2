import pandas as pd
import numpy as np
import sort
import display
import docx
import math
import time
import json
import data_processing.path2resource as p2r

path = "/media/data/lanpd/data_work/gene_panel/creation/"
np.seterr(all="ignore")
pd.options.mode.chained_assignment = None  # default='warn'

civic_cl = pd.read_csv(path + f"raw_output/doid2nci.csv", index_col=False)
for i in range(0, len(civic_cl)):
    civic_cl['DOID'][i] = civic_cl['DOID'][i].replace('DOID:','')
cosmic_cl = pd.read_csv(path + f"raw_output/coso2nci.csv", index_col=False)

cond = [
    ['breast', 'asian_census', 'census'],
    ['hepatocellular_carcinoma', 'asian_census', 'census'],
    ['lung', 'asian_census', 'census'],
    ['large_intestine', 'asian_census', 'census'],
    ['thyroid', 'asian_census', 'census'],
    ['other', 'asian_census', 'census']
]

cancer_gene_a = [{} for sub in range(7)]
cancer_gene_w = [{} for sub in range(7)] 
 
final_final_columns = ['Gene name', 'Variant', 'Primary Site', 'Disease',
       'Therapies','evidence_level','therapy_rank','therapy_interaction_type','description',
       'significance', 'source_type', 'source_id', 'NCIid', 'source_db','disease_type','genomic_ID']


COSMIC_source_conversion = pd.DataFrame(data = ['PubMed','DOI','Unindexed journals, Conference abstracts',
                                                'ClinicalTrials.gov', 'Corporate website', 'Submitted to clinicaltrials.gov'
                                                ,'FDA drug label','FDA drug label','ANZCTR'], columns= ['source_name'])

gene_Supplement = ['ABL1','CDH1','CEBPA','CTNNB1','ERG','ETV1','ETV4','ETV5','EZH2','FANCA','FANCC','FANCF','FANCG',
 'FOXL2','GNA11','GNAQ','HNF1A','IDF1','IDF2','JAK1','JAK3','MAP2K2','MAP2K4','MPL','MYC','MYCN','NPM1'
,'PIK3R1','PPARG','PTPN11','RAF1','RUNX1','SMARCB1','SRC','VHL']

geneListW = pd.read_csv(path + f"raw_output/COSMIC/world_gen_set.csv", engine="pyarrow")
geneListA = pd.read_csv(path + f"raw_output/COSMIC/asia_gen_set.csv", engine="pyarrow")

world_panel = pd.read_csv(path + "output/panels/gene_panel(names only)_world.csv")['Gene']
asia_panel = pd.read_csv(path + "output/panels/gene_panel(names only)_asia.csv")['Gene']

def _get_gene_list(j, scope):
    if j < 5:
        if scope=='world':
            data = geneListW[geneListW['CLASS'] == cond[j][0]].reset_index(drop=True)
        else:
            data = geneListA[geneListA['CLASS'] == cond[j][0]].reset_index(drop=True)
        return data
    else:
        if scope=='world':
            data = geneListW
        else:
            data = geneListA
        return data
def Civicdb_filter(fn):
    evidence = pd.read_csv(fn, engine="pyarrow",encoding='utf-8')
    evidence['disease_type'].replace(to_replace = 'colorectal', value = 'large_intestine', regex = False, inplace = True)
    evidence['disease_type'].replace(to_replace = 'hepatocellular', value = 'hepatocellular_carcinoma', regex = False, inplace = True)
    evidence = evidence[evidence['evidence_type'] == "Predictive"]
    evidence = evidence[evidence['evidence_direction'] == "Supports"]
    evidence = evidence.query("evidence_level in ['A', 'B', 'C']")
    evidence.drop(columns=['is_flagged'], axis=1, inplace=True)
    evidence.insert(len(evidence.columns), "Gene name", "")
    evidence['Gene name'] = evidence['molecular_profile'].str.decode("utf-8").str.split(" ")

    evidence = evidence.reset_index()
    for k in range(0, len(evidence)):
        evidence['Gene name'][k] = evidence['Gene name'][k][0]
    return evidence

def _copy_evi_civic(sheet):
    sheet['molecular_profile'] = sheet['molecular_profile'].str.decode('utf-8',errors='ignore')
    sheet['evidence_statement'] = sheet['evidence_statement'].str.decode('utf-8',errors='ignore')
    sheet['disease'] = sheet['disease'].str.decode('utf-8',errors='ignore')

    out = pd.DataFrame(index=sheet.index, columns = final_final_columns)
    out[['Gene name', 'Variant', 'Primary Site','Disease','Therapies','evidence_level',
         'therapy_interaction_type','description','significance', 'source_type', 'source_id']] = sheet[['Gene name','molecular_profile','disease_type','disease','therapies','evidence_level','therapy_interaction_type','evidence_statement','significance','source_type','citation_id']]
    out[['disease_type']] = sheet[['disease_type']]
    out['source_db'] = 'CIVIc'
    out['therapy_rank'] = 0
    for k in range(0, len(out)):
        out['NCIid'][k] = civic_cl[civic_cl['DOID']==sheet['doid'][k]].reset_index(drop=True)['NCI_CODE'].values
    return out

def Civicdb_process(scope):
    if scope=='asia': final_list = cancer_gene_a 
    else: final_list = cancer_gene_w
    evidence = Civicdb_filter(path + f"raw_output/civicdb/all_types_evidence.csv")

    for j in range(0,6):
        data = _get_gene_list(j, scope)['list']
        if j < 5: relevant_entries = evidence[evidence['disease_type'] == cond[j][0]].reset_index(drop=True)
        else: relevant_entries = evidence
        tier_1_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_approved.xlsx", sheet_name=cond[j][0])
        tier_2_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_unapproved.xlsx", sheet_name=cond[j][0])
        for i in range(0, len(data)): 
            ########################
            gene_name = data[i]
            slice = relevant_entries[relevant_entries['Gene name'] == gene_name].reset_index(drop=True)
            if len(slice) > 0:
                filter = _copy_evi_civic(slice)
                ########################
                for k in range(0, len(tier_1_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_1_drugs['drug_name'][k], na=False))
                                & (filter['evidence_level'].isin(['A', 'B'])), 'therapy_rank'] = 1
                for k in range(0, len(tier_2_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_2_drugs['drug_name'][k], na=False)) 
                                & (filter['evidence_level'].isin(['A', 'B'])) & (filter['therapy_rank']==0), 'therapy_rank'] = 2
                filter.loc[(filter['evidence_level'].isin(['A', 'B'])) & (filter['therapy_rank']==0), 'therapy_rank'] = 3     
                filter.loc[(filter['evidence_level']=='C'), 'therapy_rank'] = 4
                ########################
                if len(filter) > 0:
                    filter = filter.sort_values(['therapy_rank'], ascending=True, ignore_index=True).reset_index(drop=True)
                    final_list[j].update({gene_name:filter})

def COSMIC_filter(fn):
    evidence = pd.read_csv(path + "raw_output/COSMIC/actionability/outer_action.csv", engine="pyarrow",encoding='utf-8')
    evidence['disease_type'].replace(to_replace = 'colorectal', value = 'large_intestine', regex = False, inplace = True)
    evidence['disease_type'].replace(to_replace = 'hepatocellular', value = 'hepatocellular_carcinoma', regex = False, inplace = True)
    return evidence

def _copy_evi_COSMIC(filter, sheet):
    out = pd.DataFrame(columns = final_final_columns)
    out[['Gene name', 'Primary Site', 'Disease','Therapies','evidence_level','source_id']] = sheet[['GENE','disease_type','DISEASE','DRUG_COMBINATION','ACTIONABILITY_RANK','TRIAL_ID']]
    out[['disease_type']] = sheet[['disease_type']]
    for k in range(0, len(out)):
        out['NCIid'][k] = cosmic_cl[cosmic_cl['COSMIC_PHENOTYPE_ID']==sheet['CLASSIFICATION_ID'][k]].reset_index(drop=True)['NCI_CODE'].values
        out['source_type'][k] = COSMIC_source_conversion['source_name'][sheet['SOURCE_TYPE'][k]-1]
        out['Variant'][k] = sheet['MUTATION_REMARK'][k]
        out['genomic_ID'][k] = sheet['GENOMIC_MUTATION_ID'][k]
    out['therapy_rank'] = 0
    out['source_db'] = "COSMIC"
    out['significance'] = "Sensitivity"
    out = pd.concat([filter.reset_index(drop=True), out.reset_index(drop=True)]).reset_index(drop=True)
    return out

def COSMIC_process(scope):
    if scope=='asia': final_list = cancer_gene_a 
    else: final_list = cancer_gene_w
    evidence = COSMIC_filter(path + "raw_output/COSMIC/actionability/outer_action.csv")
    for j in range(0,6):
        data = _get_gene_list(j, scope)['list']
        if j < 5: relevant_entries = evidence[evidence['disease_type'] == cond[j][0]].reset_index(drop=True)
        else: relevant_entries = evidence        
        tier_1_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_approved.xlsx", sheet_name=cond[j][0])
        tier_2_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_unapproved.xlsx", sheet_name=cond[j][0])
        for i in range(0, len(data)): 
            gene_name = data[i]
            if gene_name in final_list[j]: 
                filter = final_list[j][gene_name]
            else:   filter = pd.DataFrame(columns=final_final_columns)
            slice = relevant_entries[relevant_entries['GENE'] == gene_name].reset_index(drop=True)
            if len(slice) > 0:
                filter = _copy_evi_COSMIC(filter, slice)
                ########################            
                for k in range(0, len(tier_1_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_1_drugs['drug_name'][k], na=False)) 
                                & (filter['evidence_level'].isin([1,2,3])), 'therapy_rank'] = 1
                for k in range(0, len(tier_2_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_2_drugs['drug_name'][k], na=False)) 
                                & (filter['evidence_level'].isin([1,2,3])) & (filter['therapy_rank']==0), 'therapy_rank'] = 2
                filter.loc[(filter['evidence_level'].isin([1,2,3])) & (filter['therapy_rank']==0), 'therapy_rank'] = 3     
                filter.loc[(filter['evidence_level']==4), 'therapy_rank'] = 4
                ########################
                if len(filter) > 0:
                    filter = filter.sort_values(['therapy_rank'], ascending=True).reset_index(drop=True)     
                    final_list[j].update({gene_name:filter})

def COSMIC_res_filter(fn):
    evidence = pd.read_csv(fn, engine="pyarrow",encoding='utf-8')
    evidence['disease_type'].replace(to_replace = 'colorectal', value = 'large_intestine', regex = False, inplace = True)
    evidence['disease_type'].replace(to_replace = 'hepatocellular', value = 'hepatocellular_carcinoma', regex = False, inplace = True)
    return evidence

def _copy_evi_COSMIC_res(filter, sheet):
    out = pd.DataFrame(columns=final_final_columns)
    out[['Gene name','Primary Site', 'Disease','Therapies','source_id','disease_type']] = sheet[['Gene Name','Primary Tissue','Histology','Drug Name','Pubmed Id','disease_type']]
    for k in range(0, len(sheet)):
        out['Variant'][k] = f"{sheet['AA Mutation'][k]} (AA)/ {sheet['CDS Mutation'][k]} (CDS)"
        out['genomic_ID'][k] = sheet['GENOMIC_MUTATION_ID'][k]
    out['therapy_rank'] = 0
    out['source_db'] = "COSMIC"
    out['significance'] = "Resistance"
    out['source_type'] = "PubMed"
    filter = pd.concat([filter.reset_index(drop=True), out.reset_index(drop=True)]).reset_index(drop=True)
    return out

def COSMIC_res_process(scope):
    if scope=='asia': final_list = cancer_gene_a 
    else: final_list = cancer_gene_w
    evidence = COSMIC_res_filter(path + f"raw_output/COSMIC/resistance/resist_6types.csv")
    for j in range(0,6):
        data = _get_gene_list(j, scope)['list']
        tier_1_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_approved.xlsx", sheet_name=cond[j][0])
        tier_2_drugs = pd.read_excel(path + f"raw_output/drug_list/VN_unapproved.xlsx", sheet_name=cond[j][0])
        if j < 5: relevant_entries = evidence[evidence['disease_type'] == cond[j][0]].reset_index(drop=True)
        else: relevant_entries = evidence        
        for i in range(0, len(data)): 
            gene_name = data[i]
            if gene_name in final_list[j]: 
                filter = final_list[j][gene_name]
            else:   filter = pd.DataFrame(columns=final_final_columns)
            slice = relevant_entries[relevant_entries['Gene Name']==gene_name].reset_index(drop=True)
            if len(slice) > 0:
                filter = _copy_evi_COSMIC_res(filter, slice)
                #########################     
                for k in range(0, len(tier_1_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_1_drugs['drug_name'][k], na=False)), 'therapy_rank'] = 1
                for k in range(0, len(tier_2_drugs)):
                    filter.loc[(filter['Therapies'].str.contains(tier_2_drugs['drug_name'][k], na=False))
                                & (filter['therapy_rank']==0), 'therapy_rank'] = 2
                filter.loc[(filter['therapy_rank']==0), 'therapy_rank'] = 3     
            if len(filter) > 0:
                filter = filter.sort_values(['therapy_rank'], ascending=True).reset_index(drop=True)     
                final_list[j].update({gene_name:filter})

def _output(scope):
    if scope=='asia': final_list = cancer_gene_a 
    else: final_list = cancer_gene_w
    gen_total = []
    for j in range(0,6):
        print(f"{cond[j][0]} có ({len(final_list[j])}) gen chứa dữ liệu đột biến - thuốc")
        filename = path + f"output/panels/{cond[j][0]}_panel_{scope}.xlsx"
        with pd.ExcelWriter(filename, mode="w", engine="openpyxl") as writer:
            for key in final_list[j].keys():
                final_list[j][key] = final_list[j][key].fillna("n/a")
                final_list[j][key].to_excel(writer, sheet_name=key, index=False)
                gen_total.append(key)
    print(f"Số gen khác nhau trong panel : ({len(set(gen_total))}) gen ({scope})")
    print("*****************\n")    

def _extract(extract, final_list):
    for j in range(5,6):
        for key in final_list[j].keys():
            extract[key].reset_index(drop=True)
            extract[key] = pd.concat([extract[key], final_list[j][key].reset_index(drop=True)]).reset_index(drop=True)
    return extract

def _gene_based_listing(scope):
    if scope=='asia': final_list = cancer_gene_a 
    else: final_list = cancer_gene_w
    gene_list = []
    for j in range(5,6):
        for key in final_list[j].keys():
            if key not in gene_list:    gene_list.append(key)
    output = pd.DataFrame(data=None, columns=['Gene','Disease','Variant','Therapies','Therapy_rank'])
    output['Gene'] = gene_list
    extract = dict.fromkeys(gene_list, pd.DataFrame(data=None, columns=final_final_columns))
    extract = _extract(extract, final_list)
    for key in extract.keys():
        string_disease = ""
        string_variant = ""
        for k in extract[key]['Disease'].unique():
            string_disease += f"{k}; "
            string_variant += f"  {extract[key][(extract[key]['Disease']==k) & ('unspecified' not in extract[key]['Variant'])]['Variant'].nunique()}  ({k}); "
        output.loc[output['Gene']==key,'Disease'] = string_disease
        output.loc[output['Gene']==key,'Variant'] = string_variant
        output.loc[output['Gene']==key,'Therapies'] = f"Không kháng: {extract[key][extract[key]['significance']!='Resistance']['Therapies'].nunique()}/ Kháng: {extract[key][extract[key]['significance']=='Resistance']['Therapies'].nunique()}"
        output.loc[output['Gene']==key,'Therapy_rank'] = f"1: {extract[key][extract[key]['therapy_rank']==1]['Therapies'].nunique()}; 2: {extract[key][extract[key]['therapy_rank']==2]['Therapies'].nunique()}; 3: {extract[key][extract[key]['therapy_rank']==3]['Therapies'].nunique()}; 4: {extract[key][extract[key]['therapy_rank']==4]['Therapies'].nunique()}"
    with pd.ExcelWriter(path + f"output/18_5_23_baocao_{scope}.xlsx", mode="w", engine="openpyxl") as writer:
        output.to_excel(writer, index=False)








