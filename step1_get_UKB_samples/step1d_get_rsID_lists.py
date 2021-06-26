import pandas as pd
import numpy as np
import pdb

SNPS1 = pd.read_csv("SNPs_truncation.txt", delimiter = "\t", skiprows = 1, dtype = str,
                    usecols = ["CHROM", "POS", "ID", "Trait", "BETA", "P"]).dropna(how = 'all')
SNPS2 = pd.read_csv("SNPs_coding.txt", delimiter = "\t", skiprows = 1, dtype = str,
                    usecols = ["CHROM", "POS", "ID", "Trait", "BETA", "P"]).dropna(how = 'all')
SNPS3 = pd.read_csv("SNPs_silent.txt", delimiter = "\t", skiprows = 1, dtype = str,
                    usecols = ["CHROM", "POS", "ID", "Trait", "BETA", "P"]).dropna(how = 'all')
SNPS = pd.concat([SNPS1, SNPS2, SNPS3])
SNPS.to_csv("SNP_info.txt", sep = "\t", header = True, index = False)

for i in np.arange(1, 23).astype(str):
    path = "eid_filters/SNP_positions_chr" + i + ".txt"
    SNPS_chr = SNPS.loc[SNPS["CHROM"] == i, "ID"].drop_duplicates().dropna()
    SNPS_chr.to_csv(path, sep = "\t", header = False, index = False)