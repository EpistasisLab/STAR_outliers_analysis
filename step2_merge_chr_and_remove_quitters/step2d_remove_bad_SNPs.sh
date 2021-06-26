#!/bin/bash
#BSUB -J step2_runall
#BSUB -o step2_runall.out
#BSUB -e step2_runall.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB
module load plink/1.90Beta

plink --memory 15000 --bfile kinship_UKB_samples --maf 0.005 --hwe 0.000001 --geno 0.02 --make-bed --out kinship_UKB_samples_half_filtered
rm kinship_UKB_samples.bed
rm kinship_UKB_samples.bim
rm kinship_UKB_samples.fam
rm kinship_UKB_samples.frq
rm kinship_UKB_samples.hwe
rm kinship_UKB_samples.imiss
rm kinship_UKB_samples.lmiss
rm kinship_UKB_samples.log

# produces data to check for low quality samples
plink --memory 15000 --bfile kinship_UKB_samples_half_filtered --missing --out kinship_UKB_samples_half_filtered
plink --memory 15000 --bfile kinship_UKB_samples_half_filtered --het --out kinship_UKB_samples_half_filtered
plink --memory 15000 --bfile kinship_UKB_samples_half_filtered --check-sex --out kinship_UKB_samples_half_filtered
