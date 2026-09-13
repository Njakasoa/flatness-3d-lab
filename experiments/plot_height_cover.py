"""Draw the exact rational rectangle cover; a figure is not a proof."""
from fractions import Fraction
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]


def main():
    data=json.loads((ROOT/'results/height_interval_relaxation.json').read_text())
    records={(r['class_index'],tuple(r['extrema']),r['node']):r for r in data['queries']}
    fig,axes=plt.subplots(2,6,figsize=(15,6.4),layout='constrained')
    colors=['#d6e7f5','#a9cee6','#78afd1','#bce0d6','#85c4b3','#55a390']
    for row,idx in enumerate((6,7)):
        charts=[r for r in data['charts'] if r['class_index']==idx]
        for col in range(6):
            ax=axes[row,col]
            if col>=len(charts):ax.axis('off');continue
            C=charts[col];ext=tuple(C['extrema']);free=[i for i in range(4) if i not in ext]
            for number,node in enumerate(C['closed_leaves']):
                record=records[idx,ext,node];box=[[float(Fraction(x)) for x in r] for r in record['box']]
                (x0,x1),(y0,y1)=box
                ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor=colors[(len(node)+number)%len(colors)],edgecolor='#264653',linewidth=.8))
            ax.set(xlim=(0,1),ylim=(0,1),xticks=(0,.5,1),yticks=(0,.5,1),aspect='equal',
                   xlabel=f'q{free[0]}',ylabel=f'q{free[1]}',title=f'd={7 if idx==6 else 8}; (L,H)={ext}\n{len(C["closed_leaves"])} rectangles')
            ax.tick_params(labelsize=8)
    fig.suptitle('62 rational rectangles cover all normalized-height charts\nEach leaf relaxation is UNSAT in Z3 and independent cvc5',fontsize=14)
    fig.savefig(ROOT/'results/height_cover.png',dpi=180)
    fig.savefig(ROOT/'results/height_cover.pdf')
    plt.close(fig)
    print('Wrote height_cover.png and height_cover.pdf; explanatory figure only')


if __name__=='__main__':main()
