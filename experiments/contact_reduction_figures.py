"""Scientific figures for the necessary discrete contact configurations."""
import json
from pathlib import Path
from itertools import combinations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from scipy.spatial import ConvexHull

def main():
    data=json.loads(Path('certificates/contact_hull_obstructions.json').read_text())
    eight=[c for c in data['classes'] if len(c['vertices'])==8]
    fig=plt.figure(figsize=(12,11),layout='constrained')
    for i,c in enumerate(eight):
        ax=fig.add_subplot(3,3,i+1,projection='3d')
        p=np.asarray(c['vertices'],dtype=float);hull=ConvexHull(p)
        # Triangulations serve display only. Certification uses exact integers.
        ax.plot_trisurf(p[:,0],p[:,1],p[:,2],triangles=hull.simplices,
                        alpha=.16,color='#287b8e',edgecolor='#287b8e',linewidth=.7)
        ax.scatter(*p.T,c='#c44e52',s=28,depthshade=False)
        ax.set_title(rf'Type 8.{i+1}: $\lambda_1(P-P)={c["minimum_certificate"]["lambda1"]}$',fontsize=11)
        ax.set_xlabel('x',labelpad=0);ax.set_ylabel('y',labelpad=0);ax.set_zlabel('z',labelpad=0)
        ax.set_box_aspect((1.4,1,.8))
        for axis in (ax.xaxis,ax.yaxis,ax.zaxis):axis.set_major_locator(MaxNLocator(3,integer=True))
        ax.tick_params(labelsize=7)
    fig.suptitle('Nine necessary eight-contact hulls\nInteger contacts; axes scaled independently for legibility',fontsize=16)
    fig.savefig('results/eight_contact_hulls.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    labels=['Planar square','4 vertices','5 vertices','6 vertices','7 vertices','8 vertices']
    counts=[1,10,11,22,10,9]
    bars=ax.bar(labels,counts,color=['#e4a24d']+['#287b8e']*5)
    ax.bar_label(bars,padding=3)
    ax.set_ylim(0,25);ax.set_ylabel('Necessary affine lattice classes')
    ax.set_title(r'63 contact-hull possibilities when $w(K)>\frac{11}{7}(1+2/\sqrt{3})$')
    ax.text(.5,-.17,'Exact finite enumeration; this does not assert realizability at high width.',transform=ax.transAxes,ha='center',fontsize=10)
    fig.savefig('results/contact_reduction_counts.png',dpi=180);plt.close(fig)
    print('Two contact reduction figures generated (display geometry only).')

if __name__=='__main__':main()
