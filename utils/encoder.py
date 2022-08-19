from bitstuff import BitStuffEncoder
from collections import Counter
from bitstring import BitArray
from tqdm import tqdm


class Encoder(BitStuffEncoder):

    def __init__(self):
        super().__init__()


    def _get_freq_and_probs(self, bytes_array):  
        ''' Compute the number of occurrences and thus the approximated probability of each byte. '''

        freq_dict = Counter(bytes_array)
        freq = sorted(freq_dict.items(), key=lambda x: x[1])                 
        num_bytes = len(bytes_array)                                                                                       
        probs = {f[0] : float(f[1]/num_bytes) for f in freq}
        return freq, probs


    def _make_tree(self, freqs): 
        ''' Generate the Huffman tree by combining the elements with the lowest probability. '''

        while len(freqs) > 1:                                                
            lowest_freq_elements = tuple(freqs[0:2])                                  
            combined_freq = lowest_freq_elements[0][1] + lowest_freq_elements[1][1]     
            other_elements = freqs[2:]                                            
            freqs = other_elements + [(lowest_freq_elements, combined_freq)]         
            freqs = sorted(freqs, key=lambda x: x[1])                                  
        return freqs[0]  

    
    def _remove_freq(self, freqs): 
        ''' Remove recursively the frequency value of each node, leaving only the branches that follows from it. '''                                              
        freqs = freqs[0]                                                   
        if isinstance(freqs, str):                                             
            return freqs                                                   
        else:                                                              
            return (self._remove_freq(freqs[0]), self._remove_freq(freqs[1]))     


    def _get_codes(self, branch, codes, pointer=''):
        ''' Generate Huffman codes based on the Huffman tree. '''
    
        if isinstance(branch, str):                     
            codes[branch] = pointer                 
        else:                                     
            self._get_codes(branch[0], codes, pointer + '0')
            self._get_codes(branch[1], codes, pointer + '1')


    def encode(self, file_path):
        bytes_array = [BitArray(byte).bin for byte in self._read_file_bytes(file_path)] 
        freqs, probs = self._get_freq_and_probs(bytes_array)
        tree = self._make_tree(freqs)
        tree = self._remove_freq(tree)
        huff_codes = {} 
        self._get_codes(tree, huff_codes)  
        corpus_stream = self._make_bitstream(bytes_array, huff_codes)
        header_info = self._gen_header(huff_codes)         
        stream = header_info + corpus_stream 
        stream = self._gen_padding(stream)                                      
        self._write_file_from_stream(stream, file_path + '.huff')
        return stream                 


path = 'os_maias.txt'
encoder = Encoder()
teste = encoder.encode(path)
print(teste[:10])