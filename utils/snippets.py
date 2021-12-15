from utils.Parser import Term
from solver import TRUE, UNK, FALSE


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