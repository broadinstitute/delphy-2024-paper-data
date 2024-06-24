#!/bin/bash
mkdir -p delphy_outputs
mkdir -p beast2_run

time ../delphy \
   --v0-in-fasta delphy_inputs/ma_sars_cov_2.fasta \
   --v0-init-heuristic \
   --v0-steps 2000000000 \
   --v0-out-log-file delphy_outputs/ma_sars_cov_2_delphy.log \
   --v0-log-every 200000 \
   --v0-out-trees-file delphy_outputs/ma_sars_cov_2_delphy.trees \
   --v0-tree-every 2000000 \
   --v0-out-beast-xml beast2_run/ma_sars_cov_2.xml

../treeannotator2 -heights ca -burnin 30 delphy_outputs/ma_sars_cov_2_delphy.trees delphy_outputs/ma_sars_cov_2_delphy.mcc
