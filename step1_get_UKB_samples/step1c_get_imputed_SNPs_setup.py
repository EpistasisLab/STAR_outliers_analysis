import numpy as np
import pandas as pd
import os
import pdb

eid_filters_folder = "eid_filters"
filtered_output_folder = "filtered_output"
data_folder = "/project/UKB_moore/UKB_50978/genotype/penn_freeze_11132019"
chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
chromosomes += ["14", "15", "16", "17", "18", "19", "20", "21", "22"]
if not os.path.exists(filtered_output_folder):
    os.mkdir(filtered_output_folder)
if not os.path.exists(eid_filters_folder):
    os.mkdir(eid_filters_folder)
output_file_names_file = open("../step2_merge_chr_and_remove_quitters/step2.0_output_file_names.txt", 'w')
modified_output_file_names_file = open("../step2_merge_chr_and_remove_quitters/step2.0_output_file_names_modified.txt", 'w')

# makes files to copy UKB data with imputed values
for i in chromosomes:

    # makes the common part of the data filtering shell script
    filter_file_template = "#!/bin/bash\n"
    filter_file_template += "#BSUB -J " + eid_filters_folder + "/get_UKB_imputed_samples_chr" + i + "\n"
    filter_file_template += "#BSUB -o " + eid_filters_folder + "/get_UKB_imputed_samples_chr" + i + ".out\n" 
    filter_file_template += "#BSUB -e " + eid_filters_folder + "/get_UKB_imputed_samples_chr" + i + ".err\n" 
    filter_file_template += '#BSUB -R "rusage[mem=10000MB]"\n'
    filter_file_template += "#BSUB -M 10000MB\n"
    filter_file_template += "module load qctool/2.0-rc4\n\n"

    # opens the data filtering shell script for the ith chromosome plink file
    filter_path = eid_filters_folder + "/get_UKB_imputed_samples_chr" + i + ".sh"
    filter_file = open(filter_path, 'w')

    # writes the data filtering shell script for the ith chromosome plink file
    filter_file_content = filter_file_template
    filter_file_content += "qctool -g  /project/UKB_moore/UKB_50978/imputed/penn_freeze_11132019/ukb_imp_chr" + i + "_v3.bgen \\\n" 
    filter_file_content += "-s /project/UKB_moore/UKB_50978/imputed/penn_freeze_11132019/ukb50978_imp_chr" + i + "_v3_s487314.sample \\\n"
    filter_file_content += "-og " + filtered_output_folder  + "/UKB_samples_chr" + i + " -ofiletype binary_ped \\\n"
    filter_file_content += "-incl-rsids " + eid_filters_folder + "/SNP_positions_chr" + i + ".txt -incl-samples eids_imputed.tab\n"
    filter_file.write(filter_file_content)
    filter_file.close()

    # adds a filtered output file name to the list of such names for merging (excuding the first file)
    if i != "1":
        output_file_names_file.write("../step1_get_UKB_samples/" + filtered_output_folder  + "/UKB_samples_chr" + i + "\n")
        modified_output_file_names_file.write("../step1_get_UKB_samples/" + filtered_output_folder  + "/UKB_samples_chr" + i + "_modified\n")
output_file_names_file.close()