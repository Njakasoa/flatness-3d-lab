"""Independent SymPy replay of the serialized pair-matrix certificate."""
import copy
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['k0', 'k1', 'k2', 'k3', 'e02', 'e03', 'e12', 'e13',
         'e20', 'e21', 'e30', 'e31']
VARS = s.symbols(' '.join(NAMES))
SIGMA = (1, 0, 3, 2)


def require(value, message):
    if not value:
        raise ValueError(message)


def polynomial(terms):
    require(bool(terms), 'empty polynomial')
    seen = set()
    expression = 0
    for term in terms:
        powers, coefficient = term['powers'], term['coefficient']
        require(len(powers) == 12 and all(type(x) is int and x >= 0 for x in powers),
                'invalid exponent vector')
        require(type(coefficient) is int and coefficient > 0, 'invalid coefficient')
        require(tuple(powers) not in seen, 'duplicate monomial')
        seen.add(tuple(powers))
        expression += coefficient * s.prod(v ** p for v, p in zip(VARS, powers))
    return s.Poly(expression, *VARS)


def formal_replay(c):
    require(c['variables'] == NAMES, 'variable order mismatch')
    adj_terms = c['adjugate_terms']
    require(len(adj_terms) == 4 and all(len(row) == 4 for row in adj_terms),
            'missing adjugate entry')
    variables = dict(zip(NAMES, VARS))
    matrix = s.zeros(4)
    for i in range(4):
        matrix[i, i] = variables[f'k{i}']
        for j in range(4):
            if (i < 2) != (j < 2):
                edge = variables[f'e{i}{j}']
                matrix[i, i] += edge
                matrix[i, j] = -edge
    determinant = polynomial(c['determinant_terms'])
    require(determinant == s.Poly(matrix.det(), *VARS), 'determinant mismatch')
    require(len(determinant.terms()) == 45, 'determinant term count')
    require(all(sum(m[:4]) > 0 for m in determinant.monoms()), 'root-free determinant')
    counts = [sum(m[i] == 1 and sum(m[:4]) == 1 for m in determinant.monoms())
              for i in range(4)]
    require(counts == c['one_root_spanning_tree_counts'] == [4] * 4, 'root counts')
    expected_adj = matrix.adjugate()
    replayed_adj = s.zeros(4)
    for i, j in itertools.product(range(4), repeat=2):
        entry = polynomial(adj_terms[i][j])
        require(entry == s.Poly(expected_adj[i, j], *VARS), 'adjugate mismatch')
        require(any(not any(m[:4]) for m in entry.monoms()), 'missing edge-only term')
        replayed_adj[i, j] = entry.as_expr()
    require(all(s.expand(x) == 0 for x in
                matrix * replayed_adj - determinant.as_expr() * s.eye(4)),
            'adjugate product mismatch')


def boundary_and_symmetry(c):
    permutation = s.eye(4)[:, list(SIGMA)]
    signature = s.diag(1, 1, -1, -1)
    require(permutation.det() == 1, 'permutation orientation')
    for mask in range(16):
        a = s.zeros(4)
        for i in range(4):
            designated = s.Rational(3, 4) if mask >> i & 1 else s.Rational(1, 2)
            a[i, SIGMA[i]] = designated
            for j in range(4):
                if (i < 2) != (j < 2):
                    a[i, j] = (1 - designated) / 2
        require(bool(a.det() > 0) == bool(mask), 'boundary determinant')
        if mask:
            inverse = a.inv()
            require(all(s.sign(inverse[i, j]) == (1 if (i < 2) == (j < 2) else -1)
                        for i, j in itertools.product(range(4), repeat=2)), 'inverse signs')
            m = signature * a * permutation * signature
            require(inverse == permutation * signature * m.inv() * signature,
                    'inverse orientation')
        else:
            require(a.rank() == 3, 'all-half rank')
    group = [p for p in itertools.permutations(range(4))
             if all(p[SIGMA[i]] == SIGMA[p[i]] for i in range(4))]
    require(len(group) == 8 and sorted(map(tuple, c['contact_permutation_centralizer'])) == group,
            'centralizer mismatch')
    for ranks in itertools.product(range(4), repeat=4):
        require(any(ranks[p[0]] == max(ranks) and ranks[p[2]] >= ranks[p[3]]
                    for p in group), 'canonical weak order failure')
    points = list(map(s.Matrix, [(0, 0, 0), (2, 1, 1), (0, 1, 0), (0, 0, 1)]))
    basis = s.Matrix.hstack(*(points[i] - points[0] for i in range(1, 4)))
    for p in itertools.permutations(range(4)):
        linear = s.Matrix.hstack(*(points[p[i]] - points[p[0]] for i in range(1, 4))) * basis.inv()
        require(all(x.q == 1 for x in linear) and abs(linear.det()) == 1,
                'contact map not unimodular')


def main():
    certificate = json.loads((ROOT / 'certificates/pair_matrix_structure.json').read_text())
    formal_replay(certificate)
    boundary_and_symmetry(certificate)
    for corruption in ('coefficient', 'missing_entry'):
        altered = copy.deepcopy(certificate)
        if corruption == 'coefficient':
            altered['determinant_terms'][0]['coefficient'] += 1
        else:
            altered['adjugate_terms'][0].pop()
        try:
            formal_replay(altered)
        except ValueError:
            pass
        else:
            raise ValueError(f'failed to reject {corruption}')
    print('PASS: 45 determinant terms; 16 adjugates; 16 boundary masks; '
          '8 centralizers; 256 weak-rank tuples; 24 affine lattice maps; 2 corruption guards')


if __name__ == '__main__':
    main()
