from bitstuff import BitStuff
from collections import Counter
from bitstring import BitArray
from tqdm import tqdm


class Encoder:

    def __init__(self):
        self._bitstuff = BitStuff()


    def _get_freq_and_probs(self, bytes_array):  
        ''' Compute the number of occurrences and thus the approximated probability of each byte '''

        freq_dict = Counter(bytes_array)
        freq = sorted(freq_dict.items(), key=lambda x: x[1])                 
        num_bytes = len(bytes_array)                                                                                       
        probs = {f[0] : float(f[1]/num_bytes) for f in freq}
        return freq, probs


    def _make_tree(self, freqs): 
        ''' Generate the Huffman tree by combining the elements with the lowest probability '''

        while len(freqs) > 1:                                                
            lowest_freq_elements = tuple(freqs[0:2])                                  
            combined_freq = lowest_freq_elements[0][1] + lowest_freq_elements[1][1]     
            other_elements = freqs[2:]                                            
            freqs = other_elements + [(lowest_freq_elements, combined_freq)]         
            freqs = sorted(freqs, key=lambda x: x[1])                                  
        return freqs[0]  


    def encode(self, file_path):
        # Generate a list with every byte read from the file
        bytes_array = [BitArray(byte).bin for byte in self._bitstuff.read_file_bytes(file_path)] 
        freqs, probs = self._get_freq_and_probs(bytes_array)
        return self._make_tree(freqs)
        # huff_codes = {}                                                      
                          
                                                                             # Probs contains the probabilities of each symbol
        # freq, probs = prepare_data(bytes_array)                               # freq is a list of tuples, each tuple contains (n_k, byte_k), where n_k is the number os occurences of byte_k in bytes_array
        # tree = make_tree(freq)                                               # The huffman tree. The tree is a tuple of tuples. Each tuple contains (freq, element), where freq is the number os occurrences of elements
        # tree = remove_freq(tree)                                             # The Huffman tree without the frequencies.                
        # get_codes(tree, huff_codes)                                              # Recursive function to assign the codes to the symbols by traversing the tree
        # stream = makeStream(bytes_array, huff_codes)                              # Make the compressed bitstream
        # stream1 = makeHeader(stream, huff_codes)                                 # Append the Header to the bitstram
        # stream2 = makePadding(stream1)                                       # Make padding if necessary
        
        # cName = file_path + '.huff'
        # writeCompressed(stream2, cName)                                      # Make a binary file with the compressed array

        # return bytes_array, stream, stream1, stream2, huff_codes, probs


path = 'os_maias.txt'
encoder = Encoder()
tree = encoder.encode(path)
print(tree)