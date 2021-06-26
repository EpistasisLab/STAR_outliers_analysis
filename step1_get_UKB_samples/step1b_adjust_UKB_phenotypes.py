import numpy as np
import pandas as pd
import os
import pdb
from functools import reduce
from scipy.stats import pearsonr
from matplotlib import pyplot as plt

def innerjoin(df1, df2): return(df1.merge(df2, how = "inner", on = "eid"))
def outerjoin(df1, df2): return(df1.merge(df2, how = "outer", on = "eid"))

all_cov = pd.read_csv("all_covariates.txt", delimiter = "\t", header = None)
paths = ["UKB_features.txt",
         "UKB_features_yj.txt",
         "UKB_features_log.txt",
         "UKB_features_IQR.txt",
         "UKB_features_yj_IQR.txt",
         "UKB_features_log_IQR.txt",
         "UKB_features_cleaned_data.txt",
         "UKB_features_yj_cleaned_data.txt",
         "UKB_features_log_cleaned_data.txt"]

for path in paths:
    path_name = path.split(".")[0]
    features_df = pd.read_csv(path, delimiter = "\t", header = 0)
    names = features_df.columns[features_df.columns != "eid"]
    
    X = all_cov[all_cov.columns[all_cov.columns != "eid"]].to_numpy(dtype = float)
    r2 = []
    y_sets = []
    if not os.path.exists("adjusted_data_" + path_name):
        os.mkdir("adjusted_data_" + path_name)
    if not os.path.exists("adjusted_data_plots_" + path_name):
        os.mkdir("adjusted_data_plots_" + path_name)
    for i, name in enumerate(names): 

        y_df = features_df.loc[:, ["eid", name]]
        y = y_df[name].to_numpy()
        not_missing = (np.isnan(y) == False)
    
        X2 = (X - np.mean(X, axis = 0))/np.std(X, axis = 0)
        X2 = X2[not_missing]
        X2 = np.concatenate([X2, np.ones((len(X2), 1))], axis = 1).astype(float)
        y2 = y[not_missing]
        y2 = (y2 - np.mean(y2))/np.std(y2)
        XtX = np.matmul(X2.T, X2) + np.eye(len(X2[0]))*1E-6
        XtX_inv = np.linalg.inv(XtX)
        y_coef = np.matmul(XtX_inv, X2.T)
    
        W = np.matmul(y_coef, y2)
        y_est = np.matmul(X2, W)
        r = pearsonr(y2, y_est)[0]
        r2.append(r**2)
        residuals = y2 - y_est
        path = "adjusted_data/" + names[i] + ".txt"
        y_df = y_df.loc[not_missing, :]
        test_value = pearsonr(y_df[name], residuals)[0]**2 + r**2
        if np.round(test_value, 3) != 1:
            print("exiting: variance accounted for by y_pred and residuals did not sum to 1")
            exit()
        y_df[name] = residuals
        y_sets.append(y_df)

        B1x = (y_est - np.mean(y_est))
        B1y = (y2 - np.mean(y2))
        B1 = np.sum(B1x*B1y)/np.sum(B1x*B1x)
        B0 = np.mean(y2) - B1*np.mean(y_est)
        est_y2 = B0 + B1*y_est
        plt.plot(y_est, y2, '*', label = "data vs estimate (R^2 = " + str(r**2) + ")")
        plt.plot(y_est, est_y2, '-', label = "best fit line")
        plt.legend()
        plt.xlabel(names[i] + " estimate")
        plt.ylabel(names[i] + " value")
        plt.savefig("adjusted_data_plots_" + path_name + "/" + names[i] + ".png")
        plt.clf()

    adjusted_data = reduce(outerjoin, y_sets).sort_values(by = "eid")
    adjusted_data.to_csv(path_name + "_adjusted.txt", sep = "\t", header = True, index = False)

adjusted_data[["eid", "eid"]].to_csv("eids.tab", sep = "\t", header = False, index = False)    
adjusted_data[["eid"]].to_csv("eids_imputed.tab", sep = "\t", header = False, index = False)  