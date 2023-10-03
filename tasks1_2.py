from collections import Counter
from math import log2

FILE_PATH = R'1.txt'
USE_UNICODE = True
FILE_OPEN_MODE = {'mode': 'r', 'encoding': 'utf-8'} if USE_UNICODE else {'mode': 'rb'}


def file_length(file_path: str) -> int:
    with open(file_path, **FILE_OPEN_MODE) as file:
        return len(file.read())


def symbol_amounts(file_path: str) -> Counter:
    with open(file_path, **FILE_OPEN_MODE) as file:
        return Counter(file.read())


def total_information(sym_amounts: Counter) -> tuple[float, float]:
    total_symbols = sum(sym_amounts.values())
    total_info_bits = sum(symbol_information(probability(amount, total_symbols)) * amount
                          for amount in sym_amounts.values())

    return total_info_bits, total_info_bits / 8


def probability(symbol_frequency: int, total_symbols: int) -> float:
    return symbol_frequency / total_symbols


def symbol_information(symbol_frequency: float) -> float:
    return -log2(symbol_frequency)


def display_table(sym_amounts: Counter):
    total_symbols = sum(sym_amounts.values())
    table = [(
        symbol if USE_UNICODE else f'{hex(symbol)[2:]:0>2}',
        freq,
        probability(freq, total_symbols),
        symbol_information(probability(freq, total_symbols))
    ) for symbol, freq in sym_amounts.items()
    ]

    print('\nSorted by symbol:')
    print(f"{'Hex symbol':12} {'Frequency':10} {'Probability':12} {'Information':12}")
    for row in sorted(table, key=lambda x: x[0]):
        sym, freq, prob, inf = row
        print(f"{sym:12} {freq:<10} {prob:<12.7f} {inf:<12.7f}")

    print('\nSorted by frequency:')
    print(f"{'Hex symbol':12} {'Frequency':10} {'Probability':12} {'Information':12}")
    for row in sorted(table, key=lambda x: x[1], reverse=True):
        sym, freq, prob, inf = row
        print(f"{sym:12} {freq:<10} {prob:<12.7f} {inf:<12.7f}")


def main(file_path: str):
    print(f'File Length (in symbols): {file_length(file_path)}')
    sym_amounts = symbol_amounts(file_path)
    bits_info, bytes_info = total_information(sym_amounts)
    print(f'Total Information (bits, bytes): {bits_info:.5f}, {bytes_info:.5f}')
    display_table(sym_amounts)


if __name__ == '__main__':
    main(FILE_PATH)
