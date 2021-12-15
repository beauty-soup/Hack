from utils.Parser import parse_file, read_txt, Term
from utils.Unif import unify
TEST_DIR = 'trs'

from utils import timeout
TIMEOUT_LIM = 160

tests = dict(
    {
        'dickson': [f'{TEST_DIR}/Dickson/test_dickson{i}.trs' for i in range(1, 5)],
        'kruskal': [f'{TEST_DIR}/Kruskal/test_growing{i}.trs' for i in range(1, 5)],
        'lex': [f'{TEST_DIR}/Lex/test_lex{i}.trs' for i in range(1, 5)],
        'loop': [f'{TEST_DIR}/Loop/test_loop{i}.trs' for i in range(2, 5)],
        'wfma': [f'{TEST_DIR}/WFMA/test_fuma{i}.trs' for i in range(1, 5)],
    }
)
test_f = 'test.trs'

SYNTAX_ERROR = "Syntax_error"
TRUE = "True"
FALSE = "False"
UNK = "Unknown"


def write_result(result):
    with open('result', 'w') as f:
        f.write(result)

@timeout.timeout(TIMEOUT_LIM)
def solve():
    try:
        raw = read_txt(test_f)
        parsed = parse_file(test_f)
    except Exception:
        return SYNTAX_ERROR
    for row in parsed:
        mgu = unify(row[0], row[1])
        print(mgu)
    return TRUE


def is_decreasing_on_signature(t1: Term, t2: Term):
    c1 = t1.constr_count
    c2 = t2.constr_count
    if {*c1} - {*c2}:
        return True
    for k, v in c1.items():
        if v > c2[k]:
            return True
    return False


def check_decreasing_on_signature(rules):
    for rule in rules:
        if not is_decreasing_on_signature(*rule):
            return False
    return True


def check_subterms_proliferation(rules):
    pass


def check_decreasing_lexicographic_order(rules):
    pass


def analyze_system(rules):
    is_double = False
    for rule in rules:
        for r in rule:
            if r.double:
                is_double = True
                break
    if is_double:
        return check_subterms_proliferation(rules)
    if check_decreasing_on_signature(rules) or \
            check_decreasing_lexicographic_order(rules):
        return TRUE
    return UNK


if __name__ == '__main__':
    result = solve()
    write_result(result)