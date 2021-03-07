def print_row(*data):
    print('|', end='')
    for val in data:
        print('%s|' % val, end='')


def convert_value(v, empty_str):
    x = v if v else empty_str
    if x == 'None':
        return empty_str
    else:
        return x



def print_markdown_table(dictionaries, empty_str, keep_raw_header):
    assert len(dictionaries) > 0

    keys = dictionaries[0].keys()

    if keep_raw_header:
        print_row(*keys)
    else:
        print_row(*map(lambda x: x.replace('#', '').strip(), keys))
    print()
    print_row(*map(lambda x: '-' * len(x), keys))
    print()

    for d in dictionaries:
        rr = []
        for k in keys:
            v = d.get(k, empty_str)
            if v:
                v = v.strip()
            rr.append(convert_value(v, empty_str))
        print_row(*rr)
        print()
    print()


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-n', '--empty-str', default='NULL')
    parser.add_argument('-k', '--keep-raw-header', action='store_true')
    parser.add_argument('-s', '--separator')
    return parser.parse_args()


def main():
    from csv import DictReader, excel_tab
    import io
    import sys

    args = parse_args()
    empty_str = args.empty_str
    keep_raw_header = args.keep_raw_header

    data = []
    for line in sys.stdin:
        data.append(line)
    data = '\n'.join(data)
    with io.StringIO(data) as f:
        if args.separator == 't':
            reader = DictReader(f, dialect=excel_tab)
        else:
            reader = DictReader(f)
        dictionaries = [d for d in reader]
    print_markdown_table(dictionaries, empty_str, keep_raw_header)


if __name__ == '__main__':
    main()
