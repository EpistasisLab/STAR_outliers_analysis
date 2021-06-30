import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import pdb
from bed_reader import open_bed

real_names = ['Cholesterol', 'HDL cholesterol', 'Triglycerides', 'Creatinine (enzymatic) in urine']
real_names += ['Sodium in urine', 'Albumin', 'Alkaline phosphatase', 'Alanine aminotransferase']
real_names += ['Apolipoprotein B', 'Aspartate aminotransferase', 'Urea', 'Calcium']
real_names += ['C-reactive protein', 'Cystatin C', 'Gamma glutamyltransferase', 'Glucose']
real_names += ['Glycated haemoglobin (HbA1c)', 'IGF-1', 'Phosphate', 'SHBG']
real_names += ['Total protein', 'Urate', 'Vitamin D', 'Microalbumin in urine']
real_names += ['Potassium in urine', 'Apolipoprotein A', 'Direct bilirubin', 'Creatinine']
real_names += ['LDL direct', 'Lipoprotein A', 'Oestradiol', 'Rheumatoid factor'] 
real_names += ['Total bilirubin', 'Testosterone']

prefix = "../step1_get_UKB_samples/SNPs_"
SNP_phenotypes1 = pd.read_csv(prefix + "coding.txt", delimiter = "\t", header = 1)
SNP_phenotypes2 = pd.read_csv(prefix + "silent.txt", delimiter = "\t", header = 1)
SNP_phenotypes3 = pd.read_csv(prefix + "truncation.txt", delimiter = "\t", header = 1)
SNP_phenotypes = pd.concat([SNP_phenotypes1, SNP_phenotypes2, SNP_phenotypes3])[["ID", "Trait"]]
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'AST to ALT ratio', "Trait"] = np.nan
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'Creatinine in urine', "Trait"] = 'Creatinine (enzymatic) in urine'
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'HbA1c', "Trait"] = 'Glycated haemoglobin (HbA1c)'
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'LDL cholesterol', "Trait"] = 'LDL direct'
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'Non-albumin protein', "Trait"] = np.nan
SNP_phenotypes.loc[SNP_phenotypes["Trait"] == 'eGFR', "Trait"] = np.nan

real_names_to_ignore = np.setdiff1d(real_names, SNP_phenotypes["Trait"].to_numpy(dtype = str))
names = np.array(real_names)[np.isin(real_names, real_names_to_ignore) == False]
path_suffixes = ["UKB_features_adjusted.txt",
                 "UKB_features_yj_adjusted.txt",
                 "UKB_features_log_adjusted.txt",
                 "UKB_features_IQR_adjusted.txt",
                 "UKB_features_yj_IQR_adjusted.txt",
                 "UKB_features_log_IQR_adjusted.txt",
                 "UKB_features_cleaned_data_adjusted.txt",
                 "UKB_features_yj_cleaned_data_adjusted.txt",
                 "UKB_features_log_cleaned_data_adjusted.txt"]
paths = ["../step1_get_UKB_samples/" + suf for suf in path_suffixes]
phenotypes = [pd.read_csv(path, delimiter = "\t") for path in paths]
all_SNPs = pd.read_csv("UKB_samples_unrelated.bim", delimiter = "\t", header = None)[1].to_numpy(dtype = str)
all_eids = pd.read_csv("UKB_samples_unrelated.fam", delimiter = " ", header = None)[[1]]
all_eids.columns = ["eid"]
sorted_eid_indices = np.argsort(all_eids["eid"].to_numpy())
all_eids_sorted = all_eids[sorted_eid_indices]
bed_reader = open_bed("UKB_samples_unrelated.bed", count_A1 = True, num_threads = 1)
bed_file = bed_reader.read(np.s_[sorted_eid_indices, :])

genotype_subsets = []
for i, name in enumerate(names):
    SNPs = SNP_phenotypes.loc[SNP_phenotypes["Trait"] == name, "ID"].to_numpy(dtype = str)
    SNP_col_ind = np.isin(all_SNPs, SNPs)
    genotype_subsets.append(bed_file[:, SNP_col_ind])

all_correlations = []
all_p_value_sets = []
pdb.set_trace()
for Y_mat in phenotypes:
    Y_mat2 = all_eids.merge(Y_mat, on = "eid", how = "inner").sort_values(by = "eid")
    Y_mat3 = Y_mat2[Y_mat2.columns[Y_mat2.columns != "eid"]]
    X_Y_correlations = []
    X_Y_p_value_sets = []
    for i, y in enumerate(Y.T):
        X = genotype_subsets[i]
        X_y_correlations = []
        X_y_p_values = []
        for x in X.T:
            r, p = pearsonr(x, y)
            X_y_correlations.append(r)
            X_y_p_values.append(p)
        pdb.set_trace()
        X_Y_correlations.append(X_y_correlations)
        X_Y_p_value_sets.append(X_y_p_values)
    pdb.set_trace()
    all_correlations.append(X_Y_correlations)
    all_p_value_sets.append(X_Y_p_value_sets)    