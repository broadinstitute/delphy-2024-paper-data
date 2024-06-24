#!/usr/bin/bash

[ -f mafft ] || ln -s "`which mafft`"
[ -f delphy ] || ln -s "${HOME}/now/delphy/build/relwithdebinfo/delphy"
[ -f treeannotator2 ] || ln -s "`which treeannotator2`"  # BEAST2's treeannotator
[ -f loganalyser2 ] || ln -s "`which loganalyser2`"  # BEAST2's loganalyser

