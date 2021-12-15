from utils.Parser import parse_file, Term, TERMS
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
            # print('lexer')
            return TRUE
    return UNK


def analyze_system(rules, constructors):
    is_decreasing = True
    for t1, t2 in rules:
        if t1.double or t2.double or \
                (not t1.is_singleton() or not t2.is_singleton()):
            is_decreasing = False
            break
    if is_decreasing:
        # print('signature')
        if check_decreasing_on_signature(rules) or \
                check_decreasing_lexicographic_order(rules, constructors):
            return TRUE
    else:
        return check_subterms_proliferation(rules)
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
    res = analyze_system(parsed, constructors)
    return res


def check_subterms_proliferation(rules, depth=10):
    def dfs(h):
        while h:
            t = stack[-1]
            for ch in t.to:
                for s in stack:
                    if unify(s, TERMS[ch]):
                        return True
                stack.append(TERMS[ch])
                dfs(h-1)
            h -= 1
            stack.pop()
    for rule in rules:
        stack = [rule[0]]
        if dfs(depth):
            # print('loop')
            return TRUE
    return FALSE


if __name__ == '__main__':
    result = UNK
    try:
        result = solve()
    except Exception:
        result = UNK
    finally:
        # print(result)
        write_result(result)