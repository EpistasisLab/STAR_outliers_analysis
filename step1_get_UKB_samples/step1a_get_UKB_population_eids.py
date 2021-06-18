import numpy as np
import pandas as pd
import os
import pdb

# field 22006-0.0: white if yes, np.nan otherwise (https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=22006)
# Note: field 22006-0.0 appears to equal the subset of field 21000-0-0 who self-identify as both white and british

# covariate correction factors:
# top 40 UKB-provided PCs: 22009
# 1 yr age indicator variables: 21022
# gender indicator: 22001
# 5-year age by gender indicators: derived
# ethnicity indicators: 21000 (may skip)
# ethnicity by gender indicators: derived (may skip)
# 1 hr fasting time indicators (and single indicator for >18h and for 0 or 1 hours): 74
# estimated sample dilutionfactor (icosatiles): 30897
# assessment center indicators: 54
# genotyping batch indicators: 22000
# time of sampling during the day (icosatiles): [3166 for blood, 20035 for urine] 
# date of assay indicators: varies
# month of assessment indicators (and a single indicator for all of 2006 and August through October of 2010): 55
# The residuals are used for all downstream analysis:

def is_field(col_name, fields):

    """
    Purpose
    -------
    Parameters
    ----------
    Returns
    -------
    """

    status = False
    column_has_0th_instance = False

    # These lines assume standard colname notation of "field-X.Y", where X is the instance number, and Y is the rep number.
    partial_col_names = [field + "-" for field in fields]
    colname_has_partial = np.any([col_name[0:(len(part))] == part for part in partial_col_names])
    if colname_has_partial: column_has_0th_instance = col_name.split("-")[1][0] == "0"

    # Also, if there is only 1 instance and 1 rep, then the colname is just "field"
    if column_has_0th_instance or col_name in fields: status = True
    
    return(status)

# eid, whiteness, and anomalous heterozygosity, as determined by the UKB.
path = "/project/UKB_moore/UKB_50978/phenotype/penn_freeze_11132019/ukb38304.csv"

metadata = ["eid", "22006", "22027"]

features = ["eid", "30510", "30520", "30530"]
features += ["30600", "30610", "30620", "30630", "30640", "30650", "30660", "30670", "30680", "30690"]
features += ["30700", "30710", "30720", "30730", "30740", "30750", "30760", "30770", "30780", "30790"]
features += ["30800", "30810", "30820", "30830", "30840", "30850", "30860", "30870", "30880", "30890"]

covariates = ["eid", "22009", "21022", "22001", "21000"]
covariates += ["74", "30897", "54", "22000", "3166", "20035", "55"]

f_covariates = ["eid", "30512", "30522", "30532"]
f_covariates += ["30601", "30611", "30621", "30631", "30641", "30651", "30661", "30671", "30681", "30691"]
f_covariates += ["30701", "30711", "30721", "30731", "30741", "30751", "30761", "30771", "30781", "30791"]
f_covariates += ["30801", "30811", "30821", "30831", "30841", "30851", "30861", "30871", "30881", "30891"]

if not os.path.exists("initial_input"):
    os.mkdir("initial_input)

    features_df = pd.read_csv(path, delimiter = ',', header = 0, 
                              usecols = lambda name: is_field(name, features))

    covariates_df = pd.read_csv(path, delimiter = ',', header = 0, 
                                usecols = lambda name: is_field(name, covariates))

    f_covariates_df = pd.read_csv(path, delimiter = ',', header = 0, 
                                  usecols = lambda name: is_field(name, f_covariates))

    features_df.to_csv("initial_input/features.txt", sep = "\t", header = True, index = false)
    covariates_df.to_csv("initial_input/covariates.txt", sep = "\t", header = True, index = false)
    f_covariates_df.to_csv("initial_input/f_covariates.txt", sep = "\t", header = True, index = false)
else:
    features_df = pd.read_csv("initial_input/features.txt", delimiter = '\t', header = 0)
    covariates_df = pd.read_csv("initial_input/covariates.txt", delimiter = '\t', header = 0)
    f_covariates_df = pd.read_csv("initial_input/f_covariates.txt", delimiter = '\t', header = 0)



pdb.set_trace()

eid_filters_folder = "eid_filters"
filtered_output_folder = "filtered_output"
data_folder = "/project/UKB_moore/UKB_50978/genotype/penn_freeze_11132019"
chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
chromosomes += ["14", "15", "16", "17", "18", "19", "20", "21", "22", "MT", "X", "XY", "Y"]
if not os.path.exists(filtered_output_folder):
    os.mkdir(filtered_output_folder)
if not os.path.exists(eid_filters_folder):
    os.mkdir(eid_filters_folder)
output_file_names_file = open("../step2_remove_quitters_and_get_SNP_cutoffs/step2.0_output_file_names.txt", 'w')
for i in chromosomes:

    # makes the common part of the data filtering shell script
    filter_file_template = "#!/bin/bash\n"        
    filter_file_template += "#BSUB -J " + eid_filters_folder + "/get_UKB_samples_chr" + i + "\n" 
    filter_file_template += "#BSUB -o " + eid_filters_folder + "/get_UKB_samples_chr" + i + ".out\n" 
    filter_file_template += "#BSUB -e " + eid_filters_folder + "/get_UKB_samples_chr" + i + ".err\n\n" 
    filter_file_template += "module load python/3.8\n" 
    filter_file_template += "module load plink/1.90Beta\n\n"

    # opens the data filtering shell script for the ith chromosome plink file
    filter_path = eid_filters_folder + "/get_UKB_samples_chr" + i + ".sh"

    filter_file = open(filter_path, 'w')

    # writes the data filtering shell script for the ith chromosome plink file
    data_path_prefix = data_folder + "/ukb_snp_chr" + i + "_v2"
    filter_file_content = filter_file_template + "plink --bfile " + data_path_prefix 
    filter_file_content += " --keep eids.tab --make-bed --out " 
    filter_file_content += filtered_output_folder  + "/UKB_samples_chr" + i 
    filter_file.write(filter_file_content)
    filter_file.close()

    # adds a filtered output file name to the list of such names for merging (excuding the first file)
    if i != "1":
        output_file_names_file.write("../step1_get_UKB_samples/" + filtered_output_folder  + "/UKB_samples_chr" + i + "\n")
output_file_names_file.close()
    
