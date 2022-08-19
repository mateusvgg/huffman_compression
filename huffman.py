from absl import app
from absl.flags import argparse_flags
import argparse
from utils.encoder import Encoder
from utils.decoder import Decoder


def parse_args(argv):
    parser = argparse_flags.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-c", action='store_true', help="Set this flag to run the compress mode."
    )

    parser.add_argument(
        "-d", action='store_true', help="Set this flag to run the decompress mode."
    )

    parser.add_argument(
        'file_path', type=str, help='Path to the file to be compressed or decompressed.'
    )

    args = parser.parse_args(argv[1:])
    return args


def main(args):
    if args.c:
        encoder = Encoder()
        encoder.encode(args.file_path)

    if args.d:
        decoder = Decoder()
        decoder.decode(args.file_path)


if __name__ == "__main__":
    app.run(main, flags_parser=parse_args)