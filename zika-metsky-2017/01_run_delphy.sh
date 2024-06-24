#!/bin/bash
mkdir -p delphy_outputs
mkdir -p beast2_run

time ../delphy \
   --v0-in-fasta delphy_inputs/zika.fasta \
   --v0-init-heuristic \
   --v0-steps 1000000000 \
   --v0-out-log-file delphy_outputs/zika_delphy.log \
   --v0-log-every 200000 \
   --v0-out-trees-file delphy_outputs/zika_delphy.trees \
   --v0-tree-every 1000000 \
   --v0-out-beast-xml beast2_run/zika.xml

../treeannotator2 -heights ca -burnin 30 delphy_outputs/zika_delphy.trees delphy_outputs/zika_delphy.mcc
