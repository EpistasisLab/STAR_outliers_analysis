#!/bin/bash
#BSUB -J step4a_divide_eids_into_subsets
#BSUB -o step4a_divide_eids_into_subsets.out
#BSUB -e step4a_divide_eids_into_subsets.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB

module load plink/1.90Beta

plink --memory 15000 --bfile ../step3_remove_relatives/kinship_UKB_samples_filtered --remove ../step3_remove_relatives/relatives_to_remove.tab --make-bed --out kinship_UKB_samples_unrelated
