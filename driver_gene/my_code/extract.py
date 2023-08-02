import pandas as pd
num_of_line = 100

path = "/media/data/lanpd/"

# df = pd.read_table(path + "dataset/BLCA-US/simple_somatic_mutation.open.BLCA-US.tsv").head(num_of_line)

# df.to_csv(path + "dataset/BLCA-US/simple_somatic_mutation.open.BLCA-US.sample.csv")

# df = pd.read_table(path + "dataset/BLCA-US/exp_seq.BLCA-US.tsv").head(num_of_line)

# df.to_csv(path + "dataset/BLCA-US/exp_seq.BLCA-US.sample.csv")

# df = pd.read_table(path + "dataset/BLCA-US/mirna_seq.BLCA-US.tsv").head(num_of_line)

# df.to_csv(path + "dataset/BLCA-US/mirna_seq.BLCA-US.sample.csv")

df = pd.read_table("/media/data3/biodataset/COSMIC/v98/CosmicMutantExport.tsv")
print("done!")
df1 = df[df['GRCh']=='37']
print(len(df1))
df2 = df[df['GRCh']=='38']
print(len(df2))
