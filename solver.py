from Parser import parse_file, read_txt
from Unif import unify
TEST_DIR = 'trs'

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


def solve():
    try:
        raw = read_txt(test_f)
        parsed = parse_file(test_f)
    except Exception:
        return SYNTAX_ERROR
    for row in parsed:
        print(row[0].unfold())
        mgu = unify(row[0], row[1])
        print(mgu)
    return TRUE


if __name__ == '__main__':
    result = solve()
    write_result(result)