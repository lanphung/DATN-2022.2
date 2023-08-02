import pandas as pd
import numpy as np
import sort
import display

np.seterr(all="ignore")
pd.options.mode.chained_assignment = None  # default='warn'
cond = [
    ['breast', 'asian_census', 'census'],
    ['hepatocellular', 'asian_census', 'census'],
    ['lung', 'asian_census', 'census'],
    ['colorectal', 'asian_census', 'census'],
    ['thyroid', 'asian_census', 'census']
]

def frequency_cal():
    num_asia = 0
    dp = pd.read_csv(f"/media/data/thanhnb/MyProgram/out/targeted_asian_mutant.csv")
    print(dp['CLASS'].unique())
    for j in range(0,5):
        ratio = dict()
        ratio_census = dict()
        for i in range (1,2):        
            df = dp[dp['CLASS']==cond[j][0]]
            df = df[~df['Gene name'].str.contains('ENST')]
            list = df['Gene name'].unique() 
            freq_list = [0]*len(list)
            ratio_list = [1.0]*len(list)
            gene_ratio = {
                        'list' : list, 
                        'freq': freq_list,  #how many time this gene is met over all patients
                        'ratio': ratio_list, #ratio of each gene
                        }
            # sum_patient = df['id_individual'].nunique() 
            # for k in range(0, len(list)):
            #     gene_ratio['freq'][k] = sort._count_gene_freq(list[k],df)
            #     gene_ratio['ratio'][k] = gene_ratio['freq'][k]/sum_patient
            ratio = gene_ratio
            ratio_census = gene_ratio
        #gene_ratio.sort_values(['ratio'], ascending=False)
        print(f"{cond[j][0]} has {len(ratio['list'])} (asia)")
        #display._chart_create(ratio, ratio_census, cond[j][0], 'g', 'Châu Á', 'Thế giới')
        display.write_to_doc(ratio, ratio_census, cond[j][0])

frequency_cal()
            
            






