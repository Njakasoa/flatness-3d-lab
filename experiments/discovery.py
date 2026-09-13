"""Bounded exploratory search. Float observations are NEVER proof certificates.

Unseeded contact-simplex samples and asymmetric multistart optimization; separate
five/six-facet cube-contact families. These ansatzes are explicitly incomplete.
"""
import itertools, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import ConvexHull

SEED=20260913
P=np.vstack([np.zeros(3),np.eye(3)])
DIRS=np.array([u for u in itertools.product(range(-2,3),repeat=3)
    if any(u) and next(x for x in u if x)>0 and np.gcd.reduce(u)==1])
GRID=np.array(list(itertools.product(range(-9,10),repeat=3)))

def vertices_from_parameters(x):
    C=np.zeros((4,4))
    for j in range(4):
        a=np.array([x[2*j],x[2*j+1],0.]); a=np.exp(a-a.max());a/=a.sum()
        C[[i for i in range(4) if i!=j],j]=a
    V=(np.vstack([P.T,np.ones(4)])@np.linalg.inv(C))[:3].T
    return V,C

def assess(V,contacts=P):
    if not np.isfinite(V).all() or np.max(abs(V))>8: return None
    try: hull=ConvexHull(V)
    except Exception: return None
    lo=np.ceil(V.min(0)).astype(int);hi=np.floor(V.max(0)).astype(int)
    pts=GRID[np.all((GRID>=lo)&(GRID<=hi),axis=1)]
    # Prescribed facet contacts are excluded from numerical interior tests.
    pts=pts[~np.any(np.all(pts[:,None,:]==contacts[None,:,:],axis=2),axis=1)]
    slack=-(pts@hull.equations[:,:3].T+hull.equations[:,3])
    depth=np.maximum(slack.min(1),0) if len(pts) else np.array([0.])
    widths=np.ptp(V@DIRS.T,axis=0)
    return float(widths.min()),float(depth.max()),float(hull.volume),widths

def facets_from_vertices(V):
    hull=ConvexHull(V);groups={}
    for e in hull.equations:
        key=tuple(np.round(e,8));groups[key]=e
    return list(groups.values())

def main(samples=2400,starts=32):
    rng=np.random.default_rng(SEED);rows=[];seeds=[];seen=set();calls=0
    delta=None
    from src.examples import codenotti_santos
    delta=np.array([[float(z) for z in v] for v in codenotti_santos().vertices])
    def record(V,family,contacts,parameters=None):
        nonlocal calls
        calls+=1; a=assess(V,contacts)
        if a is None or a[1]>1e-8:return a
        w,depth,vol,widths=a
        key=tuple(np.round(V.flatten(),8))
        if key in seen:return a
        seen.add(key)
        facets=facets_from_vertices(V)
        boundary=[];relcounts=[]
        lo=np.ceil(V.min(0)).astype(int);hi=np.floor(V.max(0)).astype(int)
        grid=GRID[np.all((GRID>=lo)&(GRID<=hi),axis=1)]
        sl=-(grid@np.array(facets)[:,:3].T+np.array(facets)[:,3])
        keep=np.all(sl>=-1e-7,axis=1);boundary=grid[keep].tolist()
        for k in range(len(facets)):
            on=np.abs(sl[:,k])<1e-7
            strict=np.all(np.delete(sl,k,axis=1)>1e-7,axis=1)
            relcounts.append(int(np.sum(on&strict)))
        active=DIRS[widths<=w+1e-6].tolist()
        dist=None
        if len(V)==4:
            dist=min(float(np.linalg.norm(V-delta[list(perm)],axis=1).max()) for perm in itertools.permutations(range(4)))
        rows.append({'id':len(rows),'status':'numeric_body','family':family,
          'width_directional_upper_estimate':w,'hollow_numeric':True,'interior_tolerance':1e-8,
          'volume_numeric':vol,'vertices':V.tolist(),'facets':[e.tolist() for e in facets],
          'facet_count':len(facets),'vertex_count':len(V),'primitive_facet_normals':None,
          'lattice_contacts_numeric':boundary,'relative_interior_contact_counts':relcounts,
          'active_directions_numeric':active,'automorphism_group':None,
          'distance_vertex_matching_in_fixed_coordinates':dist,'parameters':None if parameters is None else parameters.tolist()})
        return a
    for i in range(samples):
        x=rng.normal(0,1.1,8)
        try: V,C=vertices_from_parameters(x)
        except np.linalg.LinAlgError:continue
        a=record(V,'unseeded_unimodular_contacts',P,x)
        if a and a[1]<1e-8:seeds.append((a[0],x))
    seeds.sort(key=lambda a:-a[0])
    def objective(x):
        try:V,_=vertices_from_parameters(x)
        except np.linalg.LinAlgError:return 1e5
        a=record(V,'asymmetric_optimization',P,x)
        if a is None:return 1e4+float(np.linalg.norm(x))
        return -a[0]+200*a[1]
    for _,x in seeds[:starts]:
        opt=minimize(objective,x,method='Powell',bounds=[(-3,3)]*8,
                 options={'maxiter':35,'maxfev':1100,'xtol':2e-5,'ftol':2e-6})
        # Epigraph refinement allows multiple tied width directions to move together.
        def epigraph(y):
            try:V,_=vertices_from_parameters(y[:8]);a=record(V,'asymmetric_epigraph',P,y[:8])
            except np.linalg.LinAlgError:return 1e5
            if a is None:return 1e4
            return -y[8]+200*a[1]
        def constraints(y):
            try:V,_=vertices_from_parameters(y[:8]);return np.ptp(V@DIRS.T,axis=0)-y[8]
            except np.linalg.LinAlgError:return np.full(len(DIRS),-1e4)
        v,_=vertices_from_parameters(opt.x)
        a=assess(v)
        if a:
            minimize(epigraph,np.r_[opt.x,a[0]],method='SLSQP',
                bounds=[(-3,3)]*8+[(0,4)],constraints={'type':'ineq','fun':constraints},
                options={'maxiter':100,'ftol':1e-9})
    # Distinct five/six contact hulls, no Delta seed. Random outward support cones.
    cube=np.array(list(itertools.product((0.,1.),repeat=3)))
    for m in (5,6):
        for trial in range(400):
            contacts=cube[rng.choice(8,m,replace=False)]; normals=[]
            for p in contacts:
                # Expose p among SELECTED contacts, not among all eight cube corners.
                # Octant normals would enclose the entire cube and force omitted
                # corners into the interior: an intrinsically nonhollow generator.
                others=contacts[np.any(contacts!=p,axis=1)]-p
                for attempt in range(1000):
                    n=rng.normal(size=3)
                    if np.all(others@n < -1e-5):break
                else:raise RuntimeError('No exposing normal sampled')
                normals.append(n/np.linalg.norm(n))
            A=np.array(normals);b=np.sum(A*contacts,axis=1)
            vs=[]
            for ids in itertools.combinations(range(m),3):
                try:v=np.linalg.solve(A[list(ids)],b[list(ids)])
                except np.linalg.LinAlgError:continue
                if np.all(A@v<=b+1e-8):vs.append(v)
            if len(vs)<4:continue
            V=np.unique(np.round(vs,12),axis=0)
            # Bounded iff facet normals positively span R^3.
            try:
                normal_hull=ConvexHull(A)
                if np.any(normal_hull.equations[:,3]>=-1e-9):continue
            except Exception:continue
            record(V,f'cube_contacts_{m}_facets',contacts)
    Path('results/near_extremizers.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    best=sorted(rows,key=lambda r:-r['width_directional_upper_estimate'])[:12]
    families={}
    for r in rows:
        f=families.setdefault(r['family'],{'count':0,'best':0.,'above_3':0,'above_3_2':0,'above_3_3':0,'above_3_4':0})
        w=r['width_directional_upper_estimate'];f['count']+=1;f['best']=max(f['best'],w)
        for thresh,k in [(3,'above_3'),(3.2,'above_3_2'),(3.3,'above_3_3'),(3.4,'above_3_4')]:f[k]+=int(w>thresh)
    clusters={}
    for r in rows:
        if r['width_directional_upper_estimate']<3:continue
        key=str((r['facet_count'],tuple(sorted(r['relative_interior_contact_counts'])),len(r['active_directions_numeric'])))
        clusters[key]=clusters.get(key,0)+1
    summary={'seed':SEED,'calls':calls,'accepted_numeric_bodies':len(rows),'families':families,
        'best_ids':[r['id'] for r in best],'clusters_above_3':clusters,
        'limits':['directions only [-2,2]^3; widths are upper estimates',
          'hollowness uses float tolerance; exact certification required',
          'tetrahedral ansatz fixes unimodular contacts; no inference of universality',
          'no symmetry constraint; repeated optimization iterates are correlated',
          'multifacet families incomplete; no globally exhaustive search',
          'distance is vertex matching in fixed contact coordinates, not unimodular Hausdorff distance']}
    Path('results/discovery_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
