import argparse


def compress(input_filename: str, output_filename: str) -> None:
    pass
    # with (
    #     open(input_filename, "rb") as input_file,
    #     open(output_filename, "wb") as output_file,
    # ):
    #     input_content = input_file.read()
    #     input_freqs = Counter(input_content)


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
