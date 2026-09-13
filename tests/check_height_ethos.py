"""Check stored CPC refutations with official Ethos and reference-input binding.

Standard library only; never calls an SMT solver. See HEIGHT_ETHOS_REPRODUCTION.md.
"""
from pathlib import Path
from collections import Counter
import argparse, gzip, hashlib, json, re, subprocess, tempfile, time

ROOT = Path(__file__).resolve().parents[1]
ETHOS_REV = '221641668d75eaffd308e0511d63962cea937110'
CVC5_REV = 'f3b21c4483d3b88dc63cb7cd3e5eb092eee5e341'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sexps(text):
    """Restricted input grammar: no quoted strings/symbols or comments accepted."""
    need(not any(c in text for c in ';"|'), 'unexpected quoting/comment')
    stack = [[]]
    for tok in re.findall(r'\(|\)|[^\s()]+', text):
        if tok == '(':
            stack.append([])
        elif tok == ')':
            need(len(stack) > 1, 'unbalanced close')
            v = stack.pop(); stack[-1].append(v)
        else:
            stack[-1].append(tok)
    need(len(stack) == 1, 'unbalanced open')
    return stack[0]


def emit(e):
    return '(' + ' '.join(map(emit, e)) + ')' if isinstance(e, list) else e


def real_reference(text):
    """QF_LRA numeral tokens have Real context. Change n to n/1 only there.

No algebraic simplification or assertion change is made. Proof syntax is never
normalized: its rule indices must remain integer literals.
"""
    cmds = sexps(text)
    need(cmds[0] == ['set-logic', 'QF_LRA'], 'expected QF_LRA')
    variables = set()
    assertions = 0
    def convert(e):
        if isinstance(e, str):
            if re.fullmatch(r'[0-9]+', e):
                return e + '/1'
            need(e in variables, 'non-Real or undeclared leaf: ' + e)
            return e
        need(e and e[0] in ('+', '-', '*', '/', '=', '<', '<=', '>', '>=', 'or', 'and', 'not'), 'unsupported assertion operation')
        return [e[0], *[convert(a) for a in e[1:]]]
    out = []
    for c in cmds:
        if c[0] == 'set-logic':
            need(c == cmds[0], 'unexpected logic'); out.append(c)
        elif c[0] == 'declare-fun':
            need(len(c) == 4 and c[2:] == [[], 'Real'], 'only nullary Real declarations')
            need(c[1] not in variables, 'duplicate declaration'); variables.add(c[1]); out.append(c)
        else:
            need(c[0] == 'assert' and len(c) == 2, 'unexpected reference command')
            out.append(['assert', convert(c[1])]); assertions += 1
    need(len(variables) == 22 and assertions > 0, 'full matrix encoding size')
    return '\n'.join(map(emit, out)) + '\n', assertions, variables


def proof_body(raw, variables):
    """Validate proof framing and goal; allow no rules/signatures in proof body."""
    text = raw.decode().strip()
    need(text.startswith('(\n') and text.endswith('\n)'), 'one CPC outer list')
    body = text[1:-1]
    depth = 0; counts = Counter(); declared = set(); final = None; kept = []; definitions = set()
    for line in body.splitlines():
        if not line.strip():
            continue
        commands = sexps(line)
        need(len(commands) == 1 and isinstance(commands[0], list), 'one command per CPC line')
        c = commands[0]; head = c[0]
        need(head in ('declare-const', 'define', 'assume', 'assume-push', 'step', 'step-pop'), 'proof command whitelist')
        counts[head] += 1
        if head != 'declare-const':
            kept.append(line)
        if head == 'define':
            need(len(c) == 4 and c[2] == [] and c[1].startswith('@t') and c[1] not in definitions, 'fresh nullary abbreviation')
            definitions.add(c[1])
        if head == 'assume':
            need(depth == 0, 'global assumption only at top level')
        if head == 'declare-const':
            need(len(c) == 3 and c[2] == 'Real' and c[1] in variables and c[1] not in declared, 'proof declaration binding')
            declared.add(c[1])
        if head == 'assume-push':
            depth += 1
        if head == 'step-pop':
            need(depth > 0, 'scope underflow'); depth -= 1
        if head in ('step', 'step-pop'):
            need(':rule' in c and c[c.index(':rule') + 1] not in ('trust', 'sorry'), 'unjustified proof rule')
        final = c
    need(declared == variables, 'same declared Real variables')
    need(depth == 0, 'undischarged local assumption')
    need(counts['assume'] > 0 and counts['step'] > 0, 'nonempty proof')
    need(final[:1] == ['step'] and final[2] == 'false', 'final top-level refutation')
    return '\n'.join(kept) + '\n', dict(counts)


def checker(ethos, source, proof, reference):
    sig = source / 'proofs/eo/cpc'
    cmd = [str(ethos), '--include=' + str(sig / 'Cpc.eo'),
           '--include=' + str(sig / 'expert/CpcExpert.eo'),
           '--reference=' + str(reference)]
    start = time.monotonic()
    r = subprocess.run(cmd, input=proof.read_text(), text=True, capture_output=True, timeout=120)
    return {'exit_code': r.returncode, 'stdout': r.stdout.strip(), 'stderr': r.stderr.strip(),
            'elapsed_seconds': time.monotonic() - start}


def revision(path):
    r = subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True, capture_output=True, check=True)
    need(not subprocess.run(['git', '-C', str(path), 'status', '--porcelain', '--untracked-files=no'], text=True, capture_output=True, check=True).stdout.strip(), 'modified thirdparty source')
    return r.stdout.strip()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ethos', type=Path, required=True)
    p.add_argument('--ethos-source', type=Path, required=True)
    p.add_argument('--cvc5-source', type=Path, required=True)
    p.add_argument('--output', type=Path, default=ROOT / 'results/height_ethos_validation.json')
    args = p.parse_args()
    args.ethos = args.ethos.resolve(); args.ethos_source = args.ethos_source.resolve(); args.cvc5_source = args.cvc5_source.resolve()
    need(revision(args.ethos_source) == ETHOS_REV, 'pinned Ethos revision')
    need(revision(args.cvc5_source) == CVC5_REV, 'pinned CPC signature revision')
    receipt_path = ROOT / 'results/height_cover_cvc5_validation.json'
    receipt = json.loads(receipt_path.read_text())
    need(receipt['status'] == 'PASS' and len(receipt['leaves']) == 62, 'complete cvc5 receipt required')
    config = subprocess.run([str(args.ethos), '--show-config'], text=True, capture_output=True, check=True).stdout.strip()
    need('version 0.2.3' in config, 'checker version')
    signatures = {str(f.relative_to(args.cvc5_source)): sha(f.read_bytes()) for f in sorted((args.cvc5_source / 'proofs/eo').rglob('*.eo'))}
    rows = []; controls = []
    report = {'status': 'INCOMPLETE', 'checker': {'name': 'Ethos', 'version': '0.2.3', 'revision': ETHOS_REV,
        'binary_sha256': sha(args.ethos.read_bytes()), 'configuration': config, 'source_url': 'https://github.com/cvc5/ethos'},
        'cvc5_signature_revision': CVC5_REV, 'cvc5_signature_tag': 'cvc5-1.3.4', 'signature_sha256': signatures,
        'cvc5_receipt_sha256': sha(receipt_path.read_bytes()), 'leaves': rows, 'controls': controls,
        'command_template': 'python3 tests/check_height_ethos.py --ethos ETHOS/build/src/ethos --ethos-source ETHOS --cvc5-source CVC5',
        'reference_adapter': 'Parse restricted QF_LRA with only nullary Real declarations. Rewrite each assertion numeral token n to n/1; preserve every operator and assertion. Ethos --reference then checks assumptions against this exact Real rendering.',
        'proof_adapter': 'Remove outer CPC list and verified duplicate Real declarations; preserve all other commands. Stream proof on stdin after --reference to retain reference checking in Ethos 0.2.3. Reject extra commands, trust/sorry, unbalanced scopes and missing final top-level false.',
        'trust_boundary': 'Ethos C++ kernel, compiler/runtime/GMP, pinned official CPC Eunoia signatures, and this framing/reference adapter. No trusted/sorry proof steps. Signature soundness is not proved in a separate proof assistant. Geometry, encoding and cover require their separate audits.',
        'build': {'cmake': '4.4.3', 'compiler': 'GNU C++ 13.3.0', 'gmp_package': 'Ubuntu 2:6.3.0+dfsg-2ubuntu6.1',
                  'upstream_tests': '174/174 passed; see reproduction document for commands.'}}
    def save():
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    tags = set()
    with tempfile.TemporaryDirectory(prefix='flatness-ethos-') as tmp:
        tmp = Path(tmp); pr = tmp / 'proof.cpc'; ref = tmp / 'reference.smt2'
        for leaf in receipt['leaves']:
            need(leaf['status'] == 'unsat', 'UNSAT leaf')
            idx, ext, node = leaf['class_index'], leaf['extrema'], leaf['node']
            tag = f'{idx}_{ext[0]}_{ext[1]}_{node}'
            need(tag not in tags, 'duplicate leaf'); tags.add(tag)
            base = ROOT / 'certificates/height_cover_cvc5' / tag
            smt = base.with_suffix('.smt2').read_bytes(); packed = base.with_suffix('.cpc.gz').read_bytes(); raw = gzip.decompress(packed)
            need(sha(smt) == leaf['input_sha256'] and sha(raw) == leaf['proof_sha256'] and sha(packed) == leaf['compressed_proof_sha256'], 'receipt hash binding')
            adapted, assertions, variables = real_reference(smt.decode()); body, counts = proof_body(raw, variables)
            ref.write_text(adapted); pr.write_text(body)
            result = checker(args.ethos, args.cvc5_source, pr, ref)
            row = {'leaf': tag, 'input_sha256': sha(smt), 'proof_sha256': sha(raw),
                   'compressed_proof_sha256': sha(packed), 'reference_sha256': sha(adapted.encode()),
                   'assertions': assertions, 'proof_commands': counts, 'reference_binding': True,
                   'balanced_scopes': True, 'final_top_level_false': True, **result}
            rows.append(row); save()
            need(result['exit_code'] == 0 and result['stdout'] == 'correct' and not result['stderr'], 'Ethos proof failure: ' + tag)
            print(json.dumps({'leaf': tag, 'ethos': 'correct', 'seconds': result['elapsed_seconds']}), flush=True)
            if len(rows) == 1:
                # A proof containing a fresh assertion must be rejected by reference binding.
                bad = body + '\n(assume @fresh_unrelated false)\n'
                pr.write_text(bad)
                r = checker(args.ethos, args.cvc5_source, pr, ref)
                need(r['exit_code'] != 0 and 'assumption' in (r['stdout'] + r['stderr']).lower(), 'reference-binding negative control')
                controls.append({'name': 'fresh unrelated assumption', 'rejected': True, **r})
                # Wrong final conclusion must fail the proof rule itself, not merely framing.
                pos = body.rfind(' false :rule '); need(pos >= 0, 'explicit final false')
                pr.write_text(body[:pos] + body[pos:].replace(' false :rule ', ' true :rule ', 1))
                r = checker(args.ethos, args.cvc5_source, pr, ref)
                need(r['exit_code'] != 0, 'false conclusion mutation')
                controls.append({'name': 'final false changed to true', 'rejected': True, **r})
                # Removing the conclusion can leave a well-typed partial proof; framing must reject it.
                last = body.rstrip().rfind('\n')
                try:
                    proof_body(('(\n' + '\n'.join('(declare-const ' + v + ' Real)' for v in sorted(variables)) + '\n' + body[:last] + '\n)').encode(), variables)
                except (ValueError, IndexError):
                    controls.append({'name': 'missing final refutation', 'rejected': True, 'checker': 'local framing guard'})
                else:
                    raise ValueError('missing final conclusion accepted')
                try:
                    real_reference(smt.decode().replace('() Real)', '() Int)', 1))
                except ValueError:
                    controls.append({'name': 'non-Real reference declaration', 'rejected': True, 'checker': 'local reference guard'})
                else:
                    raise ValueError('non-Real reference accepted')
                save()
    need(len(rows) == 62 and len(controls) == 4, 'complete verification')
    report['status'] = 'PASS'; report['external_correct'] = len(rows); save()
    print(json.dumps({'status': 'PASS', 'external_correct': len(rows), 'controls_rejected': len(controls)}))


if __name__ == '__main__':
    main()
