"""Exact corollary arithmetic and hash-bound independent review of CLAIM-0010."""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-primary-text",action="store_true",help="Replay arithmetic and local bindings without the unredistributed primary article; does not repeat the primary-source review.")
    args=parser.parse_args()
    beta=Q(183,500)
    delta_lt=Q(49,1500)
    delta_gt=Q(249,1700)
    assert Q(1,3)+delta_lt==beta
    assert Q(1,5)+Q(17,15)*delta_gt==beta
    assert 1-beta==Q(317,500)
    assert Q(2,3)-delta_lt==Q(4,5)-Q(17,15)*delta_gt==1-beta
    assert Q(17,5)*(1-beta)==Q(5389,2500)
    radical_rhs=Q(5389,2500)-1
    assert radical_rhs>0 and Q(4,3)<radical_rhs**2
    assert 25000000<25038963
    assert Q(1,3)+Q(2,3)==1
    assert Q(1,5)+Q(17,15)*Q(12,17)==1
    with localcontext() as ctx:
        ctx.prec=60
        A=1+Decimal(2)/Decimal(3).sqrt()
        bound=Decimal(500)*A/Decimal(317)
        assert str(bound).startswith('3.398581290819008720849')
        assert bound<Decimal(17)/5
        bound_text=str(bound)
    endpoint_checks=0
    for den in (2,7,31):
        for lo in range(den):
            for hi in range(lo+1,den+1):
                x,y=Q(lo,den),Q(hi,den)
                L=(y-x)/(y*(1-x))
                assert 0<L<=1
                assert y*(1-x)-(y-x)==x*(1-y)
                assert (L==1)==(x==0 or y==1)
                for delta in (delta_lt,delta_gt):
                    assert (L>delta)==(y-x>delta*y*(1-x))
                    assert (L<=delta)==(y-x<=delta*y*(1-x))
                endpoint_checks+=1
    source_paths=[
        'claims/CLAIM-0010.md',
        'proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md',
        'proofs/DET5_CLAIM0010_INDEPENDENT_REVIEW.md',
        'results/det5_compact_shape_chart_validation.json',
        'results/det5_separated_residual_queue_validation.json',
        'papers/ACMS-1907.06199.txt',
    ]
    if args.skip_primary_text:
        source_paths=source_paths[:-1]
    sources=[{'path':p,'sha256':sha256((ROOT/p).read_bytes()).hexdigest()} for p in source_paths]
    compact=json.loads((ROOT/source_paths[3]).read_text())
    queue=json.loads((ROOT/source_paths[4]).read_text())
    assert compact['status']=='PASS' and compact['guard_equivalence_checks']==9600
    assert queue['status']=='PASS' and queue['entries_preserved']==258
    assert queue['entries_refined']==70 and queue['other_chart_entries_unchanged']==188
    claim=(ROOT/source_paths[0]).read_text()
    assert '3.3985812908190085' not in claim
    for phrase in ('L<2/3','L<12/17','L<=49/1500','L<=249/1700','58-type count is unchanged'):
        assert phrase in claim
    if not args.skip_primary_text:
        primary=(ROOT/source_paths[5]).read_text()
        start=primary.index('Lemma 5.1.')
        end=primary.index('5.2. Bounds on volume and width.',start)
        lemma=primary[start:end]
        assert 'hollow convex body in dimension three' in lemma
        assert 'λ1(K−K)(14)' in lemma
    out={'status':'PASS','review_type':'Independent internal analytic review, not external human peer review',
         'sources':sources,'primary_source_checked':not args.skip_primary_text,
         'primary_source':'https://arxiv.org/abs/1907.06199; Lemma 5.1, equation (14)',
         'exact_height_endpoint_and_clearing_regressions':endpoint_checks,
         'band_endpoint_gauge':'183/500','width_coefficient':'500/317',
         'width_bound_decimal_60_digit_context':bound_text,
         'strict_band_endpoints_verified':True,'both_height_orders_verified':True,
         'requires_no_prior_high_width_for_gauge_upper_bounds':True,
         'corrections_required':[], 'solver_queries_run':0,
         'scope':'CLAIM-0010 analytic corollaries, endpoints and stated limitations; not a finite coverage proof or priority audit.'}
    (ROOT/'results/det5_claim0010_review_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
