hashes = [
    777,
    111,
    222,
    333,
    66,
    22,
    99,
    666
]
count = 1
for hash in hashes:
    print(f'K{count} -> {(100 / max(hashes)) * hash * 3.6}')
    count += 1