"""Independent symbolic review of the eight-parameter ordered height chart."""
import json
from pathlib import Path

import sympy as s


def main():
    x, y, t, h, c, e, r, u = s.symbols("x y t h c e r u")
    d = y-x
    a = x+t*d
    b = h-a
    F = s.Matrix([
        [0, 1-h-(1-y)*r, 1-h-(1-x)*u, d*e],
        [1-t+(1-y)*c, 0, u, 1-t-y*e],
        [t-(1-x)*c, r, 0, t+x*e],
        [d*c, h-y*r, h-x*u, 0],
    ])
    one = s.ones(4, 1)
    H = s.Matrix([0, 1, 1, 0])
    q = s.Matrix([0, x, y, 1])
    A, B = (1-x)*c+x*e, (1-y)*c+y*e
    D = u*A-r*B
    checks = 0

    def zero(expr):
        nonlocal checks
        assert s.expand(expr) == 0, expr
        checks += 1

    for expr in F.T*one-one:
        zero(expr)
    for expr in F.T*q-a*one-b*H:
        zero(expr)
    zero(s.cancel(F.det())-b*D)
    for expr in F[:, 3]-F[:, 0]-s.Matrix([d*e, -B, A, -d*c]):
        zero(expr)
    zero(d*e+A-(y*e+(1-x)*c))
    S = s.eye(4)
    S.row_swap(1, 2)
    G = S*F*S
    for expr in G.T*s.Matrix([0, y, x, 1])-a*one-b*H:
        zero(expr)
    zero(s.cancel(G.det())-b*D)
    for expr in [(a-x)/d-t, F[3, 0]/d-c, F[0, 3]/d-e,
                 F[2, 1]-r, F[1, 2]-u]:
        zero(s.cancel(expr))

    fixture = {x:s.Rational(1,4), y:s.Rational(3,4), t:s.Rational(1,2),
               h:s.Rational(3,5), c:s.Rational(1,5), e:s.Rational(1,5),
               r:s.Rational(1,5), u:s.Rational(1,5)}
    M = F.subs(fixture)
    assert all(M[i,j]>0 for i in range(4) for j in range(4) if i!=j)
    assert b.subs(fixture)==s.Rational(1,10)
    assert M.det()==0
    gauges=[]
    for X,Y,Z in [(1,0,0),(2,0,1),(1,0,1),(3,0,1)]:
        ell=s.Matrix([s.Rational(2,5)*X-Y-Z, s.Rational(1,5)*X,
                      Y-s.Rational(1,5)*X, Z-s.Rational(2,5)*X])
        gauges.append(str(sum(abs(v) for v in M*ell)/2))
    assert gauges==["3/50", "9/50", "6/25", "3/25"]
    result={"status":"PASS", "symbolic_identities":checks,
            "branch_count":2, "positive_singular_fixture":True,
            "singular_fixture_gauges":gauges, "solver_queries":0,
            "scope":"Exact chart identities and singularity control; no width exclusion."}
    path=Path(__file__).resolve().parents[1]/"results/det5_rational_height_chart_review_validation.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
