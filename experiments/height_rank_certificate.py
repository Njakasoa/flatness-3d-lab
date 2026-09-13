"""Exact rank margins and determinant/height identities for two contact classes."""
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BETA=Q(37,102)
VECTORS=((1,0,0),(3,0,1),(2,0,1))


def ell(v,d,a):
    x,y,z=map(Q,v)
    return (a*x/d-y-z,x/d,y-x/d,z-a*x/d)


def symbolic_identities():
    qi,qj,ri,rj,si,sj,ti,tj,ci,cj,a,b=sp.symbols('qi qj ri rj si sj ti tj ci cj a b')
    records=[]
    for low,high in permutations(range(4),2):
        i,j=[k for k in range(4) if k not in (low,high)]
        columns=[]
        for vi,vj,total,qvalue in ((ri,rj,0,0),(si,sj,0,0),(ti,tj,0,b),(ci,cj,1,a)):
            v=[None]*4;v[i]=vi;v[j]=vj;v[high]=qvalue-qi*vi-qj*vj
            v[low]=total-vi-vj-v[high];columns.append(v)
        M=sp.Matrix(4,4,lambda row,col:columns[col][row])
        order=(i,j,low,high)
        sign=-(-1)**sum(order[r]>order[s] for r in range(4) for s in range(r+1,4))
        expected=sign*b*(ri*sj-rj*si)
        if sp.expand(M.det(method='berkowitz')-expected)!=0:
            raise ValueError('universal determinant identity')
        records.append({'low':low,'high':high,'complementary_rows':[i,j],
                        'signed_factor':sign,'identity':'det(M)=signed_factor*b*(r_i*s_j-r_j*s_i)'})
    return records


def build():
    records=[]
    for idx,d,a in ((6,7,2),(7,8,3)):
        rows=[ell(v,d,a) for v in VECTORS]
        masses=[sum(map(abs,r))/2 for r in rows]
        if rows[2]!=tuple(y-x for x,y in zip(rows[0],rows[1])):
            raise ValueError('difference triple')
        maximum=max(masses);gap=2*BETA-maximum
        if gap<=0:raise ValueError('strict rank margin')
        kmin=BETA*gap/4;kmax=masses[0]*masses[1]
        C=sp.Matrix([[sp.Rational(r[i].numerator,r[i].denominator) for r in
                      (rows[0],rows[1],ell((0,1,0),d,a),(Q(1),Q(0),Q(0),Q(0)))] for i in range(4)])
        if C.det()!=sp.Rational(1,d):raise ValueError('contact basis determinant')
        records.append({'class_index':idx,'determinant':d,'residue':a,
                        'vectors':VECTORS,'difference_barycentrics':[[str(x) for x in r] for r in rows],
                        'positive_masses':list(map(str,masses)), 'maximum_mass':str(maximum),
                        'l1_distance_to_line_lower_bound':str(gap),
                        'complementary_minor_absolute_lower_bound':str(kmin),
                        'complementary_minor_absolute_upper_bound':str(kmax),
                        'determinant_over_height_gap_lower_bound':str(d*kmin),
                        'contact_basis_determinant':str(Q(1,d)),
                        'height_gap_volume_lower_bound':str(BETA**3/(6*kmax))})
    hexagon=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
    checks=[abs(x[0]*y[1]-x[1]*y[0]) for x,y in product(hexagon,repeat=2)]
    if max(checks)!=1:raise ValueError('projected l1 hexagon determinant bound')
    return {'status':'exact_height_rank_and_determinant_certificate','beta':str(BETA),
            'classes':records,'universal_determinant_identities':symbolic_identities(),
            'hexagon_vertices':hexagon,'hexagon_determinants':checks,
            'scope':'Analytic rank stability and exact height-volume lifting. No width class is eliminated and no solver query is run.'}


def main():
    data=build()
    (ROOT/'certificates/height_rank_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'classes':data['classes'],
                      'universal_identities':len(data['universal_determinant_identities'])}))


if __name__=='__main__':main()
