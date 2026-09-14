"""Combine separated-height queue and certified anchor rectangle, without solvers."""
from copy import deepcopy
import gzip
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'results/det5_separated_residual_queue.json'
ANCHOR = 'results/det5_strong_anchor_rectangle.json'
GEOMETRY = 'results/det5_strong_anchor_rectangle_validation.json'
KERNEL = 'results/det5_strong_anchor_rectangle_ethos_validation.json'
OUTPUT = 'results/det5_combined_residual_queue.json'
BOX = [['0','1/256'],['31/256','33/256']]


def read(path): return json.loads((ROOT/path).read_text())
def sha(path): return sha256((ROOT/path).read_bytes()).hexdigest()
def binding(path): return {'path':path,'sha256':sha(path)}


def main():
    old,row,geometry,kernel = map(read,(SOURCE,ANCHOR,GEOMETRY,KERNEL))
    assert old['status']=='READY' and old['target']=='17/5' and old['entry_count']==len(old['entries'])==258
    assert row['status']=='unsat' and row['internal_complete_proof_check']
    assert row['target']=='17/5' and row['extrema']==[0,3] and row['box']==BOX
    assert geometry['status']==kernel['status']=='PASS'
    assert geometry['source_archive_sha256']==sha(ANCHOR)
    assert geometry['external_proof_receipt_sha256']==sha(KERNEL)
    assert row['input_sha256']==sha(row['input_path'])==geometry['input_sha256']==kernel['input_sha256']
    assert row['proof_sha256']==sha256(gzip.decompress((ROOT/row['proof_path']).read_bytes())).hexdigest()==geometry['proof_sha256']==kernel['proof_sha256']
    assert kernel['ethos']['exit_code']==0 and kernel['ethos']['stdout']=='correct' and not kernel['ethos']['stderr']
    clause = {
        'certified_leaf':'0_3:strong_anchor_rectangle',
        'excluded_closed_Y_box':BOX,
        'proof_input_path':row['input_path'], 'proof_receipt_path':KERNEL,
        'geometry_receipt_path':GEOMETRY,
        'literals':[
            {'free_coordinate':i,'vertex_index':i+1,'relation':relation,'threshold':BOX[i][endpoint]}
            for i in range(2) for relation,endpoint in (('<',0),('>',1))]}
    entries = deepcopy(old['entries'])
    amended = []
    for entry in entries:
        if entry['Y_extrema']==[0,3]:
            assert entry['free_Y_vertex_indices']==[1,2]
            entry['outside_Y_clauses'].append(deepcopy(clause))
            amended.append(entry['entry_id'])
    assert len(amended)==70
    output = {
        'status':'READY', 'target':'17/5', 'class_index':5,
        'scope':'Combined necessary residual domain for actual hollow determinant-five class-5 strict facet-contact tetrahedra with global lattice width >17/5. No complete coverage or whole-class exclusion.',
        'source_queue':binding(SOURCE),
        'new_rectangle_archive':binding(ANCHOR),
        'new_rectangle_geometry_audit':binding(GEOMETRY),
        'new_rectangle_kernel_receipt':binding(KERNEL),
        'new_rectangle_proof':binding(row['proof_path']),
        'boolean_semantics':old['boolean_semantics'],
        'coordinate_semantics':old['coordinate_semantics'],
        'inherited_measure_semantics':'All per-entry measure and overlap fields are preserved from the predecessor chain and describe their earlier rectangular domains only. They are not measures of this combined queue.',
        'entry_count':258,'entries':entries,
        'amended_entry_count':70,'amended_entry_ids':amended,'unchanged_entry_count':188,
        'newly_removed_entries':[],
        'removal_scope':'All258 entries conservatively retained; no assertion that individual refined entries are nonempty.',
        'new_excluded_closed_rectangle':{'Y_extrema':[0,3],'box':BOX,'area':'1/32768',
          'scope':'Entire rectangle is outside both the previous closed rectangle union and the excluded separated-height band; no total residual-area calculation.'},
        'solver_queries_run':0,'proof_kernel_calls_run':0}
    path = ROOT/OUTPUT
    if path.exists(): assert read(OUTPUT)==output, 'Existing queue differs; do not overwrite.'
    else: path.write_text(json.dumps(output,indent=2)+'\n')
    print('COMBINED_RESIDUAL_QUEUE=READY entries=258 appended=70 unchanged=188')


if __name__=='__main__':main()
