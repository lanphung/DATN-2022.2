import pandas as pd
import argparse as ap
import os, csv
# from classifier import COSO_targeted_classes
COSO_targeted_classes = pd.read_csv('/media/data/thanhnb/COSMIC_individual_/out/core_/classifier/COSO_classifier.csv')
# nạp vào danh sách các dân tộc châu á
from asian_ethnicity import asian_ethnicity as ae
# truyền tham số dòng lệnh, --i_dir là đường dẫn thư mục chứa các file input (CosmicMutantExportCensus.tsv,...)
# --o_dir là thư mục chứa các file output (/output)

# usage: extract files from ActionabilityData [-h] [--i_dir I_DIR] [--o_dir O_DIR]

# options:
#   -h, --help     show this help message and exit
#   --i_dir I_DIR  Folder containing files to extract from
#   --o_dir O_DIR  Folder to extract to

# nếu không truyền tham số cùng với gọi trường trình thì chương trình sẽ sử dụng các giá trị mặc định trong 'default'
# để thay đổi giá trị mặc định của --i_dir, --o_dir thì cần thay đổi giá trị 'default' dưới đây

dir = os.path.dirname(__file__)
Default = os.path.dirname(dir)

parser = ap.ArgumentParser('extract files from ActionabilityData')
parser.add_argument('--i_dir', help = 'Folder containing files to extract from', default = '/media/data3/biodataset/COSMIC/v98')
parser.add_argument('--o_dir', help = 'Folder to extract to', default = '/media/data/thanhnb/COSMIC_individual_/out/core_')
args = parser.parse_args()

# kiểm tra thư mục o_dir có tồn tại không, nếu không thì báo lỗi và dừng chương trình
if(not os.path.exists(args.o_dir)): print('invalid output dir'), exit()
# load các file input (ActionabilityData.tsv,...) từ thư mục i_dir
# ném ra error nếu không tìm thấy file
try:
    print('loading input files for Census Mutation output ...', end=' ')
    in_ = args.i_dir + '/'
 
    cm = pd.read_table(in_ + 'CosmicResistanceMutations.tsv', dtype=str, low_memory=False, encoding='latin-1')
    cs = pd.read_table(in_ + 'CosmicSample.tsv', dtype=str, encoding='latin-1', low_memory=False, usecols=['sample_id','id_individual','ethnicity'])
    tmp = pd.merge(cm, cs, left_on = 'Sample ID', right_on = 'sample_id').drop_duplicates().drop('sample_id',axis=1)
    left_ = ['Primary Tissue','Tissue Subtype 1','Tissue Subtype 2',
            'Histology','Histology Subtype 1','Histology Subtype 2',]
    right_ = ['SITE_PRIMARY_COSMIC', 'SITE_SUBTYPE1_COSMIC', 'SITE_SUBTYPE2_COSMIC',
                'HISTOLOGY_COSMIC', 'HIST_SUBTYPE1_COSMIC', 'HIST_SUBTYPE2_COSMIC']
    _2classes = COSO_targeted_classes[right_+['CLASS']].drop_duplicates()
    rs = pd.merge(tmp, _2classes, left_on = left_, right_on = right_, ).drop(right_, axis = 1)
  
    print(rs)
    # exit()
    print('loaded completely.')
except FileNotFoundError: print('invalid input dir')

# tạo thư mục output con (census_mutation_output) chứa các file output nếu chưa có thư mục con này
out_ = args.o_dir + '/resistance_/'
os.makedirs(out_, exist_ok=True)
tags = ['Sample Name','Sample ID','Gene Name','Transcript',
        'Census Gene','Drug Name','MUTATION_ID','GENOMIC_MUTATION_ID',
        'LEGACY_MUTATION_ID','AA Mutation','CDS Mutation',
        'Primary Tissue','Tissue Subtype 1','Tissue Subtype 2',
        'Histology','Histology Subtype 1','Histology Subtype 2',
        'Pubmed Id','CGP Study','Somatic Status','Sample Type',
        'Zygosity','Genome Coordinates (GRCh38)','Tier','HGVSP',
        'HGVSC','HGVSG','id_individual','ethnicity','disease type']
ars = rs.query(f'ethnicity in {ae}')
rs.to_csv(out_+'cosmic_world_5_cancers_resistance.csv', mode = 'w', index = False)
ars.to_csv(out_+'cosmic_asian_5_cancers_resistance.csv', mode = 'w', index = False)
# hàm trích xuất dữ liệu vào các file output theo giá trị cột
# ls[0] là tên cột, ls[1] là giá trị cần lấy
print()
def _extract_by_(targ):
    res = rs[rs['CLASS'] == targ]
    res.reset_index(inplace = True, drop = True)
    # res.to_csv(output+'cosmic_cancer_census_mutation.csv', mode = 'a', index = False, header = False)
    res.to_csv(out_+f'cosmic_world_{targ}_cancer_resistance.csv',mode = 'w', index = False)
    # thông báo hoàn thành trích xuất một file
    # print(f'    cosmic_{ls[1]}_cancer_census_mutation.csv completed.')
    # lọc lấy ra các dân tộc châu á
    ares = ars[ars['CLASS'] == targ]
    ares.reset_index(inplace = True, drop = True)
    # ares.to_csv(output+'asian_cancer_census_mutation.csv', mode = 'a', index = False, header = False)
    ares.to_csv(out_+f'cosmic_asian_{targ}_cancer_resistance.csv',mode = 'w', index = False)
    # thông báo hoàn thành trích xuất một file
    # print(f'    cosmic_{ls[1]}_cancer_asian_census_mutation.csv completed.')

# danh sách các cặp tên cột - giá trị cần lấy
con = ['lung', 'breast', 'thyroid', 'colorectal', 'hepatocellular']
# con = [['Primary site', 'lung'],
#        ['Primary site', 'breast'],
#        ['Primary site', 'thyroid'],
#        ['Primary site', 'large_intestine'],
#        ['Histology subtype 1','hepatocellular_carcinoma']]

# bắt đầu trích xuất
print('extracting Census Mutation output from input...')

# bắt đầu trích xuất
print('extracting Actionability output from input...')
# lặp để trích xuất
for k in range(0,5):
    _extract_by_(con[k])


# thông báo hoàn thành trích xuất tất cả file từ CosmicMutantExportCensus
print('completed extracting Census Mutation output from input.')

