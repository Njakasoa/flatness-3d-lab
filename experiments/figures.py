import json,itertools,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/flatness-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from pathlib import Path
from src.exact import Q
from src.geometry import Polytope

def draw(ax,path,title):
    r=json.loads(Path(path).read_text());V=np.array([[float(Q.from_json(x)) for x in v] for v in r['vertices']])
    K=Polytope([[Q.from_json(x) for x in v] for v in r['vertices']]);faces=[]
    for n,b,ids in K.facets():
        p=V[list(ids)];center=p.mean(0);u=p[0]-center;u/=np.linalg.norm(u)
        normal=np.array([float(x) for x in n]);normal/=np.linalg.norm(normal);v=np.cross(normal,u)
        order=np.argsort(np.arctan2((p-center)@v,(p-center)@u));faces.append(p[order])
    ax.add_collection3d(Poly3DCollection(faces,alpha=.18,facecolor='#159a9c',edgecolor='#12666c',linewidth=1))
    ax.scatter(*V.T,c='#184f60',s=20)
    pts=np.array(r['hollow_certificate']['boundary_points'])
    if len(pts):
        ax.scatter(*pts.T,c='#d24733',s=48,depthshade=False)
        for i,p in enumerate(pts):ax.text(*p,f'  p{i}',fontsize=8,color='#972d20')
    ax.set(xlabel='x',ylabel='y',zlabel='z',title=title)
    ax.auto_scale_xyz(V[:,0],V[:,1],V[:,2]);ax.set_box_aspect(np.ptp(V,axis=0));ax.view_init(elev=22,azim=36)
    ax.tick_params(labelsize=7)

def main():
    fig=plt.figure(figsize=(13,6),layout='constrained')
    fig.get_layout_engine().set(rect=(0,.09,1,.91))
    draw(fig.add_subplot(121,projection='3d'),'certificates/codenotti_santos.json','Exact baseline: 4 facets, width 2 + √2')
    draw(fig.add_subplot(122,projection='3d'),'certificates/truncated_delta.json','Truncated control: 5 facets, width > 3.4')
    fig.suptitle('Flatness-3D Lab · standard integer lattice coordinates',fontsize=16)
    fig.text(.5,.01,'Red points: all lattice contacts. The very small vertex cut is certified algebraically; it is barely visible at this scale.',ha='center',fontsize=9)
    fig.savefig('results/baseline_contacts.png',dpi=180);fig.savefig('results/baseline_contacts.svg');plt.close(fig)
    base=json.loads(Path('certificates/codenotti_santos.json').read_text())
    fig=plt.figure(figsize=(11,5),layout='constrained');ax=fig.add_subplot(121,projection='3d')
    dirs=base['width_certificate']['minimizing_directions_mod_sign']
    for u in dirs:
        v=np.array(u,dtype=float);ax.quiver(0,0,0,*v,arrow_length_ratio=.12)
        ax.text(*(v*1.06),str(tuple(u)),fontsize=8)
    ax.set(xlim=(0,1.3),ylim=(0,1.3),zlim=(0,1.3),xlabel='u₁',ylabel='u₂',zlabel='u₃',title='All 7 primitive minimizing directions modulo sign')
    ax.set_box_aspect((1,1,1));ax.view_init(22,35)
    ax=fig.add_subplot(122);pts=base['hollow_certificate']['boundary_points']
    for i,p in enumerate(pts):
        ax.scatter(0,i,c='#d24733',s=65);ax.text(-.08,i,str(tuple(p)),ha='right',va='center')
    for j,f in enumerate(base['hollow_certificate']['facets']):
        ax.scatter(1,j,c='#159a9c',s=70,marker='s');ax.text(1.08,j,f'Facet {j}',va='center')
        for p in f['relative_interior_contacts']:
            i=pts.index(p);ax.plot([0,1],[i,j],color='#53697a')
    ax.set(xlim=(-.65,1.6),ylim=(-.6,3.6),title='Exact facet-contact incidence');ax.axis('off')
    fig.savefig('results/active_directions_contacts.png',dpi=180);fig.savefig('results/active_directions_contacts.svg');plt.close(fig)
    rows=[json.loads(s) for s in Path('results/near_extremizers.jsonl').read_text().splitlines()]
    fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
    for family in sorted(set(r['family'] for r in rows)):
        vals=[r['width_directional_upper_estimate'] for r in rows if r['family']==family]
        ax.hist(vals,bins=np.linspace(0,3.5,71),histtype='step',linewidth=1.6,label=f'{family} (n={len(vals)})')
    ax.axvline(2+2**.5,color='black',ls='--',lw=1,label='2 + √2')
    ax.set(yscale='log',xlabel='Numerical directional upper estimate (not certified width)',ylabel='Recorded iterates / bodies',title='Bounded discovery run — correlated iterates, incomplete families')
    ax.legend(fontsize=8);fig.savefig('results/discovery_widths.png',dpi=180);fig.savefig('results/discovery_widths.svg')
if __name__=='__main__':main()
