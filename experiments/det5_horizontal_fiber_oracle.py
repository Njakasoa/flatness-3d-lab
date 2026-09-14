"""Exact rational QF_LRA compiler for a fixed six-parameter horizontal shape.

No implicit search: compiler functions construct statements; the bounded
driver records each new solver call once. All width constraints use exact
stored numerator coefficients, with positive-gap projective normalization.
Inherited exclusions remain part of the restricted residual domain even when
full_width=False. That mode omits fourteen widths from the global-target
relaxation; its exclusions do not follow from a weaker gauge list alone.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sys
import z3

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tests'))
from check_height_ethos import emit, sexps

SHAPE = ('low', 'high', 'c', 'e', 'r', 'u')
VECTORS = [(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),
           (2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1)]


def rational(value):
    value = Q(value)
    return z3.RealVal(f'{value.numerator}/{value.denominator}')


def coefficient(terms, shape):
    out = Q(0)
    for row in terms:
        term = Q(row['coefficient'])
        for value, exponent in zip(shape, row['powers']):
            term *= value**exponent
        out += term
    return out


def coordinates(v, point=False):
    x,y,z = map(Q, v)
    return [int(point)+2*x/5-y-z, x/5, y-x/5, z-2*x/5]


def statement(assertions):
    solver = z3.Solver(); solver.add(*assertions)
    commands = sexps('\n'.join(line.split(';',1)[0] for line in solver.to_smt2().splitlines()))
    return '(set-logic QF_LRA)\n'+'\n'.join(emit(c) for c in commands if c[0] not in ('check-sat', 'set-logic'))+'\n'


def compile_fiber(shape, order, beta=Q(183,500), full_width=True, volume_cuts=False):
    shape = tuple(map(Q, shape)); x,y,c,e,r,u = shape
    if order not in ('lt','gt') or not(0<=x<y<=1 and min(c,e,r,u)>0):
        raise ValueError('invalid ordered shape')
    path = ROOT/'certificates/det5_horizontal_fiber_structure.json'
    cert = json.loads(path.read_text())
    branch = next(v for v in cert['branches'] if v['order']==order)
    D = coefficient(cert['horizontal_determinant'], shape)
    if not D:
        raise ValueError('singular shape D=0')
    alpha,eta,rho = z3.Reals('alpha eta rho')
    def affine(row):
        return sum(rational(coefficient(row[name],shape))*v for name,v in zip(('alpha','eta','rho'),(alpha,eta,rho)))
    M = [[0]*4 for _ in range(4)]
    for row in branch['scaled_F_entries']:
        M[row['row']][row['column']] = affine(row)
    rows = [eta-rational(x)*rho-rational(y-x)*alpha==1,
            rho>0,alpha>0,alpha<rho,rho>rational('17/5')]
    rows += [M[i][j]>0 for i in range(4) for j in range(4) if i!=j]
    for v in VECTORS:
        ell = coordinates(v)
        image = [sum(M[i][j]*rational(ell[j]) for j in range(4)) for i in range(4)]
        rows.append(z3.Or(*[sum(image[i] for i in range(4) if mask&(1<<i))>rational(beta)*rho for mask in range(1,15)]))
    C = next(v for v in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if v['class_index']==5)
    for point in C['guards']:
        ell = coordinates(point,True)
        rows.append(z3.Or(*[sum(M[i][j]*rational(ell[j]) for j in range(4))<=0 for i in range(4)]))
    old = json.loads((ROOT/'results/det5_class5_y_cvc5_validation.json').read_text())
    extra = json.loads((ROOT/'results/det5_y_corner_enlarged_3_5.json').read_text())
    boxes = [v['box'] for v in old['leaves'] if v['extrema']==[0,3]]+[extra['box']]
    heights = [x,y] if order=='lt' else [y,x]
    for box in boxes:
        rows.append(z3.BoolVal(any(value<Q(lo) or value>Q(hi) for value,(lo,hi) in zip(heights,box))))
    directions = json.loads((ROOT/'results/det5_complete_geometry_validation.json').read_text())['directions']
    if full_width:
        numerators = {(row['coordinate'],*row['vertex_pair']):affine(row) for row in branch['coordinate_pair_numerators']}
        for v in directions:
            if v==[0,1,0]:
                continue
            gaps = [sum(v[k]*numerators[k,i,j] for k in range(3)) for i in range(4) for j in range(i)]
            rows.append(z3.Or(*[cut for g in gaps for cut in (5*g>rational(17*abs(D)), -5*g>rational(17*abs(D)))]))
    if volume_cuts:
        # Necessary only under the actual global target, not from finite gauges alone.
        if not full_width:
            raise ValueError('volume cuts require the global target')
        upper = Q(50000000,2042829)
        rows += [rho<rational(upper), eta>0, eta<rho,
                 rho<rational(upper*abs(D))]
    return (alpha,eta,rho), rows, {'shape':dict(zip(SHAPE,map(str,shape))),
            'order':order,'D':str(D),'beta':str(beta),'target':'17/5',
            'full_width':full_width,'volume_cuts':volume_cuts,
            'coefficient_certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'gauge_vectors':VECTORS,'excluded_rectangles':boxes}
