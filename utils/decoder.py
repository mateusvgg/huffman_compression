from bitstuff import BitStuffDecoder
from collections import Counter
from bitstring import BitArray


class Decoder(BitStuffDecoder):

    def __init__(self):
        super().__init__()

    
    def decode(self, file_path):
        bytes_array = [BitArray(byte).bin for byte in self._read_file_bytes(file_path)] 
        padding_info, last_byte, symbols_bytes, bitstream = self._split_stream(bytes_array)
        bitstream = self._treat_padding(padding_info, last_byte, bitstream)
        symbols = self._get_symbols(symbols_bytes)
        bitstream, huff_codes = self._get_codes(symbols, bitstream)
        return bitstream, huff_codes


path = 'os_maias.txt.huff'
decoder = Decoder()
bitstream, huff_codes = decoder.decode(path)
print(sorted(list(huff_codes.items()), key=lambda x:len(x[1])))