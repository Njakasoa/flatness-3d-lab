"""Bind verified height-cover exclusions to the original complete contact list."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]


def main():
    T=json.loads((ROOT/'certificates/contact_templates.json').read_text())
    C=json.loads((ROOT/'results/height_cover_cvc5_validation.json').read_text())
    E=json.loads((ROOT/'results/height_ethos_validation.json').read_text())
    A=json.loads((ROOT/'results/height_cover_encoding_validation.json').read_text())
    if not (C['status']==E['status']==A['status']=='PASS' and len(C['leaves'])==E['external_correct']==62):
        raise ValueError('incomplete proof chain')
    if hashlib.sha256((ROOT/'results/height_cover_cvc5_validation.json').read_bytes()).hexdigest()!=E['cvc5_receipt_sha256']:
        raise ValueError('external receipt is not bound to this cvc5 campaign')
    bindings=[]
    for idx,d,a in ((6,7,2),(7,8,3)):
        points=[[0,0,0],[d,1,a],[0,1,0],[0,0,1]]
        entry=next(r for r in T['embeddings'] if r['class_index']==idx)
        if entry['vertices']!=points:raise ValueError('contact type binding')
        bindings.append({'class_index':idx,'contact_points':points,'upper_bound':'17/5',
                         'scope':'Full four-point relative-interior facet-contact hull of a hollow real tetrahedron.'})
    remaining=[r['class_index'] for r in T['embeddings'] if r['class_index'] not in (6,7,8,9)]
    if len(remaining)!=59 or not set(range(10,63))<=set(remaining):raise ValueError('larger hulls or square removed')
    files=['certificates/contact_templates.json','results/height_interval_relaxation.json',
           'results/height_cover_encoding_validation.json','results/height_cover_cvc5_validation.json',
           'results/height_ethos_validation.json']
    result={'status':'verified_restricted_class_exclusions','new_exclusions':bindings,
            'excluded_full_tetrahedral_classes_at_candidate_width':[6,7,8,9],
            'surviving_full_contact_classes_at_width_ge_2_plus_sqrt2':remaining,
            'surviving_count_at_candidate_width':59,'surviving_count_above_original_c':62,
            'previous_exclusion_dependency':'CLAIM-0006: classes8,9 at candidate width; only9 above original c.',
            'evidence_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
            'scope':'No improved global Flt(3) bound. No deletion of larger hulls from tetrahedral subset containment. Novelty unconfirmed.'}
    (ROOT/'certificates/height_contact_exclusions.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: classes6,7 bound to62 externally checked refutations;59 necessary candidate contact hulls remain')


if __name__=='__main__':main()
