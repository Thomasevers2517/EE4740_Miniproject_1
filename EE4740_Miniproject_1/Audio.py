import zipfile
import io
import wave

import wave
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

class AudioData:
    def __init__(self, directory_paths):
        self.audio_files = []
        # Get a list of all .zip files in the directory
        for directory_path in directory_paths:
            zip_files = glob.glob(os.path.join(directory_path, '*.zip'))
            print(zip_files)
            
            for i, zip_file_path in enumerate(zip_files):
                self.audio_files.append(Audio(zip_file_path, i))
    def encodeDifferential(self):
        for audio_sample in self.audio_files:
            audio_sample.calculateDifferential()
            
            

 
class Audio:
    def __init__(self, zip_file_path, index):
        self.audio_data = None
        self.audio_array = None
        self.time = None
        self.sample_rate = None
        self.gender = None
        self.person = None
        self.index = None
        self.differential = None
        self.orig_distribution = None
        self.differential_distribution = None
        self.orig_entropy = None
        self.differential_entropy = None
        
        
        self.getAudioData(zip_file_path) 
        self.getPropFromZip(zip_file_path, index)  
        self.differential = self.encodeDifferential(self.audio_array)
        self.orig_distribution =  self.getDistribution(self.audio_array)
        self.differential_distribution = self.getDistribution(self.differential)
        self.orig_entropy = self.getEntopy(self.orig_distribution)
        self.differential_entropy = self.getEntopy(self.differential_distribution)
        

    def getAudioData(self, zip_file_path):
        print(f'Processing {zip_file_path}...')
            # Open the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Get a list of all .wav files in the zip
            wav_files = [file for file in zip_ref.namelist() if file.endswith('.wav')]
            assert len(wav_files) == 1, f'Expected 1 .wav file in {zip_file_path}, but found {len(wav_files)}'
            for wav_file_name in wav_files:
                # Extract the .wav file from the zip
                zip_ref.extract(wav_file_name)

                # Open the extracted .wav file
                with wave.open(wav_file_name, 'rb') as wav_file:
                    # Read the audio data
                    self.audio_data = wav_file.readframes(wav_file.getnframes())
                self.audio_array = np.frombuffer(self.audio_data, dtype=np.int16)
                self.sample_rate = wav_file.getframerate()
                os.remove(wav_file_name)
                
    def getPropFromZip(self, zip_file_path, index):
        zip_file_path = zip_file_path.replace('EE4740_Miniproject_1\\', '')
        self.gender = zip_file_path[0]
        self.person = int(zip_file_path[1])
        self.index = index  
                
    def encodeDifferential(self, audio_array):
        differential = np.diff(audio_array)
        return differential
    
    def decodeDifferential(self, differential):
        audio_array = np.cumsum(differential)
        return audio_array
    
    def getDistribution(self, data):
        unique_values, counts = np.unique(data, return_counts=True)
        sorted_indices = np.argsort(-counts)
        sorted_values = unique_values[sorted_indices]
        sorted_counts = counts[sorted_indices]
        
        distribution = dict(zip(sorted_values, sorted_counts/len(data)))
        return distribution
    
    def getEntopy(self, distribution):
        entropy = -np.sum([count * np.log2(count) for count in distribution.values()])
        return entropy    
        