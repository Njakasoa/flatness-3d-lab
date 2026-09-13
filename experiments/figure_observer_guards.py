"""Static scientific view of the complete gauge-truncated guard set."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/flatness-matplotlib')
import itertools
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]


def main():
    data=json.loads((ROOT/'certificates/det2_observer_gauge_guards.json').read_text())
    contacts=[(0,0,0),(2,1,1),(0,1,0),(0,0,1)]
    fig=plt.figure(figsize=(10,8),facecolor='white')
    ax=fig.add_subplot(111,projection='3d')
    for line in data['lines']:
        points=line['points'];ax.plot(*zip(points[0],points[-1]),color='#a1a1aa',lw=.9,alpha=.55)
    automatic=[r['point'] for r in data['guards'] if r['tautological']]
    explicit=[r['point'] for r in data['guards'] if not r['tautological']]
    ax.scatter(*zip(*automatic),s=24,c='#7895b0',alpha=.5,label='44 automatic pair exclusions',depthshade=False)
    ax.scatter(*zip(*explicit),s=46,c='#c83e48',label='20 explicit pair exclusions',depthshade=False)
    for a,b in itertools.combinations(contacts,2):ax.plot(*zip(a,b),c='#122d46',lw=2)
    ax.scatter(*zip(*contacts),s=55,c='#122d46',label='Four boundary contacts',depthshade=False)
    for i,p in enumerate(contacts):ax.text(p[0],p[1],p[2]+.3,f'$p_{i}$',fontsize=10)
    ax.set(xlabel='X',ylabel='Y',zlabel='Z')
    ax.view_init(elev=22,azim=-55)
    ax.set_box_aspect((1.6,1,1))
    ax.legend(loc='upper left',fontsize=10)
    fig.suptitle('64 complete lattice guards on twelve lines',fontsize=17,y=.96)
    fig.text(.5,.91,'Conditional on four boundary contacts and all six contact-edge gauges > 37/102',ha='center',fontsize=10)
    fig.text(.5,.035,'Segments show the seven retained integer parameters per line; overlaps reduce 84 occurrences to 64 points.\nThis is a hollowness criterion under stated hypotheses, not a flatness upper bound.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.87,bottom=.09,left=.02,right=.96)
    for extension in ('png','pdf'):fig.savefig(ROOT/f'results/observer_guards.{extension}',dpi=180)
    print('Wrote results/observer_guards.png and results/observer_guards.pdf')


if __name__=='__main__':main()
