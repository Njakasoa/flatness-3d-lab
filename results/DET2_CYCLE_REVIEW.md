# Independent determinant-two cycle review

`tests/replay_det2_cycle_independent.py` replays the supplied determinant-two
cycle certificates using only Python's standard-library `Fraction` arithmetic.
It imports no module from `src` and implements its own matrix inversion,
supporting-plane checks, integer-box enumeration, and primitive-direction
enumeration.

The replay passed for both available certificates:

| certificate | exact width | decimal width | minimizing direction representatives | integer points checked | boundary points |
| --- | --- | ---: | --- | ---: | ---: |
| `det2_cycle_rational.json` | `4320583268114594607881031741630319110755574/1315893928867311218381530956762804285589247` | 3.2833826293534504547 | `(0,1,1)` | 48 | 6 |
| `det2_four_contacts.json` | `4009295246418/1232189371865` | 3.2537979453188001711 | `(1,-1,-1)` | 48 | 4 |

For each certificate the replay verified the following exactly:

- the eight cycle parameters regenerate the stored rational facet matrix;
- the stored rational vertices regenerate from that matrix and the standard
  contact frame `0,(2,1,1),e2,e3`;
- all four supporting planes agree with the independently computed simplex
  facets, including orientation and contacts;
- the exact integer bounding box is `[-1,2] x [-1,1] x [-1,2]`, with no
  interior lattice points;
- the four designated contacts are relative-interior contacts on the four
  facets: `0` on facet `(1,2,3)`, `(2,1,1)` on `(0,2,3)`, `e2` on
  `(0,1,3)`, and `e3` on `(0,1,2)`;
- the stored difference-basis inverse gives coordinate bounds `[2,3,2]`;
  all 73 primitive direction representatives in that box were checked, and
  the stored width and minimizer set agree with the exact replay.

Three in-memory mutation guards were run for each certificate. Changing a
stored vertex was rejected by the vertex reconstruction, changing the claimed
width was rejected by the complete direction replay, and removing a listed
boundary point was rejected by exact-box enumeration.

The run was:

```text
python3 tests/replay_det2_cycle_independent.py
python3 -m py_compile tests/replay_det2_cycle_independent.py
```

The machine-readable result is
`results/det2_cycle_independent.json`.

This review certifies the supplied reconstructed tetrahedra and their finite
width/hollowness checks. It does not search the parameter space, establish
maximality, or assert local or global optimality. The width completeness
argument is per body and relies on the stated four-contact cycle chart; it is
not a uniform theorem for other bodies or contact configurations.

## Integrated claim checks

The root subsequently made both inputs mandatory and added a named claim
wrapper. It requires hollowness, the recorded exact width and exact contact
set, plus width>13/4 for the four-contact witness. The entrypoint rejects
substitution of the other self-consistent witness. Astra reviewed and closed
this scope issue in DET2_WITNESS_ASTRA_REVIEW.md. Both exact generators and
the independent replay passed together with unchanged certificate bytes; see
det2_witness_validation.json.
