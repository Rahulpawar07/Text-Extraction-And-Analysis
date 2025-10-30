import pandas as pd
import nltk
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests
import urllib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings('ignore')
import os
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


from SRC.Data_ingestion import data_ingestion
from SRC.Components.Structure import Analysis


class Col_Structure:
    
    def Col_Structure_Primary(self, data):
        """Main analysis function with optimized loops and calculations"""
        updated_list = []
        
        # Pre-create Analysis instance to reuse cached data
        analysis = Analysis()
        
        # Load dictionaries once outside the loop
        positive_dictionary, negative_dictionary = analysis.MasterDictionar_data()
        
        for i, j, column in zip(data['URL_ID'], data['URL'], data['article_words']):
            # Returns tokenized words
            preprocessed_word = analysis.text_corpus(column)
            
            # 1. POSITIVE SCORE - use set intersection for efficiency
            positive_score = sum(1 for word in preprocessed_word if word.lower() in positive_dictionary)
            
            # 2. NEGATIVE SCORE - use set intersection for efficiency
            negative_score = sum(1 for word in preprocessed_word if word.lower() in negative_dictionary)
                    
            # 3. POLARITY SCORE
            total_score = positive_score + negative_score
            polarity_score = (positive_score - negative_score) / (total_score + 0.000001)
            
            # 4. SUBJECTIVITY SCORE
            subjective_score = total_score / (len(preprocessed_word) + 0.000001)
            
            # 5. AVG SENTENCE LENGTH
            total_sentences = len(nltk.tokenize.sent_tokenize(column))
            avg_sentence_lenght = round(len(preprocessed_word) / max(total_sentences, 1), 0)
            
            # 6. PERCENTAGE OF COMPLEX WORDS and 9. COMPLEX WORD COUNT
            Percentage_of_Complex_words, total_num_of_complex_words_count = analysis.calculate_complexity_percentage(preprocessed_word)
            
            # 7. FOG INDEX
            FOG_Index = 0.4 * (avg_sentence_lenght + Percentage_of_Complex_words)
            
            # 8. AVG NUMBER OF WORDS PER SENTENCE
            word_count_raw = len(column.split())
            Average_Number_of_Words_Per_Sentence = round(word_count_raw / max(total_sentences, 1), 0)
            
            # 10. WORD COUNT
            Word_Count = len(preprocessed_word)
            
            # 11. SYLLABLE PER WORD
            syllable_per_word = analysis.count_syllables_per_word(preprocessed_word)
            
            # 12. PERSONAL PRONOUNS
            personal_pronouns = analysis.Personal_pronoun_count(preprocessed_word)
            
            # 13. AVG WORD LENGTH
            word_length = analysis.Average_Word_Length(preprocessed_word)
            avg_word_lenth = round(word_length / max(len(preprocessed_word), 1), 0)
            
            final_dict = {
                            'URL_ID': i,
                            'URL': j,
                            'article_words': column,
                            'POSITIVE_SCORE': positive_score,
                            'NEGATIVE_SCORE': negative_score,
                            'POLARITY_SCORE': polarity_score,
                            'SUBJECTIVITY_SCORE': subjective_score,
                            'AVG_SENTENCE_LENGTH': avg_sentence_lenght,
                            'PERCENTAGE_OF_COMPLEX_WORDS': Percentage_of_Complex_words,
                            'FOG_INDEX': FOG_Index,
                            'AVG_NUMBER_OF_WORDS_PER_SENTENCE': Average_Number_of_Words_Per_Sentence,
                            'COMPLEX_WORD_COUNT': total_num_of_complex_words_count,
                            'WORD_COUNT': Word_Count,
                            'SYLLABLE_PER_WORD': syllable_per_word,
                            'PERSONAL_PRONOUNS': personal_pronouns,
                            'AVG_WORD_LENGTH': avg_word_lenth
                        }
            updated_list.append(final_dict)
            
        df = pd.DataFrame(updated_list)
        
        # Use relative path for output
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_path, "Notebook", "data", "Output.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        return df
            
            
            
        