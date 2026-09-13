from src.canonical import canonicalize
from src.examples import codenotti_santos
from src.geometry import Polytope
import pytest


def test_contact_frame_unimodular_invariance():
    K=codenotti_santos()
    M=K.transform([[1,2,0],[0,1,1],[0,0,-1]],[2,-3,1])
    assert canonicalize(K)['canonical_key']==canonicalize(M)['canonical_key']

def test_vertex_order_and_redundant_generator():
    K=codenotti_santos()
    center=tuple(sum(v[j] for v in K.vertices)/4 for j in range(3))
    M=Polytope(list(reversed(K.vertices))+[center])
    assert canonicalize(K)['canonical_key']==canonicalize(M)['canonical_key']

def test_forged_or_incomplete_contact_sets_rejected():
    K=codenotti_santos()
    with pytest.raises(ValueError):canonicalize(K,[(0,0,0),(1,0,0),(0,1,0),(0,0,2)])
    with pytest.raises(ValueError):canonicalize(K,[(0,0,0)])
