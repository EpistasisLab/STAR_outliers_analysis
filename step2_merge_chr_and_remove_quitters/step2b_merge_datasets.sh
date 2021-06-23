#!/bin/bash
#BSUB -J step2_runall
#BSUB -o step2_runall.out
#BSUB -e step2_runall.error
#BSUB -R "rusage[mem=20000MB]"
#BSUB -M 20000MB
module load plink/1.90Beta

#makes main genotype files
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr1 --merge-list step2.0_output_file_names.txt --remove people_who_quit.txt --make-bed --out UKB_samples
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr1 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr1_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr2 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr2_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr3 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr3_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr4 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr4_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr5 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr5_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr6 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr6_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr7 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr7_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr8 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr8_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr9 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr9_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr10 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr10_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr11 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr11_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr12 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr12_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr13 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr13_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr14 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr14_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr15 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr15_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr16 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr16_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr17 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr17_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr18 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr18_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr19 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr19_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr20 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr20_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr21 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr21_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr22 --exclude UKB_samples-merge.missnp --make-bed --out ../step1_get_UKB_samples/filtered_output/UKB_samples_chr22_modified
plink --memory 15000 --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr1_modified --merge-list step2.0_output_file_names_modified.txt --remove people_who_quit.txt --make-bed --out UKB_samples
plink --memory 15000 --exclude UKB_samples-merge.missnp --bfile ../step1_get_UKB_samples/filtered_output/UKB_samples_chr1 --merge-list step2.0_output_file_names.txt --remove people_who_quit.txt --make-bed --out UKB_samples

# makes genotype files for kinship analysis
plink --memory 15000 --bfile ../step1_get_UKB_samples/kinship_filtered_output/UKB_samples_chr1 --merge-list step2.0_kinship_output_file_names.txt --remove people_who_quit.txt --make-bed --out kinship_UKB_samples

