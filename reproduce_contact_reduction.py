#!/usr/bin/env python3
"""Reproduce the internally verified contact reduction, separate from the baseline."""
import json,os,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    if sys.flags.optimize:raise SystemExit('Assertions required; do not use -O/-OO')
    stages=[
       ('enumeration21',['-m','enumeration.empty_tetrahedra','--max-determinant','21','--output','results/empty_tetrahedra_through_21.json']),
       ('tetrahedron_minima',['-m','experiments.contact_obstructions']),
       ('contact_extensions',['-m','enumeration.contact_extensions']),
       ('contact_hull_minima',['-m','experiments.contact_hull_obstructions']),
       ('contact_templates',['-m','experiments.contact_templates']),
       ('independent_contact_replay',['tests/replay_contact_minima_independent.py']),
       ('square_contacts',['-m','experiments.square_contacts']),
       ('contact_figures',['-m','experiments.contact_reduction_figures'])]
    env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['MPLCONFIGDIR']='/tmp/flatness-matplotlib'
    report={'status':'running','stages':[]}
    for name,argv in stages:
        print('Running '+name,flush=True);start=time.monotonic()
        result=subprocess.run([sys.executable,*argv],cwd=ROOT,env=env,capture_output=True,text=True)
        log=ROOT/'results'/('validation_'+name+'.log');log.write_text((result.stdout+result.stderr).replace(str(ROOT)+'/', ''))
        report['stages'].append({'name':name,'returncode':result.returncode,'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(ROOT))})
        if result.returncode:
            report['status']='failed';(ROOT/'results/contact_reduction_replay.json').write_text(json.dumps(report,indent=2)+'\n')
            print(result.stdout+result.stderr);raise SystemExit(result.returncode)
    report['status']='passed';(ROOT/'results/contact_reduction_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Contact reduction replay passed.',flush=True)

if __name__=='__main__':main()
