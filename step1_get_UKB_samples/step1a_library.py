import numpy as np
import pandas as pd

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

def change_special_values(replicates):

    """
    Purpose
    -------
    Parameters
    ----------
    Returns
    -------
    """

    replicate_names = replicates.columns
    replicates = replicates.to_numpy(dtype = float)

    # -7, -17, -27, and -2 are each, for all practical purposes, "None of the above". 
    replicates[replicates == -2] = -7
    replicates[replicates == -17] = -7
    replicates[replicates == -27] = -7

    # -3, -13, -23, and -818 are literally the same
    replicates[replicates == -818] = np.nan
    replicates[replicates == -13] = np.nan
    replicates[replicates == -23] = np.nan
    replicates[replicates == -3] = np.nan

    # -1, -11, -21, and -121 are literally the same
    replicates[replicates == -121] = np.nan
    replicates[replicates == -11] = np.nan
    replicates[replicates == -21] = np.nan
    replicates[replicates == -1] = np.nan

    replicates = pd.DataFrame(replicates)
    replicates.columns = replicate_names
    return(replicates)

def binarize_categoricals(replicates, binary = False, change_vals = True):

    """
    Purpose
    -------
    Parameters
    ----------
    Returns
    -------
    """

    if change_vals == True:
        replicates = change_special_values(replicates)
    else:
        replicates.index = np.arange(len(replicates))
    field_cols = replicates.columns[replicates.columns != "eid"]
    field_values = replicates.loc[:, field_cols].to_numpy()
    field = field_cols[0].split("-")[0]
    all_missing_indices = np.all(np.isnan(field_values), axis = 1)

    unique_values = np.unique(field_values)[np.isnan(np.unique(field_values)) == False]
    field_values_bin = [np.any(field_values == value, axis = 1) for value in unique_values]
    field_values_bin = pd.DataFrame(np.array(field_values_bin).astype(int).T)
    field_values_bin.columns = [field + "-" + str(val) for val in unique_values]
    field_values_bin.loc[all_missing_indices, :] = np.nan

    if binary == True:
        field_values_bin = field_values_bin[field_values_bin.columns[:-1]]

    if ((field + "-" + str(-7.0)) in field_values_bin.columns) and change_vals == True:
        del field_values_bin[(field + "-" + str(-7.0))]

    field_values_bin["eid"] = replicates.loc[:, "eid"]
    return(field_values_bin)


