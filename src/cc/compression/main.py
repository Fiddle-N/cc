import argparse
import json
import struct
from collections import Counter
from io import BufferedIOBase

from cc.compression import MAGIC_BYTES, CODE_MAP_LENGTH_FORMAT
from cc.compression.bit_writer import BitWriter
from cc.compression.code_assignment import assign
from cc.compression.code_lengths import create_code_lengths
from cc.compression.freq_tree import create_freq_tree


def compress_file(input_file: BufferedIOBase, output_file: BufferedIOBase) -> None:
    content = input_file.read()
    freqs = Counter(content)
    freq_tree = create_freq_tree(freqs)
    code_lengths = create_code_lengths(freq_tree)
    codes = assign(code_lengths)

    # write header
    json_code_lengths = json.dumps(code_lengths).encode("utf-8")
    code_length = len(json_code_lengths)
    output_file.write(MAGIC_BYTES)
    output_file.write(struct.pack(CODE_MAP_LENGTH_FORMAT, code_length))
    output_file.write(json_code_lengths)

    # write body
    input_file.seek(0)
    bw = BitWriter(file=output_file)
    for char in input_file.read():
        code_num, code_length = codes[char]
        bw.write_bits(code_num, code_length)


def compress(input_filename: str, output_filename: str) -> None:
    with (
        open(input_filename, "rb") as input_file,
        open(output_filename, "wb") as output_file,
    ):
        compress_file(input_file, output_file)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    # compress
    compress_parser = subparsers.add_parser("compress", help="Compress file")
    compress_parser.add_argument("input", help="Input file")
    compress_parser.add_argument("output", help="Output file")

    # decompress
    decompress_parser = subparsers.add_parser("decompress", help="Decompress file")
    decompress_parser.add_argument("input", help="Input file")
    decompress_parser.add_argument("output", help="Output file")

    args = parser.parse_args()

    if args.command == "compress":
        compress(args.input, args.output)
    elif args.command == "decompress":
        print("TODO")
