import io
import json
import struct

from cc.compression import MAGIC_BYTES, CODE_MAP_LENGTH_FORMAT
from cc.compression.code_assignment import assign


class BitWriter:
    def __init__(self, file: io.BytesIO):
        self.file = file
        self.buffer = 0
        self.nbits = 0

    def write_bit(self, bit: int):
        self.buffer = (self.buffer << 1) | bit
        self.nbits += 1

        if self.nbits == 8:
            self.file.write(bytes([self.buffer]))
            self.buffer = 0
            self.nbits = 0

    def write_bits(self, value: int, n: int):
        for i in reversed(range(n)):
            self.write_bit((value >> i) & 1)

    def flush(self):
        if self.nbits:
            self.buffer <<= 8 - self.nbits  # pad with zeros
            self.file.write(bytes([self.buffer]))
            return self.nbits  # number of valid bits in final byte
        return 0


def encode(
    input_: io.BytesIO, output: io.BytesIO, code_lengths: dict[int, int]
) -> None:
    codes = assign(code_lengths)

    # write header
    json_code_lengths = json.dumps(code_lengths).encode("utf-8")
    code_length = len(json_code_lengths)
    output.write(MAGIC_BYTES)
    output.write(struct.pack(CODE_MAP_LENGTH_FORMAT, code_length))
    output.write(json_code_lengths)

    # write body
    input_.seek(0)
    bw = BitWriter(file=output)
    for char in input_.read():
        code_num, code_length = codes[char]
        bw.write_bits(code_num, code_length)
