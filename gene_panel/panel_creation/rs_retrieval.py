import pandas as pd
import requests, sys, json
    
server = "http://rest.ensembl.org"

#thanh_path = "/media/data/thanhnb/COSMIC_individual_/out/"
# cosmic_mutant_export = pd.read_csv(thanh_path + "individuals_/targeted_mutation.csv", engine="pyarrow")
# df = cosmic_mutant_export[['ID_sample','GENOMIC_MUTATION_ID','HGVSP','HGVSC','HGVSG']]
# df.to_csv(my_path + "cosmic_mutant_export_modified.csv")


def _get_rs_id(hgvsc_id):
    ext = f"/variant_recoder/human/{hgvsc_id}?"
        
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        
    if not r.ok:
        r.raise_for_status()
        sys.exit()
        
    decoded = r.json()
    return(decoded)

