from bitstuff import BitStuffDecoder
from collections import Counter
from bitstring import BitArray


class Decoder(BitStuffDecoder):

    def __init__(self):
        super().__init__()