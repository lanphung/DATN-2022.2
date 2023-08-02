source('my_code/load_files.R')
#load annovar file:
path2annovar_csv <- "/media/data/lanpd/driver_gene_project/dataset/THCA-US/batch_input/THCA-US.hg19_multianno.csv"
#create scna dataframe:
col_names= c('chr','start','end','log2ratio', 'tumor_id')
scna_table = read.table('/media/data/lanpd/driver_gene_project/dataset/THCA-US/THCA-US_CNV_batch.txt',sep=" ", header=TRUE,col.names = col_names)
#load phenolyzer score file:
path2phenolyzer_out <- "/media/data/lanpd/driver_gene_project/dataset/THCA-US/batch_input/THCA-US.annotated_gene_list"

#create feature dataframe:
features_df <- create_features_df(annovar_csv_path = path2annovar_csv,
                                  scna_df = scna_table, 
                                  phenolyzer_annotated_gene_list_path = path2phenolyzer_out,
                                  batch_analysis = TRUE)
driver_prob_df <- prioritize_driver_genes(features_df = features_df,
                                          cancer_type = "THCA")
write.csv(driver_prob_df,file='/media/data/lanpd/driver_gene_project/dataset/THCA-US/THCA_batch_result.csv', row.names=FALSE)
