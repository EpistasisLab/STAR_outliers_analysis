#!/bin/bash
#BSUB -J step4e_run_king_subjobs
#BSUB -o step4e_run_king_subjobs.out
#BSUB -e step4e_run_king_subjobs.error

bsub < king_subjobs/get_kinships_1.sh
bsub < king_subjobs/get_kinships_2.sh
bsub < king_subjobs/get_kinships_3.sh
bsub < king_subjobs/get_kinships_4.sh
bsub < king_subjobs/get_kinships_5.sh

bsub < king_subjobs/get_kinships_12.sh
bsub < king_subjobs/get_kinships_13.sh
bsub < king_subjobs/get_kinships_14.sh
bsub < king_subjobs/get_kinships_15.sh

bsub < king_subjobs/get_kinships_23.sh
bsub < king_subjobs/get_kinships_24.sh
bsub < king_subjobs/get_kinships_25.sh

bsub < king_subjobs/get_kinships_34.sh
bsub < king_subjobs/get_kinships_35.sh

bsub < king_subjobs/get_kinships_45.sh