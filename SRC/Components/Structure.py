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

# Download NLTK data to user directory (portable)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = stopwords.words('english')


class Analysis:
    
    
    def StopWords_data(self, file_path=None):
        """Use NLTK stopwords if external files are not available"""
        try:
            if file_path and os.path.exists(file_path):
                # Try to load custom stopwords if path exists
                stopword_auditor = open(os.path.join(file_path, 'StopWords_Auditor.txt'), 'r', encoding='ISO-8859-1')
                StopWords_Currencies = open(os.path.join(file_path, 'StopWords_Currencies.txt'), 'r', encoding='ISO-8859-1')
                StopWords_DatesandNumbers = open(os.path.join(file_path, 'StopWords_DatesandNumbers.txt'), 'r', encoding='ISO-8859-1')
                StopWords_Generic = open(os.path.join(file_path, 'StopWords_Generic.txt'), 'r', encoding='ISO-8859-1')
                StopWords_GenericLong = open(os.path.join(file_path, 'StopWords_GenericLong.txt'), 'r', encoding='ISO-8859-1')
                StopWords_Geographic = open(os.path.join(file_path, 'StopWords_Geographic.txt'), 'r', encoding='ISO-8859-1')
                StopWords_Names = open(os.path.join(file_path, 'StopWords_Names.txt'), 'r', encoding='ISO-8859-1')
                return stopword_auditor, StopWords_Currencies, StopWords_DatesandNumbers, StopWords_Generic, StopWords_GenericLong, StopWords_Geographic, StopWords_Names
            else:
                # Fallback to NLTK stopwords
                return stop_words, [], [], [], [], [], []
        except (FileNotFoundError, IOError):
            # Fallback to NLTK stopwords
            return stop_words, [], [], [], [], [], []
    
    
    def MasterDictionar_data(self, file_path=None):
        """Use basic positive/negative word lists if external files are not available"""
        try:
            if file_path and os.path.exists(file_path):
                # Try to load custom dictionaries if path exists
                file_neg = open(os.path.join(file_path, 'negative-words.txt'), 'r', encoding='ISO-8859-1')
                file_neg.seek(0)
                neg_split = file_neg.read().split()
                
                file_pos = open(os.path.join(file_path, 'positive-words.txt'), 'r', encoding='ISO-8859-1')
                file_pos.seek(0)
                pos_split = file_pos.read().split()
                
                return pos_split, neg_split
            else:
                # Fallback to basic word lists
                positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'perfect', 'best', 'love', 'like', 'happy', 'pleased', 'satisfied', 'successful']
                negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike', 'sad', 'angry', 'disappointed', 'failed', 'problem', 'issue', 'wrong', 'error']
                return positive_words, negative_words
        except (FileNotFoundError, IOError):
            # Fallback to basic word lists
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'perfect', 'best', 'love', 'like', 'happy', 'pleased', 'satisfied', 'successful']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike', 'sad', 'angry', 'disappointed', 'failed', 'problem', 'issue', 'wrong', 'error']
            return positive_words, negative_words
    
    def text_corpus(self, x):
        stopword_auditor, StopWords_Currencies, StopWords_DatesandNumbers, StopWords_Generic, StopWords_GenericLong, StopWords_Geographic, StopWords_Names = self.StopWords_data()
        
        string_format = str(x).lower()
        lower_words = re.sub('[^a-zA-Z]+', ' ', string_format).strip()
        token = word_tokenize(lower_words)
        
        # Combine all stopwords into a single list
        all_stopwords = set(stop_words)  # Start with NLTK stopwords
        if isinstance(stopword_auditor, list):
            all_stopwords.update(stopword_auditor)
        
        token_word = [t for t in token if t not in all_stopwords]
        lemantizzed = [lem.lemmatize(w) for w in token_word]
        return lemantizzed
    
    def count_syllables(self, word):
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

    def calculate_complexity_percentage(self, words):
        num_complex_words = sum(1 for word in words if self.count_syllables(word) >= 2)
        total_words = len(words)
        no_of_complex_words = num_complex_words 
        percentage_complex_words = (num_complex_words / total_words) * 100 if total_words > 0 else 0
        return percentage_complex_words, no_of_complex_words

    def count_syllables_per_word(self, words):
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

    
