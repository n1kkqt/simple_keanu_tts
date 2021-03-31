import re
import numpy as np
from scipy.io import wavfile

class TextToSpeech:
    
    CHUNK = 1024

    def __init__(self, words_pron_dict:str = 'cmudict-0.7b.txt'):
        self._l = {}
        self._load_words(words_pron_dict)
        self.letter_dict={'a':["EY"],'b':['B'],'c':['S', 'IY'],'d':['D'],'e':['IY'],'f':['F'],'g':['G'],'h':['HH'],'i':['AY'],
                          'j':['JH'],'k':['K'],'l':['L'],'m':['M'],'n':['N'],'o':['OW'],'p':['P'],'q':['K', 'UW'],'r':['R'],
                          's':['S'],'t':["T"],'u':['UW'],'v':['V'],'w':['W'],'x':['K', 'S'],'y':['IH'],'z':['Z'],
                          '0':['Z', 'IY', 'R', 'OW'],'1':['W', 'AH', 'N'],'2':['T', 'UW'],'3':['TH', 'R', 'IY'],
                          '4':['F', 'AO', 'R'],'5':['F', 'AY', 'V'],'6':['S', 'IH', 'K', 'S'],'7':['S', 'EH', 'V', 'AH', 'N'],
                          '8':['EY', 'T'],'9':['N', 'AY', 'N'], "'":[' ']}

    def _load_words(self, words_pron_dict:str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    if not key[0].isalpha():
                        key = key[0]
                    self._l[key] = re.findall(r"[A-Z]+",val)
                    
                    
    def _word_to_sounds(self, word):
        if word[0] == "'":
            word = word.replace("'", '')
        word = word.replace(' ', '')
        if word[0].isalpha() or word[0].isdigit():
            sounds_list = []
            word = word.lower()
            for letter in word:
                sounds_list += self.letter_dict[letter]
            return sounds_list
        else:
            return ['.']

    def get_pronunciation(self, str_input):
        list_pron = []
        data_lst = []
        #str_input = str_input.replace("'", '')
        if str_input=='':
            str_input = '.'
        str_input = re.sub(' +', ' ', re.sub("""[^A-Za-z0-9' ]""", ' \g<0> ', str_input))
        str_input_split = [el for el in str_input.upper().split(' ') if el != '']
        for word in str_input_split:
            if word == '.':
                list_pron += word
                continue
            else:                    
                if word in self._l:
                    list_pron += self._l[word] + [' ']
                else:
                    list_pron += self._word_to_sounds(word) + [' ']
                    
        #list_pron = list_pron[:-1]

        print(list_pron)
        for sound in list_pron:
            if (sound != ' ') and (sound != '.'):
                samplerate, data = wavfile.read("norm_sounds/"+sound+".wav")
            else:
                if sound == ' ':
                    data = np.zeros((4800,2)).astype(np.int16)
                if sound == '.':
                    data = np.zeros((9600,2)).astype(np.int16)
            data_lst.append(data)
            
        audio_out = np.concatenate(data_lst)[:,0]
        
        return audio_out