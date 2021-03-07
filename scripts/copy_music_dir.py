from pathlib import Path


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('from_dir')
    parser.add_argument('to_dir')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--no-check', action='store_true')
    return parser.parse_args()


def check_hash(from_path, to_path):
    from hashlib import sha256

    chunk_size = 65536
    fm = sha256()
    with from_path.open('rb') as f:
        d = f.read(chunk_size)
        fm.update(d)
    ft = sha256()
    with to_path.open('rb') as f:
        d = f.read(chunk_size)
        ft.update(d)
    return fm.hexdigest() == ft.hexdigest()


def copy_dir(from_path, to_path, execute, check):
    from shutil import copytree

    from_path = from_path.resolve()
    to_path = to_path.resolve()

    print(f'copy: from_path={from_path} to_path={to_path} execute={execute}')

    if execute:
        copytree(from_path, to_path)
    if check:
        check_dir(from_path, to_path)


def check_dir(from_path, to_path):
    for i in from_path.rglob('*'):
        if not i.is_file():
            continue
        rpath = i.relative_to(from_path)
        tpath = to_path / rpath
        try:
            if not check_hash(i, tpath):
                print(f'check failed: from_path={i} to_path={tpath}')
        except FileNotFoundError as e:
            print(f'check failed: from_path={i} to_path={tpath} error={e}')


def main():
    args = parse_args()
    execute = args.execute
    check = not args.no_check

    from_path = Path(args.from_dir)
    to_path = Path(args.to_dir)

    for artist_path in from_path.glob('*'):
        if not artist_path.is_dir():
            continue
        target_path = to_path / artist_path.relative_to(from_path)
        if target_path.exists():
            for album_path in artist_path.glob('*'):
                if not album_path.is_dir():
                    continue
                target_path = to_path / album_path.relative_to(from_path)
                if not target_path.exists():
                    print(f'sync: target={album_path} mode=album_dir')
                    copy_dir(album_path, target_path, execute, check)
                else:
                    print(f'sync: target={album_path} mode=skipped')
                    if check:
                        check_dir(album_path, target_path)
        else:
            print(f'sync: target={artist_path} mode=artist_dir')
            copy_dir(artist_path, target_path, execute, check)


if __name__ == '__main__':
    main()
