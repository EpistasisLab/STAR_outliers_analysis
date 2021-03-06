import numpy as np
import pandas as pd
import os
import pdb

kinship_eid_filters_folder = "kinship_eid_filters"
kinship_filtered_output_folder = "kinship_filtered_output"
data_folder = "/project/UKB_moore/UKB_50978/genotype/penn_freeze_11132019"
chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
chromosomes += ["14", "15", "16", "17", "18", "19", "20", "21", "22", "MT", "X", "XY", "Y"]
if not os.path.exists(kinship_filtered_output_folder):
    os.mkdir(kinship_filtered_output_folder)
if not os.path.exists(kinship_eid_filters_folder):
    os.mkdir(kinship_eid_filters_folder)
output_file_names_file = open("../step2_merge_chr_and_remove_quitters/step2.0_kinship_output_file_names.txt", 'w')
for i in chromosomes:

    # makes the common part of the data filtering shell script
    filter_file_template = "#!/bin/bash\n"        
    filter_file_template += "#BSUB -J " + kinship_eid_filters_folder + "/get_UKB_samples_chr" + i + "\n" 
    filter_file_template += "#BSUB -o " + kinship_eid_filters_folder + "/get_UKB_samples_chr" + i + ".out\n" 
    filter_file_template += "#BSUB -e " + kinship_eid_filters_folder + "/get_UKB_samples_chr" + i + ".err\n\n" 
    filter_file_template += "module load python/3.8\n" 
    filter_file_template += "module load plink/1.90Beta\n\n"

    # opens the data filtering shell script for the ith chromosome plink file
    filter_path = kinship_eid_filters_folder + "/get_UKB_samples_chr" + i + ".sh"

    filter_file = open(filter_path, 'w')

    # writes the data filtering shell script for the ith chromosome plink file
    data_path_prefix = data_folder + "/ukb_snp_chr" + i + "_v2"
    filter_file_content = filter_file_template + "plink --bfile " + data_path_prefix 
    filter_file_content += " --keep eids.tab --make-bed --out " 
    filter_file_content += kinship_filtered_output_folder  + "/UKB_samples_chr" + i 
    filter_file.write(filter_file_content)
    filter_file.close()

    # adds a filtered output file name to the list of such names for merging (excuding the first file)
    if i != "1":
        output_file_names_file.write("../step1_get_UKB_samples/" + kinship_filtered_output_folder  + "/UKB_samples_chr" + i + "\n")
output_file_names_file.close()
    