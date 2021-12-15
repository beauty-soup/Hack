import re

EPS = ''
SEP = '->'
OR = '|'
LETTER_REGEX = '[a-z]'
DIGIT_REGEX = '[0-9]'

INCORRECT_SYNTAX_ERROR = 'Syntax_error'

VARS = set()
CONSTRUCTS = dict()


class Term:
    def __init__(self, type: str, name: str, args: list = None):
        self.type = type
        self.name = name
        self.args = args or []

    def __str__(self):
        res = self.name
        if self.args:
            res += '(' + ','.join([str(a) for a in self.args]) + ')'
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
    assert line.pop() == ']', INCORRECT_SYNTAX_ERROR
    return sorted(list(vars))


def parse_term(line: Queue):
    global CONSTRUCTS
    line, term_name = parse_name(line)
    if term_name in VARS:
        return line, Term('var', term_name)
    if line.peek() != '(':
        assert term_name not in CONSTRUCTS or CONSTRUCTS[term_name] == 0, INCORRECT_SYNTAX_ERROR
        CONSTRUCTS[term_name] = 0
        return line, Term('const', term_name)
    line.pop()
    line, term = parse_term(line)
    term_args = [term]
    while line.peek() == ',':
        line.pop()
        line, term = parse_term(line)
        term_args.append(term)
    assert line.pop() == ')', INCORRECT_SYNTAX_ERROR
    assert term_name not in CONSTRUCTS or CONSTRUCTS[term_name] == len(term_args), INCORRECT_SYNTAX_ERROR
    CONSTRUCTS[term_name] = len(term_args)
    return line, Term('constr', term_name, term_args)


def parse_line(line: Queue):
    line, term1 = parse_term(line)
    assert line.pop() == '-' and line.pop() == '>', INCORRECT_SYNTAX_ERROR
    line, term2 = parse_term(line)
    assert line.is_empty(), INCORRECT_SYNTAX_ERROR
    return [term1, term2]


def parse_file(file_name: str) -> list:
    global VARS, CONSTRUCTS
    VARS = set()
    CONSTRUCTS = dict()
    rules = read_txt(file_name)
    res = []
    assert len(rules) > 1, INCORRECT_SYNTAX_ERROR
    VARS = parse_first_line(Queue(rules[0]))
    for rule in rules[1:]:
        res.append(parse_line(Queue(rule)))
    return res