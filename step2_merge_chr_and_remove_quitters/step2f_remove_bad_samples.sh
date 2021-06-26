#!/bin/bash
#BSUB -J step2_runall
#BSUB -o step2_runall.out
#BSUB -e step2_runall.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB
module load plink/1.90Beta

plink --memory 15000 --bfile kinship_UKB_samples_half_filtered --remove low_quality_FIDs.txt --make-bed --out ../step3_remove_relatives/kinship_UKB_samples_filtered
rm kinship_UKB_samples_half_filtered.bed
rm kinship_UKB_samples_half_filtered.bim
rm kinship_UKB_samples_half_filtered.fam
rm kinship_UKB_samples_half_filtered.het
rm kinship_UKB_samples_half_filtered.imiss
rm kinship_UKB_samples_half_filtered.lmiss
rm kinship_UKB_samples_half_filtered.sexcheck
rm kinship_UKB_samples_half_filtered.log