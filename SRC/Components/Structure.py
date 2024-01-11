from urllib.request import urlopen as uReq
import requests
import urllib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lem = WordNetLemmatizer()
nltk.data.path.append("C:\\Users\\PCLP\\AppData\\Roaming\\nltk_data")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

#C:\Users\PCLP\AppData\Roaming\nltk_data

stop_words = stopwords.words('english')


class Analysis:
    
    
    def StopWords_data(self,file_path='E:\\For_Job\\Blackcoffer\\StopWords\\'):
        stopword_auditor=open(f'{file_path}\\StopWords_Auditor.txt' ,'r',encoding='ISO-8859-1')
        StopWords_Currencies=open(f'{file_path}\\StopWords_Currencies.txt' ,'r',encoding='ISO-8859-1')
        StopWords_DatesandNumbers=open(f'{file_path}\\StopWords_DatesandNumbers.txt' ,'r',encoding='ISO-8859-1')
        StopWords_Generic=open(f'{file_path}\\StopWords_Generic.txt' ,'r',encoding='ISO-8859-1')
        StopWords_GenericLong=open(f'{file_path}\\StopWords_GenericLong.txt' ,'r',encoding='ISO-8859-1')
        StopWords_Geographic=open(f'{file_path}\\StopWords_Geographic.txt' ,'r',encoding='ISO-8859-1')
        StopWords_Names=open(f'{file_path}\\StopWords_Names.txt' ,'r',encoding='ISO-8859-1')
        
        return stopword_auditor,StopWords_Currencies,StopWords_DatesandNumbers,StopWords_Generic,StopWords_GenericLong,StopWords_Geographic,StopWords_Names
    
    
    def MasterDictionar_data(self,file_path='E:\\For_Job\\Blackcoffer\\MasterDictionary'):
        
        # Negative Dictionary 
        file_neg = open(f'{file_path}\\negative-words.txt' ,'r',encoding='ISO-8859-1')
        file_neg.seek(0)
        neg_split = file_neg.read().split()
        
        # Positive Dictionary 
        file_pos = open(f'{file_path}\\positive-words.txt' ,'r',encoding='ISO-8859-1')
        file_pos.seek(0)
        pos_split = file_pos.read().split()
        
        return pos_split,neg_split
    
    def text_corpus(self,x):
        stopword_auditor,StopWords_Currencies,StopWords_DatesandNumbers,StopWords_Generic,StopWords_GenericLong,StopWords_Geographic,StopWords_Names = self.StopWords_data()
        
        string_format = str(x).lower()
        lower_words=re.sub('[^a-zA-Z]+',' ',string_format).strip()
        #lower_words = lower_words.split()
        token = word_tokenize(lower_words)
        token_word = [t for t in token if t not in (stopword_auditor,StopWords_Currencies,StopWords_DatesandNumbers,StopWords_Generic,StopWords_GenericLong,StopWords_Geographic,StopWords_Names) ]
        lemantizzed = [lem.lemmatize(w) for w in token_word]
        return lemantizzed
    
    def count_syllables(self,word):
        vowels = ("a","e","i","o","u","y")
        count = 0
        previous_char_was_vowel = False

        for char in word:
            if char in vowels:
                if not previous_char_was_vowel:
                    count += 1
                previous_char_was_vowel = True
            else:
                previous_char_was_vowel = False

        return count

    def calculate_complexity_percentage(self,words):
        #words = text.split()
        num_complex_words = sum(1 for word in words if self.count_syllables(word) >= 2)
        total_words = len(words)
        no_of_complex_words = num_complex_words 
        percentage_complex_words = (num_complex_words / total_words) * 100
        return percentage_complex_words,no_of_complex_words
    
    def count_syllables(self,word):
        vowels = "aeiouy"
        exceptions = ["es", "ed"]
        count = 0
        previous_char_was_vowel = False

        for exception in exceptions:
            if word.endswith(exception):
                return 0  


        for char in word.lower():
            if char in vowels:
                if not previous_char_was_vowel:
                    count += 1
                previous_char_was_vowel = True
            else:
                previous_char_was_vowel = False

        return count

    def count_syllables_per_word(self,words):
        syllables_per_word = {word: self.count_syllables(word) for word in words}
        return syllables_per_word
    
    def Personal_pronoun_count(self,words_list):
        list_of_words = ['I', 'we', 'my' ,'ours','us' ]
        list_words_counts = 0
        for words in words_list:
            if words in list_of_words:
                list_words_counts += 1
        return list_words_counts
    
    def Average_Word_Length(self,words):
        count = 0
        for i in words:
            for j in i:
                count += 1
            
        return count

    
