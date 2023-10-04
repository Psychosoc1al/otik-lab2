from collections import Counter
from os import walk, path

FOLDER_PATH = r'D:\Загружено\otik-master\labs-files\Файлы в формате простого текста — кодировки разные'
FILE_PATH = r'D:\Загружено\otik-master\labs-files\Варианты 2 — определение кодировки простого текста\2.txt'
ENCODINGS = ['ascii',
             'big5',
             'big5hkscs',
             'cp037',
             'cp273',
             'cp424',
             'cp437',
             'cp500',
             'cp720',
             'cp737',
             'cp775',
             'cp850',
             'cp852',
             'cp855',
             'cp856',
             'cp857',
             'cp858',
             'cp860',
             'cp861',
             'cp862',
             'cp863',
             'cp864',
             'cp865',
             'cp866',
             'cp869',
             'cp874',
             'cp875',
             'cp932',
             'cp949',
             'cp950',
             'cp1006',
             'cp1026',
             'cp1125',
             'cp1140',
             'cp1250',
             'cp1251',
             'cp1252',
             'cp1253',
             'cp1254',
             'cp1255',
             'cp1256',
             'cp1257',
             'cp1258',
             'euc_jp',
             'euc_jis_2004',
             'euc_jisx0213',
             'euc_kr',
             'gb2312',
             'gbk',
             'gb18030',
             'hz',
             'iso2022_jp',
             'iso2022_jp_1',
             'iso2022_jp_2',
             'iso2022_jp_2004',
             'iso2022_jp_3',
             'iso2022_jp_ext',
             'iso2022_kr',
             'latin_1',
             'iso8859_2',
             'iso8859_3',
             'iso8859_4',
             'iso8859_5',
             'iso8859_6',
             'iso8859_7',
             'iso8859_8',
             'iso8859_9',
             'iso8859_10',
             'iso8859_11',
             'iso8859_13',
             'iso8859_14',
             'iso8859_15',
             'iso8859_16',
             'johab',
             'koi8_r',
             'koi8_t',
             'koi8_u',
             'kz1048',
             'mac_cyrillic',
             'mac_greek',
             'mac_iceland',
             'mac_latin2',
             'mac_roman',
             'mac_turkish',
             'ptcp154',
             'shift_jis',
             'shift_jis_2004',
             'shift_jisx0213',
             'utf_32',
             'utf_32_be',
             'utf_32_le',
             'utf_16',
             'utf_16_be',
             'utf_16_le',
             'utf_7',
             'utf_8',
             'utf_8_sig']


def get_plaintext_files_counter() -> Counter:
    localcounter = Counter()
    for root, _, files in walk(FOLDER_PATH):
        for file in files:
            with open(path.join(root, file), 'rb') as f:
                localcounter.update(Counter(f.read()))

    return localcounter


def print_tables(localcounter: Counter) -> None:
    sorted_by_freq = sorted([(symbol, freq) for symbol, freq in localcounter.items()], key=lambda x: x[1],
                            reverse=True)

    print('Top-4 most common octets:')
    print(f"{'Octet':7} {'Frequency':10}")
    for symbol, freq in sorted_by_freq[:4]:
        print(f"{f'{hex(symbol)[2:]:0>2}':7} {freq}")
    print()

    top_non_printable = [(symbol, freq) for symbol, freq in sorted_by_freq if not 31 < symbol < 127]
    print('Top-4 most common ASCII non-printable octets:')
    print(f"{'Octet':7} {'Frequency':10}")
    for symbol, freq in top_non_printable[:4]:
        print(f"{f'{hex(symbol)[2:]:0>2}':7} {freq}")
    print()


def select_encodings() -> None:
    with open(FILE_PATH, 'rb') as file:
        localcounter = sorted([(symbol, freq) for symbol, freq in Counter(file.read()).items()], key=lambda x: x[1],
                              reverse=True)

    for encoding in ENCODINGS:
        try:
            with open(FILE_PATH, 'r', encoding=encoding) as file:
                file.read()

            info = [(bytes([symbol]).decode(encoding), freq) for symbol, freq in localcounter]

            if all([info[i][0] in ' оеаинтсрвл' for i in range(10)]):  # see README
                print(encoding, 'is possible')
                for i in range(10):
                    print(info[i][0], info[i][1])
                print()

        except (UnicodeDecodeError, UnicodeEncodeError):
            ...


def main() -> None:
    counter = get_plaintext_files_counter()
    print_tables(counter)
    select_encodings()


if __name__ == '__main__':
    main()
