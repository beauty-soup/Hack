import time

from utils.Parser import parse_file, Term, TERMS, read_txt
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


def check_decreasing_on_signature(rules):

    def is_decreasing_on_signature(t1: Term, t2: Term):
        args_1 = t1.args
        args_2 = t2.args
        for arg in args_1:
            if is_decreasing_on_signature(arg, t2):
                return True
        l1 = len(args_1)
        l2 = len(args_2)
        if l1 >= l2:
            flag = True
            for arg in args_2:
                if is_decreasing_on_signature(arg, t1):
                    flag = False
                    break
            if flag:
                if l1 == l2:
                    for i in range(l1):
                        if args_1[i].s != args_2[i].s and \
                                is_decreasing_on_signature(args_2[i], args_1[i]):
                            return False
                return True
        return False

    for rule in rules:
        if not is_decreasing_on_signature(*rule):
            return False
    # print('signature')
    return True


def check_subterms_proliferation(rules, depth) -> bool:
    def dfs(h):
        while h and len(stack):
            t = stack[-1]
            #if len(stack) > 1 and unify(stack[-2], t):
            #    return True
            for s in stack[:-1]: #stack[:-2]:
                s = alpha_transform(s, '1')
                if unify(s, t):
                    return True
            for ch in t.to:
                stack.append(TERMS[ch])
                if dfs(h-1):
                    return True
            h -= 1
            stack.pop()
            return False

    for rule in rules:
        stack = [rule[0]]
        if dfs(depth):
            # print('loop')
            return True
    return False



def check_decreasing_lexicographic_order(rules, constructors: list) -> bool:
    def is_lex_greater(t1: Term, t2: Term) -> bool:
        nonlocal order
        t1_args = t1.constrs_in
        t2_args = t2.constrs_in
        t2_len = len(t2_args)
        t1_len = len(t1_args)
        for i, a1 in enumerate(t1_args):
            if i < t2_len:
                a2 = t2_args[i]
                if order[a1] > order[a2]:
                    return False
            else:
                break
        return t1_len >= t2_len

    for permutation in permutations(range(len(constructors))):
        order = dict(zip(constructors, permutation))
        flag = True
        for t1, t2 in rules:
            if not is_lex_greater(t1, t2):
                flag = False
                break
        if flag:
            # print('lexer')
            return True
    return False


@timeout.timeout(TIMEOUT_LIM)
def solve() -> str:
    try:
        rules, constructors = parse_file(test_f)
    except Exception:
        return SYNTAX_ERROR
    is_double_term = False
    is_single_val = True
    for t1, t2 in rules:
        if t1.double or t2.double:
            is_double_term = True
            is_single_val = False
            break
        if not (t1.is_singleton() and t2.is_singleton()):
            is_single_val = False
            break
    if is_single_val and check_decreasing_lexicographic_order(rules, constructors):
        return TRUE
    if not is_double_term and check_decreasing_on_signature(rules):
        return TRUE
    if check_subterms_proliferation(rules, len(rules) * 2):
        return FALSE
    return UNK


def write_result(result):
    with open('result', 'w') as f:
        f.write(result)


def alpha_transform(term: Term, postfix: str) -> Term:
    args = []
    for a in term.args:
        if a.type == 'var':
            args.append(Term(name=a.name+postfix, type=a.type, args=a.args,
                             constr_count=a.constr_count, double=a.double))
        else:
            args.append(alpha_transform(a, postfix))
    return Term(
        name=term.name,
        type=term.type,
        args=args,
        constr_count=term.constr_count,
        double=term.double,
    )


if __name__ == '__main__':
    result = UNK
    try:
        result = solve()
    except Exception as e:
        result = UNK
    finally:
        print(result)
        write_result(result)