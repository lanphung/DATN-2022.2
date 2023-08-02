import variant_therapy_listing as vl
import pandas as pd
import rs_retrieval as rsr
import sys, vcfpy, docx
import subprocess
import csv

my_dictionary = {}

path = "/media/data/lanpd/data_work/gene_panel/creation/"
start = vl.time.time()
new_cols = ['Gene name', 'Genomic Position', 'CDS Mutation', 'AA Mutation', 'Disease', 'therapy_rank',
             'Response to Drug', 'Therapies', 'Description', 'rs value', 'pmid', 'source_db']

cond = [
    ['breast', 'asian_census', 'census'],
    ['hepatocellular_carcinoma', 'asian_census', 'census'],
    ['lung', 'asian_census', 'census'],
    ['large_intestine', 'asian_census', 'census'],
    ['thyroid', 'asian_census', 'census'],
    ['other', 'asian_census', 'census']
]
genLoc = {}
df = pd.read_table(path + "raw_output/genLoc.tsv").reset_index(drop=True)
for x,y in zip(df['Approved symbol'], df['Chromosome']):
    genLoc.update({x:y})

my_path = "data_work/gene_panel/creation/raw_output/COSMIC/targeted_mutations/"
df = pd.read_csv(my_path + "cosmic_mutant_export_modified.csv", engine="pyarrow")


def _run_variant_listing():
    vl.Civicdb_process('asia')
    print("done civic asia")
    vl.COSMIC_process('asia')
    vl.COSMIC_res_process('asia')
    print("done cosmic asia")
    vl._output('asia')

    vl.Civicdb_process('world')
    print("done civic world")
    vl.COSMIC_process('world')
    vl.COSMIC_res_process('world') 
    print("done cosmic world")
    vl._output('world')
        
def _get_civic_db(scope):
    return vl.Civicfb_filter(pd.read_csv(path + "civic_aevidence.csv", index_col=False))

def _get_cosmic_db(scope):
    return vl.COSMIC_filter(pd.read_csv(path + "raw_output/COSMIC/merged_action.csv", index_col=False))

def _get_gene_info():
    good_list = {}
    with open(path + "raw_output/COSMIC/All_COSMIC_Genes.fasta/All_COSMIC_Genes.fasta", "r") as file:
        for line in file:
            if line.startswith('>'):
                line = line.replace("\n","").replace(">","").split(" ")
                good_list.update({line[0]:line[2]})
    return good_list

gene_info = _get_gene_info()

def _get_chrom_pos(name):
    if name in gene_info.keys():
        return gene_info[name]
    return ""

def _get_gene_loc(name):
    if name in genLoc.keys():
        return genLoc[name]
    return ""

# non_var_list = ['unspecified','Amplification','Gain-of-function','Overexpression','Rare','Rearrangement','Underexpression','Wildtype'
#                 ,'Mutation','NUCLEAR','Kinase','Expression','Fusion','Mutation','no','SERUM','Loss-of-function','Loss','Exon','DNA','deletion'
#                 ,'fusions','EXPRESSION','fusion']

def _get_CDS_mut(variant, sig, dtype, id):
    if (sig == "Resistance") & ("CDS" in variant):
        return variant.split("_")[2]
    else:
        return "n/a"
        variant = variant.split("_", 1)
        for x in non_var_list:
            if x in variant[1] : return variant[1]
        num = type1[dtype]
        for x,y,z,w,u in zip(mutantExport[num]['Gene name'],mutantExport[num]['Mutation CDS'],mutantExport[num]['Mutation AA'],mutantExport[num]['CLASS'], mutantExport[num]['HGVSG']):
            if (x==variant[0]) & (y!= "c.?") & (variant[1] in z) & (w==dtype):
                gref_var.update({id:u})
                return y
        return variant[1]

def _get_AA_mut(gene, variant, sig):
    if (sig == "Resistance") & ("CDS" in variant):
        return variant.split("_")[0]
    else: return variant

def _get_rs_value(genomic_ID):
    try:
        if genomic_ID == "": return ""
        genomic_ID = "COSV" + genomic_ID
        #print(genomic_ID)
        # cmd = ['grep', genomic_ID, '/media/data/lanpd/data_work/gene_panel/creation/raw_output/COSMIC/targeted_mutations/cosmic_mutant_export_modified.csv']
        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # o, e = proc.communicate()
        # target_entries = o.decode('ascii')
        # print(target_entries[0:10])
        target_entries = df[df['GENOMIC_MUTATION_ID'] == genomic_ID]['HGVSC'].unique()
        id_list = []
        for hgvsc_id in target_entries:
            try:
                decoded = rsr._get_rs_id(hgvsc_id)
            except:
                decoded = ""
            try:
                for entry in decoded:
                    id_list.append([(genomic_ID+" "+x) for x in entry[list(entry)[0]]['id'] if "rs" in x])
            except:
                print("an error occured!: " + hgvsc_id)
        # print("before:")
        # print(id_list)
        unique_list = set([num for sublist in id_list for num in sublist])
        # unique_list = list(set(tuple(i) for i in id_list))
        # unique_list = [list(i) for i in unique_list]

        # print("after:")
        # print(unique_list)
        return(unique_list)
    except Exception as error:
        print(target_entries)
        print("An exception occurred:", type(error).__name__, "–", error)
        quit()

def _melt(df, flag):
    new_df = pd.DataFrame(index=df.index, columns=new_cols).fillna("")
    for k in range(0, len(df)):
        new_df['Gene name'][k] = df['Gene name'][k]
        new_df['Genomic Position'][k] = f"{_get_chrom_pos(df['Gene name'][k])} | {_get_gene_loc(df['Gene name'][k])}"
        new_df['CDS Mutation'][k] = _get_CDS_mut(df['Variant'][k].replace(" ","_"), df['significance'][k],df['disease_type'][k],k)
        new_df['AA Mutation'][k] = _get_AA_mut(df['Gene name'][k], df['Variant'][k].replace(" ","_"), df['significance'][k])
        new_df['Disease'][k] = df['Disease'][k]
        new_df['therapy_rank'][k] = df['therapy_rank'][k]
        if df['significance'][k] != 'Resistance': 
            new_df['Response to Drug'][k] = 'Sensitivity' 
        else:   new_df['Response to Drug'][k] = 'Resistance'
        new_df['Therapies'][k] = df['Therapies'][k]
        new_df['Description'][k] = df['description'][k]
        new_df['pmid'][k] = f"{df['source_type'][k]}:{df['source_id'][k]}"
        new_df['source_db'][k] = df['source_db'][k]
        genomic_id_list = str(df['genomic_ID'][k]).split(" + ")
        for item in genomic_id_list:
            res = _get_rs_value(item.replace("COSV","").replace(".0",""))
            new_df['rs value'][k] = res
        #if new_df['rs value'][k] != "": print(new_df['rs value'][k])
    return new_df
def _is_census(gene):
    df = pd.read_csv(path + "raw_output/COSMIC/cancer_gene_census.csv", engine="pyarrow")
    df = df[df['Gene Symbol']==gene]
    if len(df) > 0:
        return f"Tier: {df['Tier'].values}; Entrez ID: {df['Entrez GeneId'].values}"
    return 'No'

def _run_evidence_merging(scope):
    gen_total=[]
    census_list = []
    for j in range(2,5):
        new_db = pd.DataFrame(data=None, columns=new_cols)
        panel = pd.ExcelFile(path + f"output/panels/{vl.cond[j][0]}_panel_{scope}.xlsx")
        ########################
        mydoc = docx.Document()
        mydoc.add_paragraph(f"{len(panel.sheet_names)} genes:\n")
        para = ""
        for sheet_name in panel.sheet_names:
            para += f"{sheet_name} "
        mydoc.add_paragraph(para)
        mydoc.save(path + f"output/panels/(names only){cond[j][0]}_{scope}.docx")
        ########################

        print(f"{cond[j][0]} có ({len(panel.sheet_names)}) gen chứa dữ liệu đột biến - thuốc")
        for sheet_name in panel.sheet_names:
            if sheet_name not in census_list: 
                census_list.append([sheet_name, _is_census(sheet_name)])
            gen_total.append(sheet_name)

            df = panel.parse(sheet_name, index_col=False).reset_index(drop=True).fillna("")
            new = _melt(df, j)
            new_db = pd.concat([new_db.reset_index(drop=True), new.reset_index(drop=True)]).reset_index(drop=True) 
        new_db.reset_index(drop=True).to_csv(path + f"output/BE_files/{vl.cond[j][0]}_{scope}_BE.csv", index=False) 
    print(f"Số gen khác nhau trong panel : ({len(set(gen_total))}) gen ({scope})")
    print("*****************\n")    
    pd.DataFrame(data=census_list, columns=['Gene', 'yes census?']).drop_duplicates(subset=['Gene', 'yes census?']).reset_index(drop=True).to_csv(path + f"output/panels/gene_panel(names only)_{scope}.csv")

def _rmv_dups(scope):
    for j in range(0,6):
        final_files = pd.read_csv(path + f"output/BE_files/{vl.cond[j][0]}_{scope}_BE.csv",engine="pyarrow").reset_index(drop=True)
        final_files = final_files.drop_duplicates(keep='first').reset_index(drop=True)
        print(f"{cond[j][0]}: {final_files['Gene name'].nunique()}")
        final_files.reset_index(drop=True).to_csv(path + f"output/BE_files/{vl.cond[j][0]}_{scope}_BE_dr.csv")

def _to_json():
    for j in range(0,6):
        for scope in ['world','asia']:
            df = pd.read_csv(f"/media/data/lanpd/data_work/gene_panel/creation/output/BE_files/{cond[j][0]}_{scope}_BE_dr.csv")
            df.pop(df.columns[0])
            for k in range(0, len(df)):
                df.at[k, 'Disease'] = df.at[k, 'Disease'].replace('/',"|")
                df.at[k, 'Genomic Position'] = df.at[k, 'Genomic Position'].replace('/',"|")
                #df.at[k, 'therapies'] = df.at[k, 'therapies'].replace(' ','')
            with open(f"/media/data/lanpd/data_work/gene_panel/creation/output/json/{cond[j][0]}_{scope}_BE.json", "w") as outfile:
                outfile.write(df.reset_index(drop=True).to_json(orient = 'records', indent=4))

def _try_stuff():
    scope = 'world'
    series = []
    for j in range(0,5):
        df = pd.read_csv(path + f"output/BE_files/{cond[j][0]}_{scope}_BE.csv").reset_index(drop=True)
        foo = df['Gene name'].unique()
        for k in foo:
            series.append([k, cond[j][0]])
    out = pd.DataFrame(data=series, columns=['list', 'CLASS'])
    print(out['list'].unique())
    out.to_csv(path + f"{scope}_gen_set_1.csv")
    quit()
    fn = "raw_output/ClinVar/clinvar_GrCh38.vcf"
    reader = vcfpy.Reader.from_path(fn)
    # Build and print header
    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
    header = ['#CHROM',	'POS','ID','REF','ALT','QUAL','FILTER','INFO']# + reader.header.samples.names    
    # print('\t'.join(header))
    # i = 0
    list = []
    i = 0
    for record in reader:

        if not record.is_snv():
            continue
        line = [record.INFO] #record.CHROM, record.POS, record.ID, record.REF, record.ALT, record.QUAL, record.FILTER, record.INFO]
        # line += [alt.value for alt in record.ALT]
        # line += [call.data.get('GT') or './.' for call in record.calls]
        list.append(line)
        #print('\t'.join(map(str, line)))
    df = pd.DataFrame(data= list).reset_index(drop=True)
    df.to_csv("output/vcf_output/clinvar_GrCh38.csv")
def _try_stuff_1():

    #evidence.loc[evidence['ASIAN_FREQUENCY']==, 'ASIAN_FREQUENCY'] = 0
    quit()
    evidence = pd.read_table("raw_output/cosmic_actionability.tsv")
    evidence_1 = pd.read_csv("raw_output/COSMIC/asian_action.csv")
    print(evidence.shape)
    print(evidence_1.shape)
    header = list(evidence.loc[:,:'TREATED_NUMBER'])
    print(header)
    evidence = pd.merge(evidence, evidence_1,on=header, how="left")
    print(evidence.shape)
    evidence.to_csv("output/test_action.csv")

#_try_stuff_1()
#_try_stuff()

#_run_variant_listing()

#_run_evidence_merging('asia')
#_run_evidence_merging('world')
_rmv_dups('asia')
_rmv_dups('world')
_to_json()


# with open('/media/data/lanpd/data_work/gene_panel/creation/raw_output/COSMIC/targeted_mutations/rs_data.csv', 'w') as f:
#     for key in my_dictionary.keys():
#         f.write("%s, %s\n" % (key, my_dictionary[key]))