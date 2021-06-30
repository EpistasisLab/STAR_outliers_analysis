import pandas as pd
import pdb

path = "../step2_merge_chr_and_remove_quitters/UKB_samples.fam"
fam_file = pd.read_csv(path, delimiter = " ", header = None)
fam_file[0] = fam_file.loc[:, 1]
fam_file.to_csv(path, sep = " ", header = False, index = False)