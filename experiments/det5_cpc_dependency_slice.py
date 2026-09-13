"""Lexically resolve CPC occurrences and slice an existing refutation.

No solver calls. Slicing is exploratory until the emitted proof is externally
checked against a matching subset input. Original proof bytes remain unchanged.
"""
from pathlib import Path
import gzip,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from check_height_ethos import sexps,emit,sha,need
ROOT=Path(__file__).resolve().parents[1]

def tokens(e):
 if isinstance(e,str):yield e
 else:
  for x in e:yield from tokens(x)

def slice_proof(raw):
 cmds=sexps(raw.decode())[0];env={};stack=[];nodes=[];pushes=[];pop_to_push={}
 for index,c in enumerate(cmds):
  head=c[0];need(head in('declare-const','define','assume','assume-push','step','step-pop'),'known command')
  if head=='declare-const':nodes.append({'command':c,'dependencies':set(),'depth':len(stack)});continue
  # Resolve against active bindings before defining this occurrence.
  deps={env[t]for t in tokens(c[2:])if t in env};deps.update(pushes)
  node={'command':c,'dependencies':deps,'depth':len(stack)};nodes.append(node)
  if head=='assume-push':
   stack.append(env.copy());pushes.append(index);env=env.copy();env[c[1]]=index
  elif head=='step-pop':
   need(stack,'scope underflow');push=pushes.pop();pop_to_push[index]=push;env=stack.pop();env[c[1]]=index
  else:env[c[1]]=index
 need(not stack and cmds[-1][:1]==['step']and cmds[-1][2]=='false','closed final refutation')
 used=set();todo=[len(nodes)-1]
 while todo:
  n=todo.pop()
  if n in used:continue
  used.add(n);todo.extend(nodes[n]['dependencies'])
 # Needed scoped steps must retain their enclosing discharge and opening.
 # Final dependency closure normally already includes discharges. Explicitly
 # retain paired scope shells if an opening is used, then close again.
 changed=True
 while changed:
  changed=False
  for pop,push in pop_to_push.items():
   if push in used and pop not in used:used.add(pop);todo.extend(nodes[pop]['dependencies']);changed=True
  while todo:
   n=todo.pop()
   if n not in used:used.add(n);todo.extend(nodes[n]['dependencies']);changed=True
 kept=[c for i,c in enumerate(cmds)if i in used or c[0]=='declare-const']
 # Keep only definitions in the dependency closure; all uses resolve above.
 global_assumptions=[(i,n['command'])for i,n in enumerate(nodes)if n['command'][0]=='assume']
 return cmds,nodes,used,kept,global_assumptions

def main():
 path=ROOT/'certificates/det5_scaled_leaf_contact_width_two.cpc.gz';packed=path.read_bytes();raw=gzip.decompress(packed)
 cmds,nodes,used,kept,assumptions=slice_proof(raw)
 text='(\n'+'\n'.join(emit(c)for c in kept)+'\n)\n';dest=ROOT/'certificates/det5_scaled_box_sliced.cpc.gz';dest.write_bytes(gzip.compress(text.encode(),mtime=0))
 record={'scope':'Lexical dependency slice of an existing CPC refutation; not accepted as a proof until external replay. No solver call.','source_path':str(path.relative_to(ROOT)),'source_sha256':sha(raw),'source_commands':len(cmds),'sliced_commands':len(kept),'top_assumptions':len(assumptions),'retained_assumption_count':sum(i in used for i,c in assumptions),'retained_assumptions':[c[1]for i,c in assumptions if i in used],'omitted_assumptions':[c[1]for i,c in assumptions if i not in used],'sliced_path':str(dest.relative_to(ROOT)),'sliced_proof_sha256':sha(text.encode()),'solver_queries_run':0}
 (ROOT/'results/det5_cpc_dependency_slice.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k]for k in('source_commands','sliced_commands','top_assumptions','retained_assumption_count')}))

if __name__=='__main__':main()
