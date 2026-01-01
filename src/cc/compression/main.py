import argparse
import json
from collections import Counter
from io import Reader, Writer
from tempfile import TemporaryFile
from typing import BinaryIO

from cc.compression import MAGIC_BYTES
from cc.compression.bit_writer import BitWriter
from cc.compression.bit_reader import read_bits
from cc.compression.code_assignment import assign, reverse
from cc.compression.code_lengths import create_code_lengths
from cc.compression.exceptions import DecompressionError
from cc.compression.freq_tree import create_freq_tree


def read_byte(file: Reader[bytes]) -> bytes:
    byte = file.read(1)
    if byte == b"":  # EOF
        raise DecompressionError
    return byte


def read_bytes(file: Reader[bytes], no: int) -> bytearray:
    ba = bytearray()
    for _ in range(no):
        byte = read_byte(file)
        ba.extend(byte)
    return ba


def compress_file(input_file: BinaryIO, output_file: Writer[bytes]) -> None:
    # calculate huffman codes
    content = input_file.read()
    freqs = Counter(content)
    freq_tree = create_freq_tree(freqs)
    code_lengths = create_code_lengths(freq_tree)
    codes = assign(code_lengths)

    # write header
    ## write magic bytes
    output_file.write(MAGIC_BYTES)

    ## write length of code lengths map, then code lengths maps in JSON
    json_code_lengths = json.dumps(code_lengths).encode(
        "utf-8"
    )  # int keys will be converted to strings
    output_file.write(
        len(json_code_lengths).to_bytes(length=2, byteorder="big", signed=False)
    )  # network-order (big-endian) uint16
    output_file.write(json_code_lengths)

    ## write length of bytes to be encoded
    output_file.write(len(content).to_bytes(length=8, byteorder="big", signed=False))

    # write body
    input_file.seek(0)

    with BitWriter(file=output_file) as bw:
        for char in input_file.read():
            code_num, code_length = codes[char]
            bw.write_bits(code_num, code_length)


def compress(input_filename: str, output_filename: str) -> None:
    with (
        open(input_filename, "rb") as input_file,
        open(output_filename, "wb") as output_file,
    ):
        compress_file(input_file, output_file)


def decompress_file(input_file: Reader[bytes], output_file: Writer[bytes]) -> None:
    # read magic
    magic = read_bytes(input_file, 4)
    if magic != MAGIC_BYTES:
        raise DecompressionError

    # read header
    ## read and decode code lengths map
    code_lengths_len_bytes = read_bytes(input_file, 2)
    code_length_len = int.from_bytes(
        code_lengths_len_bytes, byteorder="big", signed=False
    )
    json_code_lengths = read_bytes(input_file, code_length_len)
    code_lengths = json.loads(json_code_lengths.decode("utf-8"))
    code_lengths = {int(code): length for code, length in code_lengths.items()}
    codes = assign(code_lengths)

    ## read content lengths
    content_length_bytes = read_bytes(input_file, 8)
    content_length = int.from_bytes(content_length_bytes, byteorder="big", signed=False)

    reverse_codes = reverse(codes)
    read_bits(input_file, output_file, content_length, reverse_codes)


def decompress(input_filename: str, output_filename: str) -> None:
    with open(input_filename, "rb") as input_file, TemporaryFile("wb") as tmp_output:
        decompress_file(
            input_file, tmp_output
        )  # if decompression error raised, close tmp file immediately
        with open(output_filename, "wb") as output_file:
            tmp_output.seek(0)
            output_file.write(tmp_output.read())


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
        decompress(args.input, args.output)
