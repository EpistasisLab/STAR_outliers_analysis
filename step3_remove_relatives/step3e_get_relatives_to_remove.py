import numpy as np
import pandas as pd
import pdb
from copy import deepcopy as COPY
from tqdm import tqdm
from itertools import combinations
from matplotlib import pyplot as plt

print("step 1 started")
within_subjobs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
between_subjobs = list(combinations(within_subjobs, 2))
within_subjob_paths = ["kinship_within" + job + ".kin0" for job in within_subjobs]
between_subjob_paths = ["kinship_between" + job[0] + job[1] + ".kin0" for job in between_subjobs]
subjob_paths = within_subjob_paths + between_subjob_paths
related_eids1 = pd.concat([pd.read_csv(path, delim_whitespace = True, usecols = ["FID1", "FID2"], header = 0) for path in subjob_paths])
related_eids2 = COPY(related_eids1[["FID2", "FID1"]])
related_eids1.columns = [0, 1]
related_eids2.columns = [0, 1]

print("step 1 complete")
related_eids = pd.concat([related_eids1, related_eids2])
related_eids_column0 = related_eids[0].to_numpy()
related_eids_column1 = related_eids[1].to_numpy()
all_unique_eids = np.unique(related_eids[0])

print("step 2 complete")
eid_relatives = {}
for eid in all_unique_eids: eid_relatives[eid] = []
for i in range(len(related_eids)): eid_relatives[related_eids_column0[i]].append(related_eids_column1[i])
kin_counts = np.array([len(eid_relatives[eid]) for eid in all_unique_eids])

print("step 3 complete")
sorted_kin_count_indices = np.argsort(kin_counts)
sorted_kin_counts = kin_counts[sorted_kin_count_indices]
sorted_unique_eids = all_unique_eids[sorted_kin_count_indices]

print("step 4 complete")
num_chunks = 1000
chunk_size = int(len(all_unique_eids)/num_chunks)
eid_relatives2 = {}

print("step 5 complete")
for eid in all_unique_eids: eid_relatives2[eid] = []

print("step 6 starting")
for i in tqdm(range(num_chunks)):

    if i < (num_chunks - 1):
        unique_eids = sorted_unique_eids[i*chunk_size:(i+1)*chunk_size]
    else:
        unique_eids = sorted_unique_eids[i*chunk_size:]

    unique_eid_index_sets = (related_eids_column0 == unique_eids.reshape(-1,1)).astype(np.bool_)
    
    for eid, index_set in zip(unique_eids, unique_eid_index_sets):
        if len(eid_relatives2[eid]) == 0:
            relatives_to_remove = np.unique(related_eids[1][index_set])
            for relative in relatives_to_remove:
                eid_relatives2[relative].append(eid)

eids_to_discard = np.array([eid for eid in sorted_unique_eids if len(eid_relatives2[eid]) > 0])
output = pd.DataFrame(np.array([eids_to_discard, eids_to_discard]).transpose())
output.to_csv("relatives_to_remove.tab", sep = "\t", header = False, index = False)