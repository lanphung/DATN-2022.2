# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
# ---

import pandas as pd
import os
path = "/media/data/lanpd/driver_gene_project/dataset/"

personal_ssm = [{} for sub in range(9000)]

prj_codes = ['BLCA-US','BRCA-US','CESC-US','COAD-US','GBM-US','HNSC-US','KIRC-US','KIRP-US','LAML-US','LGG-US','LIHC-US','LUAD-US','LUSC-US',
             'OV-US','PAAD-US','PRAD-US','READ-US','SKCM-US','STAD-US','THCA-US','UCEC-US']

def _stat_generation():
    stat_df = pd.DataFrame(index=['gene', 'patient'],columns=['BLCA-US','BRCA-US','CESC-US','COAD-US','GBM-US','HNSC-US','KIRC-US','KIRP-US','LAML-US','LGG-US','LIHC-US','LUAD-US','LUSC-US',
             'OV-US','PAAD-US','PRAD-US','READ-US','SKCM-US','STAD-US','THCA-US','UCEC-US','total'])
    gene_list = []
    patient_list = []
    with open(path+"individual_stat.txt","w") as writer:
        for item in prj_codes:
            df = pd.read_table(path+f"{item}/simple_somatic_mutation.open.{item}.tsv",low_memory=False)
            stat_df[item][0] = df['gene_affected'].nunique()
            stat_df[item][1] = df['icgc_donor_id'].nunique()
            [gene_list.append(x) for x in df['gene_affected']]
            [patient_list.append(x) for x in df['icgc_donor_id']]
            print(f"done batch {item}!")
            writer.write(f"{item}:\n")
            for patient in df['icgc_donor_id'].unique():
                pdf = df[df['icgc_donor_id'] == patient]
                writer.write(f"donor {patient}  {pdf['gene_affected'].nunique()} gen\n")
            print("done individual!")
    stat_df['total'][0] = len(set(gene_list))
    stat_df['total'][1] = len(set(patient_list))
    stat_df.to_csv(path + "gene_statistic.csv")

def _prepare_batch_avinput(): #create annovar input files
    # patient = []
    # for item in prj_codes: #for somatic mutations
    #     print(f"begin {item}")
    #     df = pd.read_table(path+f"{item}/simple_somatic_mutation.open.{item}.tsv",low_memory=False)
    #     [patient.append(x) for x in df['icgc_donor_id']]
    #     with open(path+f"{item}/{item}_batch.avinput","w") as writer:
    #         for c,d,e,f,g,h in zip(df['chromosome'], df['chromosome_start'], df['chromosome_end'], df['mutated_from_allele'], df['mutated_to_allele'], df['icgc_donor_id']):
    #             writer.write(f"{c} {d} {e} {f} {g} {h}\n")
    #             patient.append(h)
    #     print(f"finished {item}")        
    # with open("icgc_donor_list_SSM.txt","w") as writer:
    #     [writer.write(f"{x} \n") for x in set(patient)] 


    patient = []
    for item in prj_codes: #for copy number variations
        print(f"begin {item}")
        df = pd.read_table(path+f"{item}/copy_number_somatic_mutation.{item}.tsv",low_memory=False)
        with open(path+f"{item}/{item}_CNV_batch.txt","w") as writer:
            for c,d,e,f,g in zip(df['chromosome'], df['chromosome_start'], df['chromosome_end'], df['segment_mean'], df['icgc_donor_id']):
                writer.write(f"{c} {d} {e} {f} {g}\n")
                patient.append(g)
        print(f"finished {item}")
    with open("icgc_donor_list_CNV.txt","w") as writer:
        [writer.write(f"{x} \n") for x in set(patient)] 

def _prepare_personalized_avinput(): #create annovar input files
    for item in ['LIHC-US']: #for somatic mutations
        print(f"begin {item}")
        df = pd.read_table(path+f"{item}/simple_somatic_mutation.open.{item}.tsv",low_memory=False)
        for donor_id in set(df['icgc_donor_id']):
            if not os.path.exists(path + f"{item}/data/{donor_id}"):
                os.makedirs(path + f"{item}/data/{donor_id}", exist_ok=False) 
            with open(path+f"{item}/data/{donor_id}/{donor_id}.avinput","w") as writer:
                pdf = df[df['icgc_donor_id'] == donor_id] 
                for c,d,e,f,g in zip(pdf['chromosome'], pdf['chromosome_start'], pdf['chromosome_end'], pdf['mutated_from_allele'], pdf['mutated_to_allele']):
                    writer.write(f"{c} {d} {e} {f} {g} {donor_id}\n")
        print(f"finished {item}")        


    # for item in prj_codes: #for copy number somatic mutations
    #     print(f"begin {item}")
    #     df = pd.read_table(path+f"{item}/copy_number_somatic_mutation.{item}.tsv",low_memory=False)
    #     for donor_id in set(df['icgc_donor_id']):
    #         if not os.path.exists(path + f"{item}/data/{donor_id}"):
    #             os.makedirs(path + f"{item}/data/{donor_id}") 
    #         with open(path+f"{item}/data/{donor_id}/{donor_id}_CNV.txt","w") as writer:
    #             pdf = df[df['icgc_donor_id'] == donor_id] 
    #             for c,d,e,f in zip(pdf['chromosome'], pdf['chromosome_start'], pdf['chromosome_end'], pdf['segment_mean']):
    #                 writer.write(f"{c} {d} {e} {f} {donor_id}\n")
    #     print(f"finished {item}")   

def _tumor_id_suppply(): #supply the tumor_id column to all annovar outputs    
    total = 0
    for item in prj_codes: #for batch analysis
        print(f"begin {item}")
        patient = []
        df = pd.read_table(path+f"{item}/simple_somatic_mutation.open.{item}.tsv",low_memory=False)
        anno_output = pd.read_csv(path+f"{item}/batch_input/{item}.hg19_multianno.csv",engine="pyarrow").reset_index(drop=True)
        anno_output['tumor_id'] = df['icgc_donor_id']
        anno_output.reset_index(drop=True).to_csv(path+f"{item}/batch_input/{item}.hg19_multianno.csv",index=False)
        [patient.append(x) for x in df['icgc_donor_id']]
        total += len(set(patient))
        print(f"finished {item}")  
    print(total)

def _create_patient_list():
    for item in prj_codes: #for somatic mutations
        print(f"begin {item}")
        patient = []
        df = pd.read_table(path+f"{item}/simple_somatic_mutation.open.{item}.tsv",low_memory=False)
        [patient.append(x) for x in df['icgc_donor_id']]
        with open(path + f"{item}/data/{item}_ssm_patients.txt","w") as writer:
            [writer.write(f"{x}\n") for x in set(patient)]
        print(f"finished {item}")  

    for item in prj_codes: #for CNVs
        print(f"begin {item}")
        patient = []
        df = pd.read_table(path+f"{item}/copy_number_somatic_mutation.{item}.tsv",low_memory=False)
        [patient.append(x) for x in df['icgc_donor_id']]
        with open(path + f"{item}/data/{item}_cnsm_patients.txt","w") as writer:
            [writer.write(f"{x}\n") for x in set(patient)]
        print(f"finished {item}")  

def _assign_labels():
    census = pd.read_csv("")
    for item in prj_codes: #for somatic mutations
        df = pd.read_csv(path+f"{item}/{item}_driveR_features.csv",low_memory=False)
        census

def _prepare_features_files():
    # with open(path+"_all_individual_cmd.txt","w") as writer_p:
    #     for item in prj_codes:
    #         with open(path+f"{item}/data/{item}_ssm_patients.txt","r") as writer:
    #             _patient_ids = writer.readlines()
    #             for idx in _patient_ids:
    #                 id = idx.strip()         
    #                 writer_p.write(f"perl table_annovar.pl /media/data/lanpd/driver_gene_project/dataset/{item}/data/{id}/{id}.avinput humandb/ -buildver hg19 -out /media/data/lanpd/driver_gene_project/dataset/{item}/data/{id}/{item}_{id} -remove -protocol refGene,cytoBand,exac03,avsnp150,dbnsfp30a,cosmic98_coding,cosmic98_noncoding -operation gx,r,f,f,f,f,f -nastring . -csvout -polish\n")
    # with open(path+"_all_individual_cmd_pheno.txt","w") as writer_p:
    #     for item in prj_codes:
    #         with open(path+f"{item}/data/{item}_ssm_patients.txt","r") as writer:
    #             _patient_ids = writer.readlines()
    #             for idx in _patient_ids:
    #                 id = idx.strip()         
    #                 writer_p.write(f"perl table_annovar.pl /media/data/lanpd/driver_gene_project/dataset/{item}/data/{id}/{id}.avinput humandb/ -buildver hg19 -out /media/data/lanpd/driver_gene_project/dataset/{item}/data/{id}/{item}_{id} -remove -protocol refGene,cytoBand,exac03,avsnp150,dbnsfp30a,cosmic98_coding,cosmic98_noncoding -operation gx,r,f,f,f,f,f -nastring . -csvout -polish\n")
    with open(path+"_all_batches_cmd.txt","w") as writer_p:
        for item in prj_codes:
            writer_p.write(f"perl table_annovar.pl /media/data/lanpd/driver_gene_project/dataset/{item}/{item}_batch.avinput humandb/ -buildver hg19 -out /media/data/lanpd/driver_gene_project/dataset/{item}/batch_input/{item} -remove -protocol refGene,cytoBand,exac03,avsnp150,dbnsfp30a,cosmic98_coding,cosmic98_noncoding -operation gx,r,f,f,f,f,f -nastring . -csvout -polish\n")



#_stat_generation()
#_create_patient_list()
#_prepare_batch_avinput()
_prepare_personalized_avinput()
#_tumor_id_suppply()
#_prepare_features_files()
# for item in prj_codes:
#     os.system(f"find . -name \{item}_CNV.txt -type f -delete")
# for item in prj_codes:
#     os.system(f"wc -l {path}{item}/simple_somatic_mutation.open.{item}.tsv")
#     os.system(f"wc -l {path}{item}/batch_input/{item}.hg19_multianno.csv")
