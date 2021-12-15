from Parser import parse_file, read_txt
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('file_path', metavar='-f', type=str,
                    default=None, nargs=1, help='path to test trs file')

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
    global test_counter
    raw = read_txt(test_f)
    with open(test_f, 'r') as f:
        print(f.read())
    try:
        raw = read_txt(test_f)
        parsed = parse_file(test_f)
    except Exception:
        return SYNTAX_ERROR
    return TRUE


if __name__ == '__main__':
    result = solve()
    write_result(result)