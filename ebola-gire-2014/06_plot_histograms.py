#!/usr/bin/env python

import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import math
from pathlib import Path

def compare_logs(delphy_log_filename, beast2_log_filename, out_pdf_filename, burnin=0.10, show_alpha=False):
    beast2_raw_data = pd.read_table(beast2_log_filename, comment='#')
    num_pts = len(beast2_raw_data)
    burnin_pts = math.floor(burnin * num_pts)
    beast2_data = beast2_raw_data[burnin_pts:]
    print(f'Read in BEAST2 log in {beast2_log_filename}')
    print(f' - {num_pts} entries, of which {burnin_pts} burn-in and {len(beast2_data)} usable')

    delphy_raw_data = pd.read_table(delphy_log_filename, comment='#')
    num_pts = len(delphy_raw_data)
    burnin_pts = math.floor(burnin * num_pts)
    delphy_data = delphy_raw_data[burnin_pts:]
    print(f'Read in Delphy log in {delphy_log_filename}')
    print(f' - {num_pts} entries, of which {burnin_pts} burn-in and {len(delphy_data)} usable')

    fig,ax = plt.subplots(3, 4, figsize=(11,8.5), facecolor='w')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.3)

    def make_subplot(i, colname, title, adjuster=lambda x: x, colname_beast2=None):
        if colname_beast2 is None:
            colnames_beast2 = [x for x in beast2_data.columns if x.startswith(colname)]
            if len(colnames_beast2) == 0:
                raise ValueError(f'Column {colname} not found in BEAST2 log')
            if len(colnames_beast2) > 1:
                raise ValueError(f'Column {colname} ambiguous in BEAST2 log (matches: {colnames_beast2})')
            colname_beast2 = colnames_beast2[0]
        
        plt.subplot(3,4,i)
        plt.title(title)
        plt.xlabel(None)
        
        sb.kdeplot(adjuster(beast2_data[colname_beast2]), fill=True, color='blue');
        this_ax = sb.kdeplot(adjuster(delphy_data[colname]), fill=True, color='green');
        this_ax.set(xlabel=None)
        this_ax.get_yaxis().set_visible(False)
        return this_ax

    make_subplot( 1, 'clockRate', r'Mutation rate (x$10^{-3}$/site/year)', lambda mu: mu*1000)
    make_subplot( 2, 'TreeHeight', r'Tree Height (years)')
    this_ax = make_subplot( 3, 'kappa', r'HKY $\kappa$ parameter')
    fig.legend(this_ax.get_legend_handles_labels()[0], ['BEAST2', 'Delphy'], loc='lower right')
    if show_alpha:
        make_subplot( 4, 'gammaShape', r'Heterogeneity Spread $\alpha$')
    else:
        fig.delaxes(ax[0][3])
    
    make_subplot( 5, 'freqParameter.1', r'HKY $\pi_A$', colname_beast2='freqParameter.s:input_alignment1')
    make_subplot( 6, 'freqParameter.2', r'HKY $\pi_C$', colname_beast2='freqParameter.s:input_alignment2')
    make_subplot( 7, 'freqParameter.3', r'HKY $\pi_G$', colname_beast2='freqParameter.s:input_alignment3')
    make_subplot( 8, 'freqParameter.4', r'HKY $\pi_T$', colname_beast2='freqParameter.s:input_alignment4')

    make_subplot( 9, 'CoalescentExponential', r'Coalescent Prior')
    make_subplot(10, 'ePopSize', r'Final Pop Size (years)')
    make_subplot(11, 'growthRate', r'Pop Growth Rate (1/year)')
    fig.delaxes(ax[2][3])
    
    
    plt.savefig(out_pdf_filename)
    print(f'Plot saved to {out_pdf_filename}')

Path('plots').mkdir(parents=True, exist_ok=True)

compare_logs(
    './delphy_outputs/ebola_delphy.log',
    'beast2_run/output.log',
    'plots/DelphyVsBeast2.pdf',
    burnin=0.30
)
compare_logs(
    './delphy_outputs_alpha/ebola_delphy_alpha.log',
    'beast2_run_alpha/output.log',
    'plots/DelphyVsBeast2Alpha.pdf',
    burnin=0.30,
    show_alpha=True
)
