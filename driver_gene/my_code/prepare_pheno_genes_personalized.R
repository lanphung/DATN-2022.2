source('my_code/load_files.R')
#load annovar file:
path2annovar_csv <- "/media/data/lanpd/driver_gene_project/dataset/THCA-US/data/DO39720/THCA-US_DO39720.hg19_multianno.csv"
#create scna dataframe:
col_names= c('chr','start','end','log2ratio', 'tumor_id')
scna_table = read.table('/media/data/lanpd/driver_gene_project/dataset/THCA-US/data/DO39720/DO39720_CNV.txt',sep=" ", header=TRUE,col.names = col_names)
#generate genes for phenolyzer:
phenolyzer_genes <- create_features_df(annovar_csv_path = path2annovar_csv,
                                       scna_df=scna_table,
                                       prep_phenolyzer_input = TRUE,
                                       build = "GRCh37")
write.table(x = data.frame(gene = phenolyzer_genes), 
            file = "/media/data/lanpd/driver_gene_project/dataset/THCA-US/data/DO39720/input_genes.txt", 
            row.names = FALSE, col.names = FALSE, quote = FALSE)
