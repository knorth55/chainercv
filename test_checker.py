import argparse
import os
import sys


def check_test_exists(path):
    test_paths = path.split('/')
    if test_paths[-1] == '__init__.py':
        return None

    if test_paths[1] == 'chainercv':
        test_paths[1] = 'tests'
        test_paths[2:-1] = [p + '_tests' for p in test_paths[2:-1]]
        test_paths[-1] = 'test_' + test_paths[-1]
    elif test_paths[1] == 'examples':
        test_paths[1:-1] = [p + '_tests' for p in test_paths[1:-1]]
        test_paths[-1] = 'test_' + os.path.splitext(test_paths[-1])[0] + '.sh'
    else:
        return None

    test_path = os.path.join(*test_paths)
    if os.path.exists(test_path):
        return None
    else:
        return 'Test does not exits.'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude', nargs='+')
    parser.add_argument('dir')
    args = parser.parse_args()

    n_err = 0

    for d, _, files in os.walk(args.dir):
        for f in files:
            _, ext = os.path.splitext(f)
            if not ext == '.py':
                continue

            if args.exclude is not None and f in args.exclude:
                continue

            path = os.path.join(d, f)
            msg = check_test_exists(path)
            if msg is not None:
                print('{:s}: {:s}'.format(path, msg))
                n_err += 1

    if n_err > 0:
        sys.exit('{:d} codes with no test are found.'.format(n_err))


if __name__ == '__main__':
    main()
