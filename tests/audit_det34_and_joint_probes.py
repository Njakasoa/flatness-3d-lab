"""Read-only mathematical encodings, SAT pins and provenance for bounded probes."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import z3
from audit_height_cover_independent import need,expected_assertions,compare
from audit_det5_height_independent import geometry
from audit_det5_joint_cover_independent import formula

ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads((ROOT/path).read_text())


def main():
    guards={c['class_index']:c for c in read('certificates/nonunimodular_observer_guards.json')['classes']}
    scans={c['class_index']:c for c in read('results/two_vector_class_scan.json')['classes']}
    data=read('results/det34_height_roots.json');seen=set();sat_pins=0
    for c in data['classes']:
        idx=c['class_index'];full,group,orbits=geometry(guards[idx]['contact_points'])
        need(c['full_automorphisms']==full and c['height_automorphisms']==group and c['extrema_orbits']==orbits,'independent d3/d4 symmetry group and all extrema')
        wanted={tuple(orb[0]) for orb in orbits}
        rows=[r for r in data['queries'] if r['class_index']==idx]
        need(len(rows)==len(wanted) and {tuple(r['extrema']) for r in rows}==wanted,'complete root chart list')
        for row in rows:
            key=(idx,tuple(row['extrema']));need(key not in seen,'unique root');seen.add(key)
            need(row['box']==[['0','1'],['0','1']],'whole unit square')
            p=ROOT/row['path'];need(hashlib.sha256(p.read_bytes()).hexdigest()==row['input_sha256'],'root input hash')
            expected,gauges,_=expected_assertions(guards[idx],scans[idx],row['extrema'],[[Q(0),Q(1)]]*2)
            expected += [z3.substitute(g,(z3.RealVal('37/102'),z3.RealVal('183/500'))) for g in gauges]
            actual=list(z3.parse_smt2_file(str(p)));compare(expected,actual)
            need(row['status']=='sat','archived root SAT status')
            pin=[(z3.Real(k),z3.RealVal(v)) for k,v in row['relaxed_assignment'].items()]
            need(all(z3.is_true(z3.simplify(z3.substitute(e,*pin))) for e in actual),'exact satisfying relaxed assignment')
            sat_pins+=1
    probe=read('results/det5_retained_joint_probe.json')
    for p,h in probe['sources_sha256'].items():need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'fixed probe source')
    old=read('results/det5_joint_fibers.json')['queries']
    oldkeys={(tuple(r['Y_extrema']),tuple(r['U_extrema']),tuple(map(Q,r['midpoint']))) for r in old}
    keys=set()
    for row in probe['queries']:
        key=(tuple(row['Y_extrema']),tuple(row['U_extrema']),tuple(map(Q,row['midpoint'])))
        need(key not in keys and key not in oldkeys,'new distinct exact fiber');keys.add(key)
        need(key[0]==(1,0) and key[2][:2]==(Q(5,16),Q(1,8)),'retained fixed Y chart')
        adapted=dict(row,box=[[x,x] for x in row['midpoint']])
        compare(formula(guards[5],scans[5],adapted),list(z3.parse_smt2_file(str(ROOT/row['path']))))
    out={'status':'PASS','det34_exact_relaxed_SAT_pins':sat_pins,'new_joint_fibers':len(keys),
         'solver_queries_run':0,'scope':'Independent encodings, exact relaxed SAT witnesses, and point-fiber provenance. Joint UNSAT labels not proof-checked; no continuous-class exclusion.'}
    (ROOT/'results/det34_and_joint_probe_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
