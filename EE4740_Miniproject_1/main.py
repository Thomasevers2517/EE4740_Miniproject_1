import zipfile
import wave
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from Audio import AudioData
from Huffman import Huffman
directory_paths = ['EE4740_Miniproject_1\F1', 'EE4740_Miniproject_1\F2', 'EE4740_Miniproject_1\F3', 'EE4740_Miniproject_1\F4', 'EE4740_Miniproject_1\M1', 'EE4740_Miniproject_1\M2', 'EE4740_Miniproject_1\M3', 'EE4740_Miniproject_1\M4']
AudioCol = AudioData(directory_paths)

distribution = {}
distribution['diff'] = {}
distribution['orig'] = {}
distribution['diff']['F'] = {}
distribution['diff']['M'] = {} 
distribution['diff']['all'] = {} 
distribution['orig']['F'] = {}
distribution['orig']['M'] = {}
distribution['orig']['all'] = {}

for audio_file in AudioCol.audio_files:
    for key, value in audio_file.orig_distribution.items():
        if key in distribution['orig'][audio_file.gender]:
            distribution['orig'][audio_file.gender][key] += value/8
            distribution['orig']['all'][key] += value/16
        else:
            distribution['orig'][audio_file.gender][key] = value/8
            distribution['orig']['all'][key] = value/16
      
    for key, value in audio_file.differential_distribution.items():
        if key in distribution['diff'][audio_file.gender]:
            distribution['diff'][audio_file.gender][key] += value/8
            distribution['diff']['all'][key] += value/16
        else:
            distribution['diff'][audio_file.gender][key] = value/8
            distribution['diff']['all'][key] = value/16

HuffmanCode = {}
entropy = {}   
encoded = {}
bits_per_symbol = {}    
for type in distribution:
    HuffmanCode[type] = {}
    entropy[type] = {}
    encoded[type] = {}
    bits_per_symbol[type] = {}
    
    for gender in distribution[type]:  
        entropy[type][gender] = -sum([p * np.log2(p) for p in distribution[type][gender].values()])
        HuffmanCode[type][gender] = Huffman(distribution= distribution[type][gender])
        
        for i,audio_file in enumerate(AudioCol.audio_files): 
            if audio_file.gender==gender || gender == 'all':
                
            
            encoded[type][gender], bits_per_symbol[type][gender] = HuffmanCode[type][gender].encode()
        print(f"Type: {type}, Gender: {gender}, Entropy: {entropy[type][gender]}")  


# Bar plot of orig distribution
plt.subplot(2, 1, 1)
plt.bar(distribution['orig']['F'].keys(), distribution['orig']['F'].values())
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title(f'Original F Audio Distribution  ')

plt.subplot(2, 1, 2)
plt.bar(distribution['orig']['all'].keys(), distribution['orig']['all'].values())
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title(f'Orig all Audio Distribution ')


# # Create time axis
# time = np.arange(0, len(AudioCol.audio_files[0].audio_array)) / AudioCol.audio_files[0].sample_rate

# # Plot audio data
# plt.plot(time, AudioCol.audio_files[0].audio_array)
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.title('Audio Data')
# plt.show()



plt.tight_layout()
plt.show()


