from utils.Parser import parse_file, Term, parse_term, Queue
from utils.Unif import unify
TEST_DIR = 'trs'

from utils import timeout
TIMEOUT_LIM = 160
from itertools import permutations

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
    return UNK


def check_decreasing_lexicographic_order(rules, constructors: list):
    def is_lex_greater(t1: Term, t2: Term) -> bool:
        nonlocal order
        t1_args = t1.args[:-1]
        t2_args = t2.args[:-1]
        t2_len = len(t2_args)
        for i, a1 in enumerate(t1_args):
            if i < t2_len:
                a2 = t2_args[i]
                if order[a1] > order[a2]:
                    return False
            break
        return True

    for permutation in permutations(range(len(constructors))):
        order = dict(zip(constructors, permutation))
        flag = True
        for t1, t2 in rules:
            if not is_lex_greater(t1, t2):
                flag = False
                break
        if flag:
            return TRUE
    return FALSE


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

def write_result(result):
    with open('result', 'w') as f:
        f.write(result)


@timeout.timeout(TIMEOUT_LIM)
def solve():
    try:
        parsed, constructors = parse_file(test_f)
    except Exception:
        return SYNTAX_ERROR
    for r in parsed:
        for t in r:
            print(t.is_singlton())
    res = analyze_system(parsed)
    res = check_decreasing_lexicographic_order(parsed, constructors.keys())
    return res



if __name__ == '__main__':
    result = solve()
    write_result(result)