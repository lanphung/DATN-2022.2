import os
import sys
import pandas as pd



def create_file_list(path):
    '''
        inputs: none
        outputs: a list of all .vcf files within the current directory
    '''
    file_list = []
    for word in os.listdir(path):
        if "clinvar_GrCh38.vcf" in word:
            file_list.append(word)

    return file_list

def clean_entry(field):
    g = field.replace('\n', '')
    g = g.replace(';;', ';')
    g = g.replace(';', ' ')
    g = g.replace('=0D=0A=', '')
    return g

def read_vcf(file):
    '''
        inputs: file path with .vcf files
        outputs: a dictionary form of the .vcf file
    '''
    with open(file, 'r') as f:
        lines = [l.split(':') for l in f]# if not l.startswith('#')]
        tup_lin = [tuple(li) for li in lines]
        dt = {}

        for d in tup_lin:
            if len(d) == 2:
                dt.update({d[0]:clean_entry(d[1])})
        return dt

def create_df(file_list):
    '''
        inputs: list of files to add to Dataframe
        outputs: dataframe of the vcf files
    '''
    d_list = [read_vcf(item) for item in file_list]

    db = pd.DataFrame(d_list)
    #db.drop(['BEGIN', 'END', 'X-MS-OL-DEFAULT-POSTAL-ADDRESS', 'VERSION'], axis=1, inplace=True)
    return db

#fn = sys.argv[1]
fn = "out/vcf_output/clinvar_GrCh38"

file_list = create_file_list("/media/data/biodataset/ClinVar")
df = create_df(file_list)
df.to_csv('{}.csv'.format(fn))