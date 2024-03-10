from Huffman import Huffman
import numpy as np

def get_encoding(distribution, AudioCol):
        
    HuffmanCode = {}
    entropy = {}   
    encoded = {}
    bits_per_symbol = {} 

    for l,type in enumerate(distribution):
        HuffmanCode[type] = {}
        entropy[type] = {}
        encoded[type] = {}
        bits_per_symbol[type] = {}

        for k,gender in enumerate(distribution[type]): 
            assert abs(sum(distribution[type][gender].values())-1) < 0.0001, f'{type}, {gender} distribution: {sum(distribution[type][gender].values())}'
            entropy[type][gender] = -sum([p * np.log2(p) for p in distribution[type][gender].values()])
            HuffmanCode[type][gender] = Huffman(distribution= distribution[type][gender])
            encoded[type][gender] = {}
            bits_per_symbol[type][gender] = {}
            for i,audio_file in enumerate(AudioCol.audio_files): 
                if (audio_file.gender==gender) or (gender == 'all'):
                    if type == 'diff':
                        encoded[type][gender][i], bits_per_symbol[type][gender][i] = HuffmanCode[type][gender].encode(audio_file.differential)
                    else:
                        encoded[type][gender][i], bits_per_symbol[type][gender][i] = HuffmanCode[type][gender].encode(audio_file.audio_array)
        
            print(f"Encoding {audio_file.gender}.{audio_file.person}.{audio_file.index}, Type: {type}, Gender: {gender}, Entropy: {entropy[type][gender]}, Bits per symbol: {bits_per_symbol[type][gender].values()}")  
    return HuffmanCode, entropy, encoded, bits_per_symbol
