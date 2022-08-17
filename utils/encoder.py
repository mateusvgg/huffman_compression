from bitstuff import BitStuff
from collections import Counter
from bitstring import BitArray


class Encoder:

    def __init__(self):
        self._bitstuff = BitStuff()


    def _get_freq_and_probs(self, bytes_array):  
        ''' Compute the number of occurrences and thus the approximated probability of each byte '''

        freq_dict = Counter(bytes_array)
        freq = sorted(freq_dict.items(), key=lambda x: x[1])                 
        num_bytes = len(bytes_array)                                                                                       
        probs = {f[0] : float(f[1]/num_bytes) for f in freq}
        return freq_dict, probs


    # def get_freq(freq_dict):                                               # Generate a list of tuples that contains (freq, byte)
    #     symbols = freq_dict.keys()                                           # List of the possible bytes
    #     freq = []                                                            # List that will have the tuples

    #     for symbol in symbols:                                               # Iterate in each byte
    #         freq.append((freq_dict[symbol], symbol))                           # Append the tuple (freq, byte)
    #     freq.sort()                                                          # Sort the list in ascending order of frequency
    #     return freq

    # def prepare_data(array):                                               # Function to prepare the data
    #   freq, probs = get_freq_and_probs(array)   
    #   return get_freq(freq), probs


    def encode(self, file_path):
        # Generate a list with every byte read from the file
        bytes_array = [BitArray(byte).bin for byte in self._bitstuff.read_file_bytes(file_path)] 
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
freq_dict, probs = encoder.encode(path)
print(freq_dict, '\n\n')
print(sorted(probs.items(), key=lambda x: x[1]))
num_bytes = sum(freq_dict.values())
freq = freq_dict["01100001"]
print(f'num_bytes = {num_bytes}')
print(f'freq = {freq}')
print(f'prob_test = {freq/num_bytes}')
print(f'correct = {probs["01100001"]}')