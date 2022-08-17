import bitstring
from bitstring import BitArray, BitStream, Bits

class BitStuff:

    def read_file_bytes(self, file_path):
        ''' Reads the file in binary mode and return an operator yielding the bytes read '''

        with open(file_path, 'rb') as f:                                  
            while True:                                                   
                byte = f.read(1)                                            
                if byte:                                                    
                    yield byte                                                
                else:                                                       
                    break                                                     