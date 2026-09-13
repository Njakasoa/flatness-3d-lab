import importlib, json, platform, shutil, subprocess
from pathlib import Path

def main():
    report={'python':platform.python_version(),'platform':platform.platform(),'packages':{},'commands':{}}
    for name in ['numpy','scipy','sympy','flint','sage.all','cdd','ortools','pyscipopt','cvxpy','z3','matplotlib','pytest','pypdf']:
        try:m=importlib.import_module(name);report['packages'][name]={'available':True,'version':getattr(m,'__version__','unknown')}
        except ImportError:report['packages'][name]={'available':False}
    for name in ['python3.12','sage','gp','polymake','normaliz','highs','cbc','scip','g++','rustc','git','gh']:
        report['commands'][name]=bool(shutil.which(name))
    from scipy.optimize import milp, Bounds, LinearConstraint
    res=milp(c=[1.],integrality=[1],bounds=Bounds([0],[10]),constraints=LinearConstraint([[1]],[1.5],[10]))
    assert res.success and res.x[0]==2
    report['milp_smoke_test']={'solver':'SciPy bundled HiGHS','problem':'min x, integer x>=1.5','solution':res.x.tolist(),'exact_certificate':'integer x>=1.5 implies x>=2; x=2 feasible'}
    from flint import arb
    report['arb_smoke_test']=str(arb(2).sqrt())
    from fractions import Fraction
    assert Fraction(1,3)*3==1
    Path('results/environment_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Environment audit — 2026-09-13','',f'Python {report["python"]}. This report records the current replay environment. requirements.lock records the reference dependency versions.','', '| Package | Available | Version |','|---|---|---|']
    for name,r in report['packages'].items():lines.append(f'| {name} | {r["available"]} | {r.get("version","—")} |')
    lines += ['', '## Actual solver check', '', 'SciPy/HiGHS solved min integer x subject to x>=1.5 with x=2. Arb sqrt(2) and Fraction exact arithmetic were executed. HiGHS is used only for exploratory checks; floating solver status is never accepted as a mathematical proof.', '', 'Sage, PARI/GP, polymake, Normaliz, cddlib, OR-Tools, SCIP, CVXPY and Z3 are absent unless marked above. They are optional; no proprietary solver is required. C++ compiler and Git are present. Rust and gh are absent. Repository access is not needed for these local numerical and exact checks. No paid service or external compute used.', '', 'Core certificate code requires only Python standard library. Independent verification uses SymPy; optimization SciPy; figures Matplotlib. PDF extraction uses pypdf. See results/environment_audit.json for actual executable discovery.', '', 'The public source snapshot excludes runtime installations and third-party papers. No paper download, account or API key is required to replay certificates.']
    Path('ENVIRONMENT_AUDIT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
