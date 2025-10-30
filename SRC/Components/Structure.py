from urllib.request import urlopen as uReq
import requests
import urllib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data only once if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Initialize lemmatizer and stop_words once at module level
lem = WordNetLemmatizer()
stop_words = stopwords.words('english')


class Analysis:
    # Cache for stopwords and dictionaries to avoid repeated file I/O
    _stopwords_cache = None
    _master_dict_cache = None
    _regex_pattern_cache = None
    
    def StopWords_data(self, file_path=None):
        """Load stopwords from files with caching for performance"""
        if Analysis._stopwords_cache is not None:
            return Analysis._stopwords_cache
            
        if file_path is None:
            # Use relative path from project root
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_path, 'StopWords')
        
        # Load all stopwords into sets for faster lookups
        stopwords_set = set()
        stopword_files = [
            'StopWords_Auditor.txt',
            'StopWords_Currencies.txt',
            'StopWords_DatesandNumbers.txt',
            'StopWords_Generic.txt',
            'StopWords_GenericLong.txt',
            'StopWords_Geographic.txt',
            'StopWords_Names.txt'
        ]
        
        for filename in stopword_files:
            filepath = os.path.join(file_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='ISO-8859-1') as f:
                    stopwords_set.update(word.strip().lower() for word in f.read().split())
        
        Analysis._stopwords_cache = stopwords_set
        return stopwords_set
    
    
    def MasterDictionar_data(self, file_path=None):
        """Load master dictionary with caching for performance"""
        if Analysis._master_dict_cache is not None:
            return Analysis._master_dict_cache
            
        if file_path is None:
            # Use relative path from project root
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_path, 'MasterDictionary')
        
        # Load dictionaries as sets for O(1) lookup instead of O(n)
        neg_file_path = os.path.join(file_path, 'negative-words.txt')
        pos_file_path = os.path.join(file_path, 'positive-words.txt')
        
        neg_set = set()
        pos_set = set()
        
        if os.path.exists(neg_file_path):
            with open(neg_file_path, 'r', encoding='ISO-8859-1') as file_neg:
                neg_set = set(word.strip().lower() for word in file_neg.read().split())
        
        if os.path.exists(pos_file_path):
            with open(pos_file_path, 'r', encoding='ISO-8859-1') as file_pos:
                pos_set = set(word.strip().lower() for word in file_pos.read().split())
        
        Analysis._master_dict_cache = (pos_set, neg_set)
        return pos_set, neg_set
    
    
    def _get_regex_pattern(self):
        """Cache compiled regex pattern for better performance"""
        if Analysis._regex_pattern_cache is None:
            Analysis._regex_pattern_cache = re.compile(r'[^a-zA-Z]+')
        return Analysis._regex_pattern_cache
    
    def text_corpus(self, x):
        """Optimized text preprocessing with cached stopwords"""
        stopwords_set = self.StopWords_data()
        
        string_format = str(x).lower()
        # Use cached compiled regex pattern
        pattern = self._get_regex_pattern()
        lower_words = pattern.sub(' ', string_format).strip()
        
        token = word_tokenize(lower_words)
        # Filter using set membership (O(1)) instead of tuple membership
        token_word = [t for t in token if t.lower() not in stopwords_set]
        lemantizzed = [lem.lemmatize(w) for w in token_word]
        return lemantizzed
    
    
    def count_syllables(self, word):
        """Count syllables in a word with special handling for exceptions"""
        vowels = "aeiouy"
        exceptions = ["es", "ed"]
        count = 0
        previous_char_was_vowel = False

        # Check for exceptions
        for exception in exceptions:
            if word.endswith(exception):
                return 0  

        # Count vowel groups
        for char in word.lower():
            if char in vowels:
                if not previous_char_was_vowel:
                    count += 1
                previous_char_was_vowel = True
            else:
                previous_char_was_vowel = False

        return count

    def calculate_complexity_percentage(self, words):
        """Calculate percentage of complex words (2+ syllables)"""
        num_complex_words = sum(1 for word in words if self.count_syllables(word) >= 2)
        total_words = len(words)
        no_of_complex_words = num_complex_words 
        percentage_complex_words = (num_complex_words / total_words) * 100 if total_words > 0 else 0
        return percentage_complex_words, no_of_complex_words

    def count_syllables_per_word(self, words):
        """Optimized syllable counting per word"""
        return {word: self.count_syllables(word) for word in words}
    
    def Personal_pronoun_count(self, words_list):
        """Count personal pronouns using set for O(1) lookup"""
        pronouns_set = {'i', 'we', 'my', 'ours', 'us'}
        return sum(1 for word in words_list if word.lower() in pronouns_set)
    
    def Average_Word_Length(self, words):
        """Calculate total character count efficiently"""
        # Use sum with generator expression instead of nested loops
        return sum(len(word) for word in words)

    
