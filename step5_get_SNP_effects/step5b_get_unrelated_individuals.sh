#!/bin/bash
#BSUB -J step5a_get_unrelated_individuals
#BSUB -o step5a_get_unrelated_individuals.out
#BSUB -e step5a_get_unrelated_individuals.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB
module load plink/1.90Beta

#Removes all related individuals from the analysis
plink --memory 15000 --bfile ../step2_merge_chr_and_remove_quitters/UKB_samples --keep ../step3_remove_relatives/unrelated_eids.tab --make-bed --out UKB_samples_unrelated
