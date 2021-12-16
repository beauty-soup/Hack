import re

EPS = ''
SEP = '->'
OR = '|'
LETTER_REGEX = '[a-z]'
DIGIT_REGEX = '[0-9]'

INCORRECT_SYNTAX_ERROR = 'Syntax_error'

VARS = set()
CONSTRUCTS = dict()
TERMS = []


class Term:
    def __init__(self, type: str,
                 name: str,
                 double: bool = False,
                 args: list = None,
                 constr_count: dict = None):
        self.type = type
        self.name = name
        self.double = double
        self.args = args or []
        self.constr_count = constr_count or {}
        if self.name in self.constr_count:
            self.constr_count[self.name] += 1
        else:
            self.constr_count[self.name] = 1
        self.args = args or []
        self.s = self.__str__()
        self.to = []

    def __str__(self):
        res = self.name
        if self.args:
            res += '(' + ','.join([str(a) for a in self.args]) + ')'
        return res

    def is_singleton(self):
        if self.type == 'var':
            return True
        if len(self.args) != 1:
            return False
        return self.args[0].is_singleton()

    def alpha_transform(self, postfix: int):
        postfix = str(postfix)
        for i in range(len(self.args)):
            if self.args[i].type == 'var':
                self.args[i] += postfix

    def unfold(self):
        res = [self]
        for a in self.args:
            if a.type == 'constr':
                res += a.unfold()
            else:
                res.append(a)
        return res

    def __repr__(self):
        return self.__str__()


class Queue(list):
    def __init__(self, *args):
        super().__init__(*args)

    def peek(self):
        item = ''
        try:
            item = self.__getitem__(0)
        finally:
            return item

    def is_empty(self):
        return not len(self)

    def pop(self, **kwargs):
        item = ''
        try:
            item = super().pop(0)
        finally:
            return item


def is_letter(s: str):
    return 'A' <= s <= 'Z' or 'a' <= s <= 'z'


def parse_name(line: Queue):
    result = line.pop()
    assert is_letter(result), INCORRECT_SYNTAX_ERROR
    while is_letter(line.peek()):
        result += line.pop()
    return line, result


def read_txt(path: str) -> list:
    rules = re.split('\n+', open(path, 'r')\
                     .read()\
                     .replace(' ', '')\
                     .replace('\t', ''))
    rules = [r for r in rules if r]
    return rules


def parse_first_line(line: Queue):
    vars = set()
    assert line.pop() == '[', INCORRECT_SYNTAX_ERROR
    if line.peek() != ']':
        line, var = parse_name(line)
        vars.add(var)
        while line.peek() != ']' and not line.is_empty():
            assert line.pop() == ',', INCORRECT_SYNTAX_ERROR
            line, var = parse_name(line)
            vars.add(var)
    assert line.pop() == ']' and line.is_empty(), INCORRECT_SYNTAX_ERROR
    return sorted(list(vars))


def parse_term(line: Queue):
    def add_constr_count(constr_count, term):
        for c in term.constr_count:
            if c in constr_count:
                constr_count[c] += term.constr_count[c]
            else:
                constr_count[c] = term.constr_count[c]

        return constr_count

    global CONSTRUCTS
    line, term_name = parse_name(line)
    if term_name in VARS:
        return line, Term('var', term_name)
    if line.peek() != '(':
        assert term_name not in CONSTRUCTS or \
               CONSTRUCTS[term_name] == 0, INCORRECT_SYNTAX_ERROR
        CONSTRUCTS[term_name] = 0
        return line, Term('const', term_name)
    line.pop()
    line, term = parse_term(line)
    term_constrs = add_constr_count({}, term)
    term_double = term.double
    term_args = [term]
    while line.peek() == ',':
        line.pop()
        line, term = parse_term(line)
        if not term_double:
            if term.double or (term.type == 'var' and term_args[-1].name == term.name):
                term_double = True
        term_args.append(term)
        term_constrs = add_constr_count(term_constrs, term)
    assert line.pop() == ')', INCORRECT_SYNTAX_ERROR
    assert term_name not in CONSTRUCTS or \
           CONSTRUCTS[term_name] == len(term_args), INCORRECT_SYNTAX_ERROR
    CONSTRUCTS[term_name] = len(term_args)
    return line, Term('constr', term_name, term_double, term_args, term_constrs)


def add_to_terms(term):
    global TERMS
    for t in TERMS:
        if t.name == term.name:
            return
    TERMS.append(term.alpha_transform(len(TERMS)))


def find_term(t_name):
    for i in range(len(TERMS)):
        if TERMS[i].name == t_name:
            return i
    return -1


def parse_line(line: Queue):
    line, term1 = parse_term(line)
    assert line.pop() == '-' and line.pop() == '>', INCORRECT_SYNTAX_ERROR
    add_to_terms(term1)
    line, term2 = parse_term(line)
    assert line.is_empty(), INCORRECT_SYNTAX_ERROR
    idx = find_term(term2.name)
    if idx < 0:
        term1.to.append(len(TERMS))
        TERMS.append(term2)
    else:
        if idx not in term1.to:
            term1.to.append(idx)
    return [term1, term2]


def parse_file(file_name: str) -> (list, list):
    global VARS, CONSTRUCTS, TERMS
    rules = read_txt(file_name)
    res = []
    assert len(rules) > 1, INCORRECT_SYNTAX_ERROR
    VARS = parse_first_line(Queue(rules[0]))
    for rule in rules[1:]:
        res.append(parse_line(Queue(rule)))
    return res, CONSTRUCTS.keys()