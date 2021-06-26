import numpy as np
import pandas as pd
import pdb
import os
from matplotlib import pyplot as plt

eids_fam = pd.read_csv("kinship_UKB_samples_unrelated.fam", delim_whitespace = True, usecols = [0, 1], header = None).to_numpy()

set_size = int(len(eids_fam)/5)
output_set1 = pd.DataFrame(eids_fam[:1*set_size])
output_set2 = pd.DataFrame(eids_fam[1*set_size:2*set_size])
output_set3 = pd.DataFrame(eids_fam[2*set_size:3*set_size])
output_set4 = pd.DataFrame(eids_fam[3*set_size:4*set_size])
output_set5 = pd.DataFrame(eids_fam[4*set_size:5*set_size])
if len(eids_fam) != 5*len(output_set1):
    print("Error: the sample size needs to be divisible by 5!")
    exit()

folder = "data_subset_content"
if not os.path.exists(folder):
    os.mkdir(folder)
output_path1 = folder + "/subset1.tab"
output_path2 = folder + "/subset2.tab"
output_path3 = folder + "/subset3.tab"
output_path4 = folder + "/subset4.tab"
output_path5 = folder + "/subset5.tab"

output_set1.to_csv(output_path1, sep = "\t", header = False, index = False)
output_set2.to_csv(output_path2, sep = "\t", header = False, index = False)
output_set3.to_csv(output_path3, sep = "\t", header = False, index = False)
output_set4.to_csv(output_path4, sep = "\t", header = False, index = False)
output_set5.to_csv(output_path5, sep = "\t", header = False, index = False)