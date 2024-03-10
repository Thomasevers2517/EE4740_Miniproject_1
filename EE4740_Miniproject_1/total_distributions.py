def get_total_distribution(AudioCol):
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
        print(f'Adding to distributions audio file --> {audio_file.gender}.{audio_file.person}.{audio_file.index}')
        assert abs(sum(audio_file.differential_distribution.values())-1) < 0.0001, f'error in differential distribution'
        assert abs(sum(audio_file.orig_distribution.values())-1) < 0.0001, f'error in orig distribution'
        
        for key, value in audio_file.orig_distribution.items():
            if key in distribution['orig'][audio_file.gender]:
                distribution['orig'][audio_file.gender][key] += value/8

            else:
                distribution['orig'][audio_file.gender][key] = value/8
            if key in distribution['orig']['all']:
                distribution['orig']['all'][key] += value/16
            else:
                distribution['orig']['all'][key] = value/16
        
        for key, value in audio_file.differential_distribution.items():
            if key in distribution['diff'][audio_file.gender]:
                distribution['diff'][audio_file.gender][key] += value/8
                
            else:
                distribution['diff'][audio_file.gender][key] = value/8
            if key in distribution['diff']['all']:
                distribution['diff']['all'][key] += value/16
            else:
                distribution['diff']['all'][key] = value/16
    return distribution