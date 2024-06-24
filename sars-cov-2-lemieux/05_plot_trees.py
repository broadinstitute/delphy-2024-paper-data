#!/usr/bin/env python

import baltic as bt
import matplotlib.pyplot as plt
from pathlib import Path

# Read in sample IDs & clades
# ===========================
# sample_ids.txt = Sample ids for 772 sequences used in Fig 3A of LeMieux et al (2021) (private communication)
print("\nReading in sample IDs...")
sample_id_2_clade = {}
with open('sample_ids.csv', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue   # Skip comments
        if line.startswith('id,'):
            continue   # Skip header
        stripped_line = line.strip()
        if not stripped_line:
            continue   # Skip empty lines
        
        id, clade = stripped_line.split(',')
        sample_id_2_clade[id] = clade

sample_ids = list(sample_id_2_clade.keys())
print(f'Read {len(sample_ids)} samples')
print(f'First 5 IDs: {sample_ids[:5]}')
print(f'Last 5 IDs: {sample_ids[-5:]}')

# Colors from https://github.com/JacobLemieux/sarscov2pub/blob/ec90f30ca5c115f8dfb2abfab3604723ff8a521e/scripts/main_figures.R#L204
cbPalette = [
    "#E69F00",   # 0 == orange
    "#56B4E9",   # 1 == light blue
    "#009E73",   # 2 == dark green
    "#F0E442",   # 3 == yellow
    "#0072B2",   # 4 == dark blue
    "#D55E00",   # 5 == dark orange
    "#CC79A7",   # 6 == violet
    "#999999",   # 7 == grey
]

clade_colours = {
    'Clade_1': cbPalette[0],  # orange
    'Clade_2': cbPalette[3],  # yellow
    'Clade_3': cbPalette[2],  # dark green
    'Clade_4': cbPalette[4],  # dark blue
    'Clade_5': cbPalette[1],  # light blue
}
def clade_of(branch_name):
    sample_id, *rest = branch_name.split('|')
    return sample_id_2_clade.get(sample_id, "None")


def plot_tree(mcc_filename, out_pdf_filename):
    mcc_tree = bt.loadNexus(mcc_filename)
    mcc_tree.traverse_tree()
    mcc_tree.setAbsoluteTime(bt.decimalDate("2020-05-09"))  # Hard-coded, but ok

    fig,ax = plt.subplots(figsize=(5,7),facecolor='w')

    x_attr=lambda k: k.absoluteTime
    c_func=lambda k: 'black' if k.branchType != 'leaf' else clade_colours.get(clade_of(k.name), 'black')
    s_func=lambda k: 20 if (k.branchType == 'leaf' and clade_of(k.name) != "None") else 1
    
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
        bt.decimalDate("2020-01-01"),
        bt.decimalDate("2020-02-06"),
        bt.decimalDate("2020-03-14"),
        bt.decimalDate("2020-04-19"),
       ])
    ax.set_xticklabels([
        "1 Jan\n2020",
        "6 Feb\n2020",
        "14 March\n2020",
        "19 April\n2020",
       ]);
    
    # TODO: Decide which nodes to annotate and how
    #target_func=lambda k: k.branchType=='node' and k.traits['posterior'] > 0.99 ## only target nodes
    #text_func=lambda k: '>0.99' #'%.2f'%(k.traits['posterior']) ## what text is plotted
    #kwargs={'va':'bottom','ha':'right','size':5} ## kwargs for text
    #
    #mcc_tree.addText(ax,x_attr=x_attr,target=target_func,text=text_func,**kwargs) ## text
    
    plt.savefig(out_pdf_filename)
    print(f'Plot saved to {out_pdf_filename}')

Path('plots').mkdir(parents=True, exist_ok=True)

plot_tree('./delphy_outputs/ma_sars_cov_2_delphy.mcc', 'plots/DelphyMcc.pdf')
plot_tree('./delphy_outputs_alpha/ma_sars_cov_2_delphy_alpha.mcc', 'plots/DelphyMccAlpha.pdf')
plot_tree('./beast2_run/ma_sars_cov_2_beast2.mcc', 'plots/Beast2Mcc.pdf')
plot_tree('./beast2_run_alpha/ma_sars_cov_2_beast2_alpha.mcc', 'plots/Beast2MccAlpha.pdf')
