import zipfile
import wave
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from Audio import AudioData
from Huffman import Huffman
from total_distributions import get_total_distribution
import json
from get_encoding import get_encoding

test = False
if test:
    skip_plot_distributions = True
    skip_diff = True
else:
    skip_plot_distributions = False
    skip_diff = False
    
directory_paths = ['EE4740_Miniproject_1\F1', 'EE4740_Miniproject_1\F2', 'EE4740_Miniproject_1\F3', 'EE4740_Miniproject_1\F4', 'EE4740_Miniproject_1\M1', 'EE4740_Miniproject_1\M2', 'EE4740_Miniproject_1\M3', 'EE4740_Miniproject_1\M4']
AudioCol = AudioData(directory_paths)
distribution = get_total_distribution(AudioCol)
    
HuffmanCode = {}
entropy = {}   
encoded = {}
bits_per_symbol = {} 
HuffmanCode, entropy, encoded, bits_per_symbol = get_encoding(distribution, AudioCol)

plt.figure()
for l, type in enumerate(distribution):
    for k, gender in enumerate(distribution[type]):
        # Plot a horizontal line
        plt.subplot(3, 2, l+3*k+1)
        
        plt.axhline(y=entropy[type][gender], color='r', linestyle='--', label='Entropy')
        plt.axhline(y=16, color='b', linestyle='--', label='Original Bits per Symbol')

        plt.bar(bits_per_symbol[type][gender].keys(), bits_per_symbol[type][gender].values())
        plt.xlabel('Index')
        plt.ylabel('Bits per Symbol')
        plt.ylim(10, 17)
        if type == 'diff':
            plt.title('Bits per Symbol for Gender: ' + gender + ', Type: ' + "Delta")
        else:
            plt.title('Bits per Symbol for Gender: ' + gender + ', Type: ' + "Amplitude")
        
        
plt.show()       


# Create time axis
time = np.arange(0, len(AudioCol.audio_files[0].audio_array)) / AudioCol.audio_files[0].sample_rate

# Plot audio data
plt.plot(time, AudioCol.audio_files[0].audio_array)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Data')
plt.show()

if not skip_plot_distributions:
    plt.figure(f'distributions')       
    for l,type in enumerate(distribution):
        for k,gender in enumerate(distribution[type]):
            # Bar plot of orig distribution
            print(f'Plotting {type}. {gender} distribution')
            sub = plt.subplot(3, 2, l+3*k+1)
            
            plt.bar([key for key in distribution[type][gender].keys() if -10000 <= key <= 10000], [value for key, value in distribution[type][gender].items() if -10000 <= key <= 10000])
            plt.ylabel('Probability')
            plt.xlabel('Amplitude' if type == 'orig' else "Delta")
            plt.title(f'{"Amplitude" if type =="orig" else "Delta"} distribution for {gender} Data')
            plt.ylim(0, max([value for key, value in distribution[type][gender].items() if -10000 <= key <= 10000]) * 0.1)
    plt.tight_layout()
    plt.show()








