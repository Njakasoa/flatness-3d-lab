# Additional widths required by the known determinant-five witnesses

Status: exact finite-witness analysis, 2026-09-14. These statements concern
five archived examples and their contact-symmetry images only. They neither
prove a sufficient global set of width constraints nor exclude a contact class.

For P=conv(0,(5,1,2),e2,e3), the complete target list consists of the fifteen
primitive covectors, modulo sign, of contact width at most three. All omitted
primitive covectors already have width at least four on P, hence on every
containing K. Enumerating the list is complete because contact width at most
three implies |uY|,|uZ|<=3 and |5uX+uY+2uZ|<=3, giving |uX|<=2.

The four affine lattice contact automorphisms are derived by checking all
24 contact permutations. Their action on covectors gives five orbits:

| Contact width | Covectors, modulo sign | Linear rank |
|---|---|---|
| 1 | (0,1,0) | 1 |
| 2 | (0,0,1), (0,1,-1), (1,-2,-2), (1,-1,-2) | 3 |
| 3 | (0,1,1), (0,2,-1), (1,-3,-2), (1,0,-2) | 3 |
| 3 | (1,-3,-1), (1,-2,-3), (1,-1,-1), (1,0,-3) | 3 |
| 3 | (1,-2,-1), (1,-1,-3) | 2 |

The [new stdlib-only replay](../tests/replay_det5_known_width_obstructions.py)
reconstructs each body directly from its archived contact matrix F. It
computes all fifteen widths exactly for the strong one-direction witness,
the earlier symmetry witness, and the three retained witnesses. It also
computes every contact-symmetry image, giving 20 labeled samples and 16
geometrically distinct bodies: the first two witnesses share an orbit.
The [JSON table](../results/det5_known_width_obstructions.json) records all
300 rational widths, input hashes, group actions, extrema, small directions,
and finite minimum-cardinality set covers. No previous file is changed,
no solver is called, and no prior hollowness or gauge audit is rerun.

## In the archived orientations, Z eliminates every known survivor

Let Y=(0,1,0), U=(1,-1,-2), and Z=(0,0,1). Among the archived orientations,
the strong one-direction witness already fails the U-width target. The other
four satisfy Y-width>17/5 and U-width>17/5, but fail Z-width>17/5. Z is the
unique single additional covector from the fifteen-direction list that
eliminates all four. In particular it eliminates the three retained examples.

The vectors Y,U,Z have rank three and determinant -1. This does not establish
that their width constraints imply the remaining twelve constraints. Width
is subadditive, and lower bounds in basis directions do not generally give
lower bounds in other directions.

## Symmetry images require a separate scope check

If all contact-symmetry images are included, Z alone no longer eliminates
all samples satisfying the Y/U targets. The first retained witness illustrates
why. Under contact permutation (2,0,3,1), its Y, U and Z widths are respectively

    160418300/26445567,
    162773620/26445567,
    237541900/26445567,

all above 17/5, but its sole small covector in the complete list is
(1,-2,-2). Under permutation (3,2,1,0), its sole small covector is (0,1,-1).
Its original orientation has sole small covector Z. These three samples
force every one of the three added covectors in any cover using this list.

Consequently the unique smallest addition eliminating every known symmetry
image that passes Y/U is

    Z, (0,1,-1), (1,-2,-2).

Together with U this completes the contact-width-two orbit. Together with Y
these are all five covectors of contact width at most two. This is a finite
sample cover, not a proof that these five suffice for all hollow tetrahedra.

There is an essential qualification: the five known symmetry images that
survive Y/U/Z are all **outside the retained Y-extrema representatives**.
The replay restores contact/facet labels after each automorphism: if the
contact permutation is pi, the transformed vertex g(v_i) receives label
pi(i). It then computes actual minimum and maximum indices and tests the
retained representatives (0,1), (0,3), (1,0), including all tied choices.
Only the three original retained witnesses survive Y/U in this retained
subcollection. Thus Z still eliminates every *known retained-chart* example,
even after inspecting the full contact-symmetry orbits.

It would be incorrect to claim that these unretained images refute a
Y/U/Z model on the retained charts. Equally, eliminating the known retained
examples proves no universal sufficiency of that model. The full fifteen
width constraints remain the available complete formulation.

Reproduction: `python3 tests/replay_det5_known_width_obstructions.py`.
Exact reconstruction identities, covector pullbacks and complete finite
set-cover enumeration verify the tables and their stated scopes.
