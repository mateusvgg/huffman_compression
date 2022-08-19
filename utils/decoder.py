from bitstuff import BitStuffDecoder
from collections import Counter
from bitstring import BitArray


class Decoder(BitStuffDecoder):

    def __init__(self):
        super().__init__()

    
    def decode(self, file_path):
        bytes_array = [BitArray(byte).bin for byte in self._read_file_bytes(file_path)] 
        padding_info, last_byte, symbols_bytes, stream = self._split_stream(bytes_array)
        stream = self._treat_padding(padding_info, last_byte, stream)
        symbols = self._get_symbols(symbols_bytes)
        return symbols


path = 'os_maias.txt.huff'
decoder = Decoder()
stream = decoder.decode(path)
print(stream, len(stream))