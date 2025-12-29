import io
import json
import struct

from cc.compression import MAGIC_BYTES, CODE_MAP_LENGTH_FORMAT


def encode(source: io.BytesIO, target: io.BytesIO, codes: dict[str, str]) -> None:
    # write header
    json_codes = json.dumps(codes).encode("utf-8")
    code_length = len(json_codes)
    target.write(MAGIC_BYTES)
    target.write(struct.pack(CODE_MAP_LENGTH_FORMAT, code_length))
    target.write(json_codes)

    # write body
    source.seek(0)
    # for char in source.read():
    #     code = codes[char]
