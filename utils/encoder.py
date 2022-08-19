import math
from bitstuff import BitStuffEncoder
from collections import Counter
from bitstring import BitArray


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

    
    def _get_avg_size_and_entropy(self, codes, probs):
        ''' Compute the entropy of the source based on each symbol probability
        obtained by relative frequency and the average code length. '''

        entropy = [prob * math.log(prob, 2) for prob in probs.values()]
        entropy = -sum(entropy)

        avg_len = [prob * len(code) for prob, code in zip(probs.values(), codes.values())]
        avg_len = sum(avg_len)

        return entropy, avg_len


    def encode(self, file_path):
        ''' Compress the file with Huffman compression. '''

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

        entropy, avg_len = self._get_avg_size_and_entropy(huff_codes, probs)
        print(f'Source Entropy = {round(entropy, 3)} bits')
        print(f'Average Code Length Achieved = {round(avg_len, 3)} bits')

        self._write_file_from_stream(stream, file_path + '.huff')