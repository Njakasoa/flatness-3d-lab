#!/usr/bin/env python3
"""Fail-fast project replay. Add --discovery to regenerate numerical observations."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    if sys.flags.optimize:
        raise SystemExit('Replay requires assertions: do not run Python with -O or -OO')
    parser=argparse.ArgumentParser();parser.add_argument('--discovery',action='store_true');args=parser.parse_args()
    stages=[('environment',['-m','experiments.environment_audit']),
      ('baseline',['-m','experiments.baseline']),
      ('planar_control',['-m','experiments.planar_control']),
      ('upper_bound',['-m','experiments.replay_upper_bound']),
      ('local_hessian',['-m','experiments.replay_local_hessian']),
      ('contact_enumeration',['-m','enumeration.empty_tetrahedra']),
      ('truncation',['-m','experiments.truncation_control']),
      ('independent_replay',['tests/independent_replay.py']),
      ('tests',['-m','pytest','-q'])]
    if args.discovery:stages.append(('discovery',['-m','experiments.discovery']))
    stages += [('selected_exact_candidates',['-m','experiments.certify_discovery']),('figures',['-m','experiments.figures'])]
    env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['MPLCONFIGDIR']='/tmp/flatness-matplotlib'
    report={'status':'running','python':sys.version,'discovery_regenerated':args.discovery,'stages':[]}
    for name,argv in stages:
        print(f'Running {name}',flush=True);start=time.monotonic()
        done=subprocess.run([sys.executable,*argv],cwd=ROOT,env=env,capture_output=True,text=True)
        log=ROOT/'results'/f'validation_{name}.log';log.write_text((done.stdout+done.stderr).replace(str(ROOT) + '/', ''))
        report['stages'].append({'name':name,'returncode':done.returncode,'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(ROOT))})
        if done.returncode:
            report['status']='failed';(ROOT/'results/validation.json').write_text(json.dumps(report,indent=2)+'\n')
            print(done.stdout+done.stderr);raise SystemExit(done.returncode)
    report['status']='passed';(ROOT/'results/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('All exact replays, enumeration and tests passed.',flush=True)
if __name__=='__main__':main()
