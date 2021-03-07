lines = []
while True:
    try:
        x = input()
        if not x:
            break
        lines.append(x)
    except EOFError:
        break

for i, x in enumerate(lines):
    print(f'TTITLE{i}={x}')
