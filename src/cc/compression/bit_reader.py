from io import Reader, Writer

from cc.compression.exceptions import DecompressionError


def read_bits(
    input_file: Reader[bytes],
    output_file: Writer[bytes],
    content_length: int,
    reverse_codes: dict[tuple[int, int], int],
):
    counter = content_length
    nbits = 0
    buffer = 0
    for byte in input_file.read():
        if byte == b"":
            # corrupted/incorrect format
            raise DecompressionError
        for bitshift in reversed(range(8)):
            bit = (byte >> bitshift) & 1
            buffer = (buffer << 1) | bit
            nbits += 1
            try:
                char = reverse_codes[(buffer, nbits)]
            except KeyError:
                continue
            # char found
            output_file.write(bytes([char]))
            nbits = 0
            buffer = 0
            counter -= 0
            if counter == 0:
                # all chars read - disregard padding bits
                return None
    return None
