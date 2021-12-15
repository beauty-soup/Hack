from Parser import parse_file
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

def main():
    p = parse_file(test_f)
    print(p)






if __name__ == '__main__':
    main()