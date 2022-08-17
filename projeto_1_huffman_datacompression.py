"""#Importing and getting data"""
import bitstring
import math
from bitstring import BitArray, BitStream, Bits

#All file paths

path_dom = 'os_maias.txt'

paths = {'fonte': path_f, 'fonte0': path_f0, 'fonte1': path_f1, 'TEncSearch': path_search, 'TEncEntropy': path_entropy, 'Lena': path_lena, 'Dom Casmurro': path_dom}

"""Encoder:
1. Get file bytes as a list of bytes
2. Calculate the frequency and probability 
of each byte
3. Make the binary Tree based on the bytes 
frequencies
4. Generate the Huffman codes by traversing
the tree
5. Make the raw stream with the codes
6. Make the Header and append to the raw
stream
7. Generate the padding byte, append to the
beggining of the stream and add the padding
to the end if necessary
8. Generate a .bin file with the stream

Decoder:
1. Get file bytes as a list of bytes
2. Split the stream: get the first byte, the
last byte, the 256 bits from the header as a
list and the stream that has the codes and
the raw stream
3. Read the padding info, remove, if
necessary, the padding bits from the last
byte and after append the last byte to the
stream.
4. With the first 256 bits from the header,
generate a list with the possible symbols
5. Generate the codes for the symbols by
iterating the first bits from the stream.
Return the codes and the raw stream
6. Generate the original file with the raw 
stream and the codes
7. Write back the original file

#Encoder
"""

def get_bytes(file_path, n):                                           # Function to read n bytes from the file, if n=-1 reads every byte
  with open(file_path, 'rb') as file:                                  # Open the file in read binary mode
    while True:                                                        # Loop 
      byte = file.read(1)                                              # Get a byte
      if byte:                                                         # If it is valid  
        yield byte                                                     # yields the byte  
      else:                                                            # If it is not valid
        break                                                          # Break the loop
      if n > 0:                                                        # If n still greater than 0
        n -= 1                                                         # Decrease n
        if n == 0:                      
          break                                                        # Break if n = 0

def get_freq_and_probs(array):                                         # Calculate the frequency and probability of each byte
  freq_dict = {}                                                       # Frequency dictionary {byte : frequency}
  for i in array:                                                      # Loop to fill the dictionary
    if i in freq_dict:                                                 # If the byte is already in the dict
      freq_dict[i] += 1                                                # Increases the frequency
    else:                                                              # If the byte is no in the dict 
      freq_dict[i] = 1                                                 # Add the byte as a key and initiate his frequency 

  freq = sorted(freq_dict.items(), key=lambda x: x[1])                 # Tuple with (byte, frequency) in ascending order of frequencies
  l = len(array)                                                       # How many bytes                                        

  probs = {}                                                           # Dictionary with the bytes probabilities {byte : prob}
  for f in freq:                                                       # Loop to fill the dict
    probs[f[0]] = float(f[1]/l)                                        # Number of occurences of the byte / Total byte numbers

  return freq_dict, probs

def get_freq(freq_dict):                                               # Generate a list of tuples that contains (freq, byte)
  symbols = freq_dict.keys()                                           # List of the possible bytes
  freq = []                                                            # List that will have the tuples

  for symbol in symbols:                                               # Iterate in each byte
    freq.append((freq_dict[symbol], symbol))                           # Append the tuple (freq, byte)
  freq.sort()                                                          # Sort the list in ascending order of frequency
  return freq

def prepare_data(array):                                               # Function to prepare the data
  freq, probs = get_freq_and_probs(array)   
  return get_freq(freq), probs                                         # Return the list with the tuples (freq, byte) and the prob dictionary

def make_tree(freq):                                                   # Function to make the binary tree
  while len(freq) > 1:                                                 # While is has more than 1 element in the frequency tuple 
    eCombinados = tuple(freq[0:2])                                     # Combine the 2 least frequent elements
    frequenciaCombinada = eCombinados[0][0] + eCombinados[1][0]        # Add the frequency of the least frequent elements 
    elementos = freq[2:]                                               # Get the elements thas has the frequency above the 2 least frequent
    freq = elementos + [(frequenciaCombinada, eCombinados)]            # Append the combined elements to the tuple/tree in the format (frequency, element)
    freq.sort(key=lambda x:x[0])                                       # Sort the tree by ascending order of frequency
  return freq[0]                                                       # Return the tree

def remove_freq(freq):                                                 # The tree is of type (total_occurences, (elements))
  freq = freq[1]                                                       # Get only the elements
  if type(freq) == str:                                                # If the element is a leaf
    return freq                                                        # Return the tree      
  else:                                                                # If the element is a node
    return (remove_freq(freq[0]), remove_freq(freq[1]))                # Return the branchs

def get_codes(ramo, codes, pointer=''):                                # Function to generate the codes by traversing the tree
                                                                       # Pointer is the variable that will remember the path taken  
                                                                       # codes is the dictionary that will contain the codes {byte : code}
  if type(ramo) == str:                                                # If it reaches a leaf
    codes[ramo] = pointer                                              # Returns the code  
  else:                                                                # If is reaches a branch
    get_codes(ramo[0], codes, pointer+'0')                             # If it goes to the right, append '0'
    get_codes(ramo[1], codes, pointer+'1')                             # If it goes to the left, append '1'

def makeStream(file_, codes):                                          # Generate the compressed stream based on the Huffman codes
  stream = ''                                                          # The stream
  for byte in file_:                                                   # Iterate in the original list with the bytes
    stream += codes[byte]                                              # Append the byte corresponding code
  return stream                                                        # Returns the stream

def pad(l):                                                            # Function to generate the bits to correct the stream size
  pad = ''                                                             # The correction
  for i in range(8-l):                                                 # Loop with the necessary number of bits to correct 
    pad += '0'                                                         # Append '0'
  return pad                                                           # Return the padding

def makeHeader(stream, codes):
  b1 = {}                                                              # {'00000001' : 1}
  b2 = {}                                                              # {1 : '00000001'}
  for i in range(256):                                                 # Loop to generate b1 and b2, they will make the coding easier 
    b_d = str(bin(i))[2:]                                              # Ex: str(bin(2)) = '0b10', [2:] gets only '10'
    b1[pad(len(b_d)) + b_d] = i                                        # pad(len(b_d)) + b_d return the binary number in 8-bits
    b2[i] = pad(len(b_d)) + b_d          

  header1 = ''                                                         # List with 0's and 1's, every position that has an 1 is a possible symbol
  header2 = ''                                                         # List with the code size in 8 bits followed by the code

  symbols = b1.keys()                                                  # Every symbol between 00000000 and 11111111
  possibleSymbols = codes.keys()                                       # Only the symbols in the source
  for symbol in symbols:                                               # Iterate through all symbols 00000000 - 11111111
    if symbol in possibleSymbols:                                      # If the symbol is in the source
      code = codes[symbol]                                             # The code for the symbol
      l_code = b2[len(code)]                                           # The size of the code in 8 bits, note that the code's lenght is limited at 255
      header1 += '1'                                                   # Append 1 to say that the symbols is possible
      header2 = header2 + l_code + code                                # Append the code size in 8 bits followed by the code
    else:                                                              # If the symbol is not in the source
      header1 += '0'                                                   # Append 0 to say that the code is not possible

  return header1 + header2 + stream                                    # Return the header + the original bitStream

def makePadding(stream):                                               # Function to append the padding information to the compressed stream 
  len_stream = len(stream)                                             # Lenght of the stream 
  rest = len_stream%8                                                  # The rest of the division by 8, we need to append 8-l at the end
  if rest != 0:                                                        # If it is not zero
    b = {}                                                             # Dictionary with {3 : ('0011', 00000)}
    for i in range(1,8):                                               # From 1 to 7 
      b_d = str(bin(8-i))[2:]                                          # Ex: str(bin(2)) = '0b10', [2:] gets only '10'
      if len(b_d) == 1:                                                # If it has only 1 bit 
        b[i] = ('000' + b_d, pad(i))                                   # Add the tuple 
      elif len(b_d) == 2:                                              # If it has 2 bit 
        b[i] = ('00' + b_d, pad(i))                                    # Add the tuple
      elif len(b_d) == 3:                                              # If it has 3 bit 
        b[i] = ('0' + b_d, pad(i))                                     # Add the tuple

    return '1111' + b[rest][0] + stream + b[rest][1]                   # Returns the padding appended to the strem in the following format: the first byte contains '1111' + the number of bits added to the end in 4 bits
  else:                                                                # If the rest is zero   
    return '11110000' + stream                                         # Return only the first byte

def writeCompressed(stream, file_name):                                # Write the comressed file in .bin format
  g = BitArray()                                                       # Variable with the bitstream
  for i in range(0, len(stream), 8):                                   # Starting from the first byte to the last
    g.append(BitStream('0b'+stream[i:i+8]))                            # Generate the bitstream
  g = Bits(g)                                                          # Convert to Bits class  
  with open(file_name + '.bin', 'wb') as f:                            # Open the file in write format 
    g.tofile(f)                                                        # Write the bitstream

def ENCODE(filePath):                                                  # Encoder function
  file_array = [] 
  cName = filePath.split('.')[0] + '_compressed'
  codes_ = {}                                                          # Dictionary with each symbol as the key and it's Huffman code as the value of codes[symbol]. EX: {'01010101': 01}
  #file_array is an array of bytes, i.e, [byte_0, byte_1, byte_2, ... , byte_n] and contains every byte from the file
  #byte_k is a string that contains byte_k's bits
  #Ex: byte_k = '01010101', type(byte_k) = str

  for byte in get_bytes(filePath, -1):
    file_array.append(BitArray(byte).bin)                              # Probs contains the probabilities of each symbol
  freq, probs = prepare_data(file_array)                               # freq is a list of tuples, each tuple contains (n_k, byte_k), where n_k is the number os occurences of byte_k in file_array
  tree = make_tree(freq)                                               # The huffman tree. The tree is a tuple of tuples. Each tuple contains (freq, element), where freq is the number os occurrences of elements
  tree = remove_freq(tree)                                             # The Huffman tree without the frequencies.                
  get_codes(tree, codes_)                                              # Recursive function to assign the codes to the symbols by traversing the tree
  stream = makeStream(file_array, codes_)                              # Make the compressed bitstream
  stream1 = makeHeader(stream, codes_)                                 # Append the Header to the bitstram
  stream2 = makePadding(stream1)                                       # Make padding if necessary
  writeCompressed(stream2, cName)                                      # Make a binary file with the compressed array

  return file_array, stream, stream1, stream2, codes_, probs

"""#Decoder"""

def splitStream(array):                                                # Split the stream in the way that it can extract the padding info and the header info            
  paddingInfo = array[0]                                               # The first byte
  lastByte = array[-1]                                                 # The last byte
  symbols = [i for i in array[1:33]]                                   # The 256 bits of the header that cointains the info of what symbols are possible   
  stream = array[33:-1]                                                # The stream left after this
  return paddingInfo, lastByte, symbols, stream

def treatPadding(paddingInfo, lastByte, stream):                       # Function to treat the padding
  pad = paddingInfo[4:8]                                               # Hoy many bits were added at the end in binary
  b = {}                                                               # Dictionary with {'0011' : 3}
  for i in range(0,8):                                                 # Loop to generate b 
      b_d = str(bin(i))[2:]
      if len(b_d) == 1:
        b['000' + b_d] = i
      elif len(b_d) == 2:
        b['00' + b_d] = i
      elif len(b_d) == 3:
        b['0' + b_d] = i

  pad = b[pad]                                                         # Hoy many bits were added at the end in decimal
  lastByte = lastByte[:8-pad]                                          # Remove the bits added
  
  nStream = ''                                                         # New Stream
  for i in stream:                                                     # Iterate through the stream 
    nStream += i                                                       # Generate the new stream

  return nStream + lastByte                                            # The stream without the padding

def genSymbols(array):                                                 # Generate the possible symbols
  stream = ''                                                          # The 256 bits from the header
  for i in array:                                                      # Iterate through the bits 
    stream += i                                                        # Generate a string with the bits 
  
  b1 = {}                                                              # {'00000001' : 1}
  b2 = {}                                                              # {1 : '00000001'}
  for i in range(256):                                                 # Loop 256 times to generate all decimal number in the interval 0-255 in 8 bits
    b_d = str(bin(i))[2:]
    b1[pad(len(b_d)) + b_d] = i
    b2[i] = pad(len(b_d)) + b_d

  symbols = []                                                         # List to store the possible symbols
  for ind in range(256):                                               # Iterante from 0 to 255
    if stream[ind] == '1':                                             # If this position in the stream is a 1 it is a possible symbol
      symbols.append(b2[ind])                                          # Append the symbols to the list of possible symbols
   
  return symbols

def genCodes(symbols, stream):                                         # Generate the Huffman codes based on the header information
  point = 0                                                            # Variable that will serve as a pointer
  codes_ = {}                                                          # Dictionary to store the codes
  for i in range(len(symbols)):                                        # Iterate through the possible symbols
    step = int(stream[point:point+8], 2)                               # Get the lenght of the code and save it
    point += 8                                                         # Increase the pointer by 8 since we read the byte
    codes_[symbols[i]] = stream[point:point+step]                      # Save the corresponding symbol code in the dictionary
    point += step                                                      # Increase the pointer by the size of the code read  

  return stream[point:], codes_

def originalFile(stream, codes_):                                      # Function to generate the original file bitstream
  codesD = {}                                                          # Dictionary {code : symbol}
  for i in codes_.keys():                                              # Iterate through the dictionary that has {symbol : code}
    codesD[codes_[i]] = i                                              # Save {code : symbol}
  
  original = ''                                                        # String to store the original bitstream
  dummy = ''                                                           # Dummy variable to store the bits read from the encoded stream
  for bit in stream:                                                   # Iterate through the encoded stream bit by bit 
    dummy += bit                                                       # Append the bit read
    if dummy in codesD.keys():                                         # If the sequence of bits read corresponds to a symbol
      original += codesD[dummy]                                        # Add the corresponding symbol to the original stream
      dummy = ''                                                       # Reset the dummy
    
  return original

def writeOriginal(stream, fPath):                                      # Write back the original file (I wrote two functions that do the same thing and I dont know why)
  g = BitArray()                                                       # Variable with the bitstream
  for i in range(0, len(stream), 8):                                   # Starting from the first byte to the last
    g.append(BitStream('0b'+stream[i:i+8]))                            # Generate the bitstream
  g = Bits(g)                                                          # Convert to Bits class  
  with open(fPath, 'wb') as f:                                         # Open the file in write format 
    g.tofile(f)                                                        # Write the bitstream

def DECODER(f_path):                                                   # Encoder Function
  fPath = f_path.split('.')[0] + '_compressed.bin'                     # Generate the compressed file path
  oPath = f_path.split('.')[0] + '_original.' + f_path.split('.')[1]   # Generate the new original file path

  file_array = []                                                      # Array to store the bytes from the comrpessed file
  for byte in get_bytes(fPath, -1):                                    # Iterate through the file bytes 
    file_array.append(BitArray(byte).bin)                              # Append the byte read to the array, constructing the compressed bitstream

  paddingInfo, lastByte, symbols, stream = splitStream(file_array)     # Split the stream
  stream = treatPadding(paddingInfo, lastByte, stream)                 # Treat the padding of the stream
  symbolsList = genSymbols(symbols)                                    # Generate the possible symbols
  stream, codeDict = genCodes(symbolsList, stream)                     # Generate the Huffman codes of each symbol
  original = originalFile(stream, codeDict)                            # Write back the original file bitstream
  writeOriginal(original, oPath)                                       # Write a new file decompressed 

  return original

def size_and_entropy(codes_, probs):                                   # Function to calculate the avarage size of the code and the source entropy
  ent = 0                                                              # Variable to store the entropy             
  for i in probs.keys():                                               # Iterate through the bytes
    ent += (probs[i] * math.log(probs[i], 2))                          # Sum the prob of the byte times the log2 of the prob to the total entropy 
  ent = 0-ent                                                          # Take the negative 

  avg = 0                                                              # Variable to store the avg code size
  for i in codes_.keys():                                              # Iterate through the bytes
    avg += (probs[i]*(len(codes_[i])))                                 # Add the length of the code times it's probability 

  return avg, ent

def size7zip(fPath):                                                   # Function to get the size of the file compressed by 7zip
  path = fPath.split('.')[0] + '.zip'                                  # Path to the 7zip file
  fList = []                                                           # List to store the file bytes
  for byte in get_bytes(path, -1):                                     # Iterate through the file bytes
    fList.append(BitArray(byte).bin)                                   # Append the byte
  
  return len(fList)

def checkCompression(fPath, oList, comStream, comStream2, decStream, codes_, probs):                     
  oStream = ''
  for i in oList:
    oStream += i

  avg, ent = size_and_entropy(codes_, probs)
  print(f'Original file size --------------------------------- {int(len(oStream)/8)} bytes')
  print(f'Encoded bitstream size without header and padding -- {int(len(comStream2)/8)} bytes')
  print(f'Encoded bitstream size with header and padding ----- {int(len(comStream)/8)} bytes') 
  print(f'Encoded file size by 7zip -------------------------- {size7zip(fPath)} bytes')
  print(f'Decoded file size ---------------------------------- {int(len(decStream)/8)} bytes')
  print('================================================================')
  print(f'Source entropy ----- {round(ent, 3)} bits per symbol')
  print(f'Average code size -- {round(avg, 3)} bits per symbol')
  print('================================================================')
  print('Is decoded file the same as the original?')
  print(f'R: {oStream == decStream}')

"""#Compressing, decompressing and checking"""

path_ = path_dom
bytesList, cStream, hStream, pStream, dictCodes, dictProbs = ENCODE(path_)                                 
# bytesList - List with the bytes from the original file
# cStream - compressed raw bitstream 
# hStream - compressed bitstream with the header information
# pStream - compressed bitstream with the header and padding
# dictCodes - dictionary with the Huffman codes {byte : code}
# dictProbs - dictionary with the probability of each byte {byte : prob}

ofile = DECODER(path_)
#ofile - The bitstream from the decoded file

checkCompression(path_, bytesList, pStream, cStream, ofile, dictCodes, dictProbs)

for path in paths.keys():
  print('Encoding ' + path)
  a, b, c, d, e, f = ENCODE(paths[path])
  print('Decoding ' + path)
  o = DECODER(paths[path])
  print('Checking Compression for ' + path)
  checkCompression(paths[path], a, d, b, o, e, f)
  print('\n')