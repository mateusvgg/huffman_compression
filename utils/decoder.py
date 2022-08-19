from bitstuff import BitStuffDecoder
from bitstring import BitArray


class Decoder(BitStuffDecoder):

    def __init__(self):
        super().__init__()

    
    def decode(self, file_path):
        ''' Decompress the file by reversing the steps from the encoder. '''

        bytes_array = [BitArray(byte).bin for byte in self._read_file_bytes(file_path)] 
        padding_info, last_byte, symbols_bytes, bitstream = self._split_stream(bytes_array)
        bitstream = self._treat_padding(padding_info, last_byte, bitstream)
        symbols = self._get_symbols(symbols_bytes)
        bitstream, huff_codes = self._get_codes(symbols, bitstream)
        original_bitstream = self._get_original_bitstream(bitstream, huff_codes)
        self._write_file_from_stream(original_bitstream, 'rec_' + file_path.replace('.huff', ''))