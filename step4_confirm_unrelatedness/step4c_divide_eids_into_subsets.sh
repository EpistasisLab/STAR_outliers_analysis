#!/bin/bash
#BSUB -J step4c_divide_eids_into_subsets
#BSUB -o step4c_divide_eids_into_subsets.out
#BSUB -e step4c_divide_eids_into_subsets.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB

module load plink/1.90Beta

#divides data into subsets
plink --memory 15000 --bfile kinship_UKB_samples_unrelated --keep data_subset_content/subset1.tab --make-bed --out data_subset_content/kinship_UKB_samples_unrelated_subset1
plink --memory 15000 --bfile kinship_UKB_samples_unrelated --keep data_subset_content/subset2.tab --make-bed --out data_subset_content/kinship_UKB_samples_unrelated_subset2
plink --memory 15000 --bfile kinship_UKB_samples_unrelated --keep data_subset_content/subset3.tab --make-bed --out data_subset_content/kinship_UKB_samples_unrelated_subset3
plink --memory 15000 --bfile kinship_UKB_samples_unrelated --keep data_subset_content/subset4.tab --make-bed --out data_subset_content/kinship_UKB_samples_unrelated_subset4
plink --memory 15000 --bfile kinship_UKB_samples_unrelated --keep data_subset_content/subset5.tab --make-bed --out data_subset_content/kinship_UKB_samples_unrelated_subset5
