from io import Writer


class BitWriter:
    def __init__(self, file: Writer[bytes]):
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
