import pandas as pd
import argparse as ap
import os, csv
# from classifier import COSO_targeted_classes
COSO_targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/COSO_classifier.csv')
# print(hepatocellular_classes, lung_classes, thyroid_classes, breast_classes, colorectal_classes)
# truyền tham số dòng lệnh, --i_dir là đường dẫn thư mục chứa các file input (ActionabilityData.tsv,...)
# --o_dir là thư mục chứa các file output (/output)

# usage: extract files from ActionabilityData [-h] [--i_dir I_DIR] [--o_dir O_DIR]

# options:
#   -h, --help     show this help message and exit
#   --i_dir I_DIR  Folder containing files to extract from
#   --o_dir O_DIR  Folder to extract to

# nếu không truyền tham số cùng với gọi trường trình thì chương trình sẽ sử dụng các giá trị mặc định trong 'default'
# để thay đổi giá trị mặc định của --i_dir, --o_dir thì cần thay đổi giá trị 'Default' dưới đây

dir = os.path.dirname(__file__)
# print(dir) /media/data/thanhnb/COSMIC_individual_/src/cosmic_extractor_
Default = os.path.dirname(os.path.dirname(dir))
# print(Default) /media/data/thanhnb/COSMIC_individual_
# exit()
# out_ = Default + '/out/cosmic_extractor_'
parser = ap.ArgumentParser('extract files from ActionabilityData')
parser.add_argument('--i_dir', help = 'Folder containing files to extract from', default = '/media/data3/biodataset/COSMIC/v98')
parser.add_argument('--o_dir', help = 'Folder to extract to',default = '/media/data/thanhnb/COSMIC_individual_/out/core_')
args = parser.parse_args()


# kiểm tra thư mục o_dir có tồn tại không, nếu không thì báo lỗi và dừng chương trình
if(not os.path.exists(args.o_dir)): print('invalid output dir'), exit()
# load các file input (ActionabilityData.tsv,...) từ thư mục i_dir
# ném ra error nếu không tìm thấy file
try:
    print('loading input files for Actionability output ...', end=' ')
    dir = args.i_dir + '/'
    print(dir)
    act = pd.read_table(dir + 'ActionabilityData.tsv', dtype=str, low_memory=False, encoding='utf-8')
    print(act)
    # cls = pd.read_csv(dir + 'classification.csv', usecols=[0,9,10,11,12,13,14,15,16], dtype = str, low_memory=False, encoding='utf-8')
    # cls = cls.drop_duplicates()
    print(COSO_targeted_classes)
    rs = pd.merge(act, COSO_targeted_classes, left_on = 'CLASSIFICATION_ID', right_on = 'COSMIC_PHENOTYPE_ID')
    print(rs)
    print('loaded completely.')
except FileNotFoundError: print('invalid input dir')

# tạo thư mục output con (actionability_output) chứa các file output nếu chưa có thư mục con nàsy
output = args.o_dir + '/actionability_/'
os.makedirs(output, exist_ok=True)
tags = ['GENE','MUTATION_REMARK','GENOMIC_MUTATION_ID',
        'FUSION_ID','MUTATION_AA_SYNTAX','DISEASE',
        'ACTIONABILITY_RANK','DEVELOPMENT_STATUS',
        'DRUG_COMBINATION','TESTING_REQUIRED','TRIAL_STATUS',
        'TRIAL_ID','TRIAL_NAME','COMPLETION_STATUS',
        'TRIAL_PRIMARY_COMPLETION_DATE','PATIENT_PRESCREENING',
        'RESULTS_AVAILABILITY','PROGRESSION_REMARK',
        'SOURCE_TYPE','SOURCE','TREATMENT_HISTORY',
        'PATIENT_AGE','PRIMARY_OUTCOME_MEASURE',
        'NUMBER_OF_PATIENTS','TREATED_NUMBER','CONTROL_NUMBER',
        'CONTROL_TREATMENT','ORR_TREAT','ORR_CON','ORR_CI',
        'ORR_PVAL','DOR_TREAT','DOR_CON','DOR_CI','DOR_PVAL',
        'PFS_TREAT','PFS_CON','PFS_HR','PFS_CI','PFS_PVAL',
        'TTP_TREAT','TTP_CON','TTP_HR','TTP_CI','TTP_PVAL',
        'DCR_TREAT','DCR_CON','DCR_PVAL','OS_TREAT','OS_CON',
        'OS_HR','OS_CI','OS_PVAL','OBJ_RR_TREAT','CR_COUNT',
        'PR_COUNT','SD_COUNT','RFS_TREAT','RFS_CON','RFS_HR',
        'RFS_CI','RFS_PVAL','BLOOD_RESPONSE','RESPONSE_VALUE',
        'TIMEPOINT','CLASSIFICATION_ID','LAST_UPDATED',
        'COSMIC_PHENOTYPE_ID','SITE_PRIMARY_COSMIC',
        'SITE_SUBTYPE1_COSMIC','SITE_SUBTYPE2_COSMIC',
        'SITE_SUBTYPE3_COSMIC','HISTOLOGY_COSMIC',
        'HIST_SUBTYPE1_COSMIC','HIST_SUBTYPE2_COSMIC','HIST_SUBTYPE3_COSMIC', 'CLASS'
]
rs.to_csv(output+'cosmic_5_cancers_actionability.csv', mode = 'w', index = False) 
# hàm trích xuất dữ liệu vào các file output theo giá trị cột
# ls[0] là tên cột, ls[1] là giá trị cần lấy
print()
def _extract_by_(targ):
    res = rs[rs['CLASS'] == targ]
    res.reset_index(inplace = True, drop = True)
    # res.reset_index(inplace = True, drop = True)
    # res.to_csv(output+'cosmic_actionability.csv', mode = 'a',, header = False)
    res.to_csv(output+f'cosmic_{targ}_cancer_actionability.csv',mode = 'w', index = False)
    # thông báo hoàn thành trích xuất một file
    print(f'    cosmic_{targ}_cancer_actionability.csv completed.')

# danh sách các cặp tên cột - giá trị cần lấy
# con = [['SITE_PRIMARY_COSMIC', 'lung'],
#        ['SITE_PRIMARY_COSMIC', 'breast'],
#        ['SITE_PRIMARY_COSMIC', 'thyroid'],
#        ['SITE_PRIMARY_COSMIC', 'large_intestine'],
#        ['HIST_SUBTYPE1_COSMIC', 'hepatocellular_carcinoma']]
con = ['lung', 'breast', 'thyroid', 'colorectal', 'hepatocellular']
# bắt đầu trích xuất
print('extracting Actionability output from input...')
# lặp để trích xuất
for k in range(0,5):
    _extract_by_(con[k])

# thông báo hoàn thành trích xuất tất cả file từ ActionabilityData
print('completed extracting Actionability output from input.')

