import bitstring
from bitstring import BitArray, BitStream, Bits


class ByteReader:

    def _read_file_bytes(self, file_path):
        ''' Reads the file in binary mode and return an operator yielding the bytes read. '''

        with open(file_path, 'rb') as f:                                  
            while True:                                                   
                byte = f.read(1)                                            
                if byte:                                                    
                    yield byte                                                
                else:                                                       
                    break 


    def _write_file_from_stream(self, stream, file_name):       
        ''' Write the bitstream to a file. '''

        bitarray = BitArray()                                               
        for i in range(0, len(stream), 8):                       
            bitarray.append(BitStream('0b' + stream[i : i+8]))       
        bitarray = Bits(bitarray)                                
        with open(file_name, 'wb') as f:                         
            bitarray.tofile(f)      



class BitStuffEncoder(ByteReader):

    def __init__(self):
        super().__init__()

    
    def _make_bitstream(self, bytes_array, codes):           
        ''' Generate the corpus bitstream based on the file bytes and the corresponding Huffman Codes. '''

        stream = ''                                     
        for byte in bytes_array:                              
            stream += codes[byte]                       
        return stream  


    def _gen_header(self, codes):
        ''' Generate the header information that carries 
        the possible symbols and the corresponding codes. '''

        header1 = ''                                                         # List with 0's and 1's, every position that has an 1 is a possible symbol
        header2 = ''                                                         # List with the code size in 8 bits followed by the code

        bytes_dict = {i : str(bin(i))[2:].zfill(8) for i in range(256)}         
        possible_symbols = list(bytes_dict.values())                         # Every symbol between 00000000 and 11111111
        actual_symbols = codes.keys()                                        # Only the symbols in the source

        for symbol in possible_symbols:                                               
              if symbol in actual_symbols:                                      
                  code = codes[symbol]                                         
                  binary_code_length = bytes_dict[len(code)]                     
                  header1 += '1'                                         
                  header2 = header2 + binary_code_length + code           
              else:                                                      
                  header1 += '0'                                         

        return header1 + header2

    
    def _gen_padding(self, stream):  
        ''' Add padding info in the header and the padding bits at the end of the stream, if necessary. '''

        stream_len = len(stream)                                             
        rest = stream_len % 8  

        if rest != 0:                                                      
            num_bits_added = 8 - rest
            num_bits_added_binary = str(bin(num_bits_added))[2:].zfill(4)
            bits_to_add = '0' * num_bits_added
            return '1111' + num_bits_added_binary + stream + bits_to_add  

        return '11110000' + stream  



class BitStuffDecoder(ByteReader):

    def __init__(self):
        super().__init__()       


    def _split_stream(self, bytes_array):     
        ''' Split the recieved stream in order to correctly retrieve the info sent. ''' 

        padding_info = bytes_array[0]
        last_byte = bytes_array[-1]
        symbols = [i for i in bytes_array[1:33]]  # The 256 bits of the header that cointains the info of what symbols are possible   
        stream = bytes_array[33:-1]
        return padding_info, last_byte, symbols, stream


    def _treat_padding(self, padding_info, last_byte, stream_bytes):
        ''' Remove the bits added to the final of the stream. '''

        num_bits_added_binary = padding_info[4:8]
        num_bits_added_dec = int(num_bits_added_binary, 2)
        last_byte = last_byte[:8-num_bits_added_dec] # Remove padding
        stream_bits = ''.join(byte for byte in stream_bytes)
        return stream_bits + last_byte  

    
    def _get_symbols(self, symbols_bytes):
        ''' Retrieve the the source's possible symbols. '''

        bitstream = ''.join(byte for byte in symbols_bytes)
        symbols = [str(bin(index))[2:].zfill(8) for index, i in enumerate(bitstream) if i == '1']
        return symbols

    
    def _get_codes(self, symbols, bitstream):
        ''' Generate the Huffman codes based on the header information. '''

        pointer = 0
        huff_codes = {}
        for i in range(len(symbols)):
          code_len = int(bitstream[pointer:pointer+8], 2)
          pointer += 8
          # Save the corresponding symbol code in the dictionary, note
          # that the codes are in ascending order of decimal representation
          # in the same way that it was put in the stream by the encoder,
          # this allows the indexing symbols[i].
          huff_codes[symbols[i]] = bitstream[pointer:pointer+code_len] 
          pointer += code_len

        return bitstream[pointer:], huff_codes

    
    def _get_original_bitstream(self, bitstream, huff_codes):
        ''' Retrieve the original file bitstream. '''

        codes_huff = {value : key for key, value in huff_codes.items()}
        original, buffer = '', ''
        for bit in bitstream:
            buffer += bit
            if buffer in codes_huff.keys():
                original += codes_huff[buffer]
                buffer = ''
        return original