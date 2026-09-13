# Environment audit — 2026-09-13

Python 3.12.3. This report records the current replay environment. requirements.lock records the reference dependency versions.

| Package | Available | Version |
|---|---|---|
| numpy | True | 2.5.3 |
| scipy | True | 1.18.1 |
| sympy | True | 1.14.0 |
| flint | True | 0.9.0 |
| sage.all | False | — |
| cdd | False | — |
| ortools | False | — |
| pyscipopt | False | — |
| cvxpy | False | — |
| z3 | False | — |
| matplotlib | True | 3.11.2 |
| pytest | True | 9.1.1 |
| pypdf | True | 6.18.1 |

## Actual solver check

SciPy/HiGHS solved min integer x subject to x>=1.5 with x=2. Arb sqrt(2) and Fraction exact arithmetic were executed. HiGHS is used only for exploratory checks; floating solver status is never accepted as a mathematical proof.

Sage, PARI/GP, polymake, Normaliz, cddlib, OR-Tools, SCIP, CVXPY and Z3 are absent unless marked above. They are optional; no proprietary solver is required. C++ compiler and Git are present. Rust and gh are absent. Repository access is not needed for these local numerical and exact checks. No paid service or external compute used.

Core certificate code requires only Python standard library. Independent verification uses SymPy; optimization SciPy; figures Matplotlib. PDF extraction uses pypdf. See results/environment_audit.json for actual executable discovery.

The public source snapshot excludes runtime installations and third-party papers. No paper download, account or API key is required to replay certificates.
