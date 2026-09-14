"""Independent exact polynomial/interval audit; imports no queue generator."""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = 'results/det5_separated_residual_queue.json'
OLD = 'results/det5_enlarged_residual_queue.json'
CERT = 'results/det5_class5_y_cvc5_validation.json'
OUT = 'results/det5_separated_residual_queue_validation.json'


def read(p):
    return json.loads((ROOT/p).read_text())


def hashfile(p):
    return sha256((ROOT/p).read_bytes()).hexdigest()


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def polynomial(terms):
    result = {}
    for c,i,j in terms:
        need(type(c)==type(i)==type(j)==int and i>=0 and j>=0,'integer polynomial')
        result[i,j] = result.get((i,j),Q(0))+c
    return {k:v for k,v in result.items() if v}


def validate(data):
    old = read(OLD)
    need(data['source_queue']=={'path':OLD,'sha256':hashfile(OLD)},'source binding')
    for source in data['analytic_sources']:
        need(hashfile(source['path'])==source['sha256'],'analytic source binding')
    need(data['target']=='17/5' and data['class_index']==5,'target unchanged')
    need(data['entry_count']==len(data['entries'])==len(old['entries'])==258,'complete queue')
    amended = []
    for prior,current in zip(old['entries'],data['entries']):
        copied = deepcopy(current)
        cuts = copied.pop('additional_necessary_constraints',None)
        need(copied==prior,'every predecessor entry value preserved')
        if prior['Y_extrema']!=[0,3]:
            need(cuts is None,'other charts unchanged')
            continue
        amended.append(prior['entry_id'])
        need(prior['free_Y_vertex_indices']==[1,2],'height coordinate identification')
        need(len(cuts)==1,'one new necessity')
        cut = cuts[0]
        need(cut['operator']=='OR' and len(cut['branches'])==2,'two-branch disjunction')
        need(cut['variables']==[{'name':'q1','free_coordinate':0,'vertex_index':1},
                               {'name':'q2','free_coordinate':1,'vertex_index':2}], 'variable substitution')
        for index,branch in enumerate(cut['branches']):
            delta = Q(49,1500) if index==0 else Q(249,1700)
            need(Q(branch['delta'])==delta and branch['operator']=='AND','branch threshold')
            need(branch['order']==('q1<q2' if index==0 else 'q1>q2'),'branch labels')
            ps = branch['strict_positive_polynomials']
            need(len(ps)==2,'order and separation both strict')
            order = {(1,0):Q(-1),(0,1):Q(1)} if index==0 else {(1,0):Q(1),(0,1):Q(-1)}
            need(polynomial(ps[0])==order,'strict order polynomial')
            # Derive gap-delta*M*(1-m) independently as a rational polynomial.
            expression = dict(order)
            large = (0,1) if index==0 else (1,0)
            expression[large] -= delta
            expression[1,1] = delta
            cleared = {k:v*delta.denominator for k,v in expression.items()}
            need(polynomial(ps[1])==cleared,'strict separated-height polynomial')
    need(data['amended_entry_ids']==amended and len(amended)==data['amended_entry_count']==70,'all70 target entries')
    need(data['unchanged_entry_count']==188 and data['newly_removed_entries']==[],'no entry removal claimed')
    rectangle = data['new_excluded_closed_rectangle']
    (xl,xh),(yl,yh) = [[Q(v) for v in interval] for interval in rectangle['box']]
    need(0<=xl<xh<yl<yh<Q(1,4),'positive rectangle strictly ordered below1/4')
    maxgap = yh-xl
    lower = Q(49,1500)*yl*(1-xh)
    need(maxgap<lower,'universal interval exclusion, all closed endpoints')
    need(Q(rectangle['area'])==(xh-xl)*(yh-yl)==Q(1,1000000),'positive exact area')
    need(Q(rectangle['maximum_gap'])==maxgap and Q(rectangle['minimum_delta_product_bound'])==lower,'exact interval bounds')
    need(Q(rectangle['strict_margin'])==lower-maxgap,'strict positive margin')
    cert = read(CERT)
    need(old['old_certified_Y_proofs']['path']==CERT and old['old_certified_Y_proofs']['sha256']==hashfile(CERT),'old certified boxes binding')
    prior_rectangles = [l['box'] for l in cert['leaves'] if l['extrema']==[0,3]]
    prior_rectangles.append(old['new_certified_Y_proof']['box'])
    need(len(prior_rectangles)==8,'complete previous Y03 rectangle union')
    for box in prior_rectangles:
        disjoint = any(Q(b)<lo or hi<Q(a) for (a,b),(lo,hi) in zip(box,((xl,xh),(yl,yh))))
        need(disjoint,'rectangle wholly disjoint from previous closed union')
    # Exhibit actual preceding residual boxes containing the entire new rectangle,
    # including satisfaction of their strict complements at every rectangle point.
    containing = []
    for entry in old['entries']:
        if entry['Y_extrema']!=[0,3]: continue
        if not all(Q(a)<=lo<=hi<=Q(b) for (a,b),(lo,hi) in zip(entry['box'],((xl,xh),(yl,yh)))):continue
        for clause in entry['outside_Y_clauses']:
            uniformly_true = False
            for literal in clause['literals']:
                lo,hi = ((xl,xh),(yl,yh))[literal['free_coordinate']]
                threshold = Q(literal['threshold'])
                uniformly_true |= (hi<threshold if literal['relation']=='<' else lo>threshold)
            need(uniformly_true,'all old strict clauses hold throughout rectangle')
        containing.append(entry['entry_id'])
    need(len(containing)==8,'positive-area cut lies in eight preceding residual projections')
    return containing


def main():
    data = read(NEW)
    containing = validate(data)
    mutations = []
    for kind in ('lost_entry','weakened_polynomial','changed_old_bound'):
        bad = deepcopy(data)
        if kind=='lost_entry': bad['entries'].pop()
        elif kind=='changed_old_bound': bad['entries'][0]['box'][0][0]='-1'
        else:
            e = next(e for e in bad['entries'] if e['Y_extrema']==[0,3])
            e['additional_necessary_constraints'][0]['branches'][0]['strict_positive_polynomials'][1][0][0]+=1
        try: validate(bad)
        except AssertionError: mutations.append(kind)
        else: raise AssertionError('mutation accepted: '+kind)
    result = {'status':'PASS','source_queue':{'path':NEW,'sha256':hashfile(NEW)},
              'predecessor_queue':{'path':OLD,'sha256':hashfile(OLD)},
              'entries_preserved':258,'entries_refined':70,'other_chart_entries_unchanged':188,
              'exact_branches_per_refined_entry':2,'new_rectangle_area':'1/1000000',
              'previous_residual_entries_containing_whole_rectangle':containing,
              'universal_rectangle_method':'Exact interval bounds and disjoint closed boxes; no sampling or grid coverage.',
              'mutation_controls_rejected':mutations,'solver_queries_run':0,
              'scope':'Encoding and rigorous interval audit; analytic source proofs retain their stated scope. No updated total area or complete coverage proof.'}
    (ROOT/OUT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
