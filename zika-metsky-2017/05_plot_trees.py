#!/usr/bin/env python

import baltic as bt
import matplotlib.pyplot as plt
from pathlib import Path
import csv

# Read in metadata
# ===========================
print("\nReading in metadata...")
sample_id_2_geo = {}
with open('delphy_inputs/zika_metadata.csv', 'r') as f:
    r = csv.DictReader(f)
    for record in r:
        sample_id_2_geo[record['id']] = record['Geo']

# Extracted from Metsky et al, 2017
geo_colors = {
    'Suriname': '#000000',  # unlabeled in paper
    'Brazil': '#0f7232',
    'Dominican_Republic': '#97a5d1',
    'Haiti': '#e5007e',
    'USA': '#d83433',
    'Jamaica': '#009ee2',
    'Honduras': '#f29100',
    
    'El_Salvador/Guatemala': '#ffde00',
    'Guatemala': '#ffde00',

    'Puerto_Rico': '#63247d',
    'Colombia': '#b27e4b',
    'Martinique': '#a38dc2',
    
}
def color_of(branch_name):
    sample_id, *rest = branch_name.split('|')
    return geo_colors[sample_id_2_geo.get(sample_id, "?")]

def plot_tree(mcc_filename, out_pdf_filename):
    mcc_tree = bt.loadNexus(mcc_filename)
    mcc_tree.traverse_tree()
    mcc_tree.setAbsoluteTime(bt.decimalDate("2016-10-10"))  # Hard-coded, but ok

    fig,ax = plt.subplots(figsize=(5,7),facecolor='w')

    x_attr=lambda k: k.absoluteTime
    c_func=lambda k: 'black' if k.branchType != 'leaf' else color_of(k.name)
    s_func=lambda k: 20 if (k.branchType == 'leaf') else 1
    
    mcc_tree.sortBranches(descending=True)
    for k in mcc_tree.getInternal():
        k.children.reverse()
    mcc_tree.drawTree()
    
    mcc_tree.plotTree(ax,x_attr=x_attr,colour='#5B5B5C',width=0.5)
    mcc_tree.plotPoints(
        ax,
        x_attr=x_attr,
        size=s_func,
        colour=c_func,
        zorder=100,
        outline=False)
    
    ax.set_ylim(-5, mcc_tree.ySpan+5);
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.get_yaxis().set_ticks([]);
    ax.get_xaxis().set_ticks([
        bt.decimalDate("2014-01-01"),
        bt.decimalDate("2015-01-01"),
        bt.decimalDate("2016-01-01"),
        bt.decimalDate("2017-01-01"),
       ])
    ax.set_xticklabels([
        "1 Jan\n2014",
        "1 Jan\n2015",
        "1 Jan\n2016",
        "1 Jan\n2017",
       ]);
    
    plt.savefig(out_pdf_filename)
    print(f'Plot saved to {out_pdf_filename}')

Path('plots').mkdir(parents=True, exist_ok=True)

plot_tree('./delphy_outputs/zika_delphy.mcc', 'plots/DelphyMcc.pdf')
plot_tree('./delphy_outputs_alpha/zika_delphy_alpha.mcc', 'plots/DelphyMccAlpha.pdf')
plot_tree('./beast2_run/zika_beast2.mcc', 'plots/Beast2Mcc.pdf')
plot_tree('./beast2_run_alpha/zika_beast2_alpha.mcc', 'plots/Beast2MccAlpha.pdf')
