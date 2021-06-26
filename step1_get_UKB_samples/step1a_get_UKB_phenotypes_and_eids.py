import numpy as np
import pandas as pd
import os
import pdb
from functools import reduce
from copy import deepcopy as COPY
from scipy.stats import yeojohnson as yj
from scipy.stats import pearsonr

from matplotlib import pyplot as plt

from step1a_library import is_field
from step1a_library import binarize_categoricals

# field 22006-0.0: white if yes, np.nan otherwise (https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=22006)
# Note: field 22006-0.0 appears to equal the subset of field 21000-0-0 who self-identify as both white and british

# covariate correction factors:
# top 40 UKB-provided PCs: 22009
# 1 yr age indicator variables: 21022
# gender indicator: 22001
# 5-year age by gender indicators: derived
# 1 hr fasting time indicators (and single indicator for >18h and for 0 or 1 hours): 74
# estimated sample dilutionfactor (icosatiles): 30897
# assessment center indicators: 54
# genotyping batch indicators: 22000
# time of sampling during the day (icosatiles): [3166 for blood, 20035 for urine] 
# date of assay indicators: varies
# month of assessment indicators (and a single indicator for all of 2006 and August through October of 2010): 53
# The residuals are used for all downstream analysis:

# the following are skipped because white brits only have one ethnicity value:
# If I'm wrong, it comprises a neglidgible portion of variance anyway. 
# ethnicity indicators: 21000
# ethnicity by gender indicators: derived

# eid, whiteness, and anomalous heterozygosity, as determined by the UKB.

def innerjoin(df1, df2): return(df1.merge(df2, how = "inner", on = "eid"))
def outerjoin(df1, df2): return(df1.merge(df2, how = "outer", on = "eid"))

def IQR_remover(df):
    eids = df.loc[:, "eid"].to_numpy()
    names = df.columns
    mat = df.to_numpy()
    q25, q75 = np.nanpercentile(mat, [25, 75], axis = 0)
    IQR = q75 - q25
    lb = q25 - 1.5*IQR
    ub = q75 + 1.5*IQR
    mat[np.logical_or(mat < lb, mat > ub)] = np.nan
    df = pd.DataFrame(mat)
    df.columns = names
    df["eid"] = eids
    return(df)



metadata = ["22006", "22027"]

features = ["30500", "30510", "30520", "30530"]
features += ["30600", "30610", "30620", "30630", "30640", "30650", "30660", "30670", "30680", "30690"]
features += ["30700", "30710", "30720", "30730", "30740", "30750", "30760", "30770", "30780", "30790"]
features += ["30800", "30810", "30820", "30830", "30840", "30850", "30860", "30870", "30880", "30890"]

PCs = ["22009"]

covariates = ["21022", "22001", "21000", "74"]
covariates += ["54", "22000", "3166", "53"]

# 3166 and 20035 are for blood only and urine only respectively. 
# Others each correspond to only one measurement. 
# device IDs ("30503", "30513", "30523", "30533") have only 1 unique value each.
f_covariates = ["30502", "30512", "30522", "30532", "3166", "20035"]
f_covariates += ["30601", "30611", "30621", "30631", "30641", "30651", "30661", "30671", "30681", "30691"]
f_covariates += ["30701", "30711", "30721", "30731", "30741", "30751", "30761", "30771", "30781", "30791"]
f_covariates += ["30801", "30811", "30821", "30831", "30841", "30851", "30861", "30871", "30881", "30891"]
f_covariates += ["30602", "30612", "30622", "30632", "30642", "30652", "30662", "30672", "30682", "30692"]
f_covariates += ["30702", "30712", "30722", "30732", "30742", "30752", "30762", "30772", "30782", "30792"]
f_covariates += ["30802", "30812", "30822", "30832", "30842", "30852", "30862", "30872", "30882", "30892"]

my_fields = ["eid"] + metadata + features + PCs + covariates + f_covariates

if not os.path.exists("input_UKB_data.txt"):

    # path to old original dataset
    # path1 = "/project/UKB_moore/UKB_50978/phenotype/penn_freeze_11132019/ukb38304.csv"

    path1 = "/project/UKB_moore/UKB_50978/phenotype/penn_freeze_05142021/ukb46981.csv"
    path2 = "/project/UKB_moore/UKB_50978/phenotype/penn_add_08042020/ukb43023.csv"
    path3 = "/project/UKB_moore/UKB_50978/phenotype/penn_add_12082020/ukb44783.csv"
    path4 = "/project/UKB_moore/UKB_50978/phenotype/penn_add_12232020/ukb44910.csv"

    fields1 = pd.read_csv(path1, delimiter = ',', usecols = lambda col_name: is_field(col_name, my_fields), header = 0, low_memory = False)
    fields2 = pd.read_csv(path2, delimiter = ',', usecols = lambda col_name: is_field(col_name, my_fields), header = 0, low_memory = False)
    fields3 = pd.read_csv(path3, delimiter = ',', usecols = lambda col_name: is_field(col_name, my_fields), header = 0, low_memory = False)
    fields4 = pd.read_csv(path4, delimiter = ',', usecols = lambda col_name: is_field(col_name, my_fields), header = 0, low_memory = False)

    fields = fields1.merge(fields2, how = "inner", on = "eid")
    fields = fields.merge(fields3, how = "inner", on = "eid")
    fields = fields.merge(fields4, how = "inner", on = "eid")

    fields.to_csv("input_UKB_data.txt", sep = "\t", header = True, index = False)

else:
    fields = pd.read_csv("input_UKB_data.txt", delimiter = '\t', header = 0)

metadata
field_cols = fields.columns
field_reps = np.array([rep.split("-")[0] for rep in field_cols])
rep_indices = np.array([(rep + "-0.0").split("-")[1].split(".")[1] for rep in field_cols])
field_names = np.unique(field_reps)
missing_fields = pd.DataFrame(np.setdiff1d(my_fields, field_names))
missing_fields.to_csv("missing_fields.txt", sep = "\t", header = False, index = False)

metadata_ind = np.isin(field_reps, ["eid"] + metadata)
features_ind = np.logical_and(np.isin(field_reps, ["eid"] + features), rep_indices == "0")
PCs_ind = np.isin(field_reps, ["eid"] + PCs)
covariates_ind = np.logical_and(np.isin(field_reps, ["eid"] + covariates), rep_indices == "0")
f_covariates_ind = np.logical_and(np.isin(field_reps, ["eid"] + f_covariates), rep_indices == "0")

metadata_df = fields[field_cols[metadata_ind]]
features_df = fields[field_cols[features_ind]]
PCs_df = fields[field_cols[PCs_ind]]
covariates_df = fields[field_cols[covariates_ind]]
f_covariates_df = fields[field_cols[f_covariates_ind]]

no_f_covariates = (np.any(f_covariates_df.isna(), axis = 1)).to_numpy()
no_covariates = (np.any(covariates_df.isna(), axis = 1)).to_numpy()
no_PCs = (np.any(PCs_df.isna(), axis = 1)).to_numpy()
bad_het = (metadata_df["22027-0.0"] == 1).to_numpy()
not_wbrits = (metadata_df["22006-0.0"] != 1).to_numpy()
indices_to_keep = np.any([no_f_covariates, no_covariates, no_PCs, 
                          bad_het, not_wbrits], axis = 0) == False

metadata_df = metadata_df[indices_to_keep]
features_df = features_df[indices_to_keep]
PCs_df = PCs_df[indices_to_keep]
covariates_df = covariates_df[indices_to_keep]
f_covariates_df = f_covariates_df[indices_to_keep]

# TODO! 30897 (dilutionfactor) needs to be added
binary_covariates = ["21022", "22001", "74", "54", "22000", "55"]

age_vec = covariates_df.loc[:, "21022-0.0"].to_numpy()
covariates_df["age_by_gender"] = ((age_vec - np.min(age_vec))/5).astype(int)*5 + np.min(age_vec)
age = binarize_categoricals(covariates_df[["eid", "21022-0.0"]])
age_by_gender = binarize_categoricals(covariates_df[["eid", "age_by_gender"]]) 
gender =  covariates_df.loc[:, ["eid", "22001-0.0"]].astype(float)
gender.index = age.index
age_by_gender_names = age_by_gender.columns[age_by_gender.columns != "eid"]
for col in age_by_gender_names: age_by_gender[col] *= (gender["22001-0.0"].to_numpy())
fasting_time = binarize_categoricals(covariates_df[["eid", "74-0.0"]])
fasting_time["74-1.0"] += fasting_time.loc[:, "74-0.0"]
del fasting_time["74-0.0"]
other_times = ["74-19.0", "74-20.0", "74-21.0", "74-22.0", "74-23.0"]
other_times += ["74-24.0", "74-25.0", "74-26.0", "74-27.0", "74-28.0"] 
other_times += ["74-29.0", "74-30.0", "74-36.0", "74-40.0", "74-48.0"]
fasting_time["74-18.0"] += np.sum(fasting_time[other_times].to_numpy(), axis = 1)
for time in other_times: del fasting_time[time]
center_IDs = binarize_categoricals(covariates_df[["eid", "54-0.0"]])
batch_effects = binarize_categoricals(covariates_df[["eid", "22000-0.0"]], False, False)
dates = covariates_df.loc[:, ["eid", "53-0.0"]]
date_components = dates.loc[:, "53-0.0"].astype(str).str.split("-", expand = True)
dates[["year", "month", "day"]] = date_components.astype(int)
is_weird_2010 = np.logical_and(dates["year"]==2010, np.isin(dates["month"], [8,9,10]))
is_2006 = dates["year"]==2006
is_other = np.logical_or(is_weird_2010, is_2006)
months =  binarize_categoricals(dates[["eid", "month"]])
month_names = months.columns[months.columns != "eid"]
for col in month_names: months[col] *= (is_other == False).to_numpy()
months["other"] = is_other.to_numpy()
# month of assessment indicators (and a single indicator for all of 2006 and August through October of 2010): 55 
PCs_df.index = age.index
other_cov = [age, gender, age_by_gender, fasting_time, center_IDs, batch_effects, months, PCs_df]
all_cov = reduce(innerjoin, other_cov)
all_cov.to_csv("all_covariates.txt", sep = "\t", header = False, index = False)

names = features_df.columns
names = [name.split("-")[0] for name in names]
real_names = ['eid', 'Cholesterol', 'HDL cholesterol', 'Triglycerides', 'Creatinine (enzymatic) in urine']
real_names += ['Sodium in urine', 'Albumin', 'Alkaline phosphatase', 'Alanine aminotransferase']
real_names += ['Apolipoprotein B', 'Aspartate aminotransferase', 'Urea', 'Calcium']
real_names += ['C-reactive protein', 'Cystatin C', 'Gamma glutamyltransferase', 'Glucose']
real_names += ['Glycated haemoglobin (HbA1c)', 'IGF-1', 'Phosphate', 'SHBG']
real_names += ['Total protein', 'Urate', 'Vitamin D', 'Microalbumin in urine']
real_names += ['Potassium in urine', 'Apolipoprotein A', 'Direct bilirubin', 'Creatinine']
real_names += ['LDL direct', 'Lipoprotein A', 'Oestradiol', 'Rheumatoid factor'] 
real_names += ['Total bilirubin', 'Testosterone']
features_df.columns = real_names
features_df = features_df[np.sort(real_names)]
features_log_df = np.log(features_df.loc[:, :])
features_log_df["eid"] = features_df.loc[:, "eid"]
features_yj_df = COPY(features_df.loc[:, :])
for name in real_names: 
    mu = np.nanmean(features_df[name])
    sigma = np.nanstd(features_df[name])
    x = features_df[name].dropna()
    is_val = (np.isnan(features_df[name]) == False)
    features_yj_df.loc[is_val, name] = yj((x - mu)/sigma)[0]
features_yj_df["eid"] = features_df.loc[:, "eid"]
features_df_IQR = IQR_remover(COPY(features_df))
features_log_df_IQR = IQR_remover(COPY(features_log_df))
features_yj_df_IQR = IQR_remover(COPY(features_yj_df))

features_df.to_csv("UKB_features.txt", sep = "\t", header = True, index = False)
features_log_df.to_csv("UKB_features_log.txt", sep = "\t", header = True, index = False)
features_yj_df.to_csv("UKB_features_yj.txt", sep = "\t", header = True, index = False)
features_df_IQR.to_csv("UKB_features_IQR.txt", sep = "\t", header = True, index = False)
features_log_df_IQR.to_csv("UKB_features_log_IQR.txt", sep = "\t", header = True, index = False)
features_yj_df_IQR.to_csv("UKB_features_yj_IQR.txt", sep = "\t", header = True, index = False)

features_df[["eid", "eid"]].to_csv("eids.tab", sep = "\t", header = False, index = False)    
features_df[["eid"]].to_csv("eids_imputed.tab", sep = "\t", header = False, index = False)  