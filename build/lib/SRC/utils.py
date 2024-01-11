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
lem = WordNetLemmatizer()


nltk.data.path.append("C:\\Users\\PCLP\\AppData\\Roaming\\nltk_data")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')


from SRC.Data_ingestion import data_ingestion
from SRC.Components.Structure import Analysis
#from SRC.Pipeline.Training_pipeline import 

#_,df=data_ingestion.secondary()
#df.head()


class Col_Structure:
    
    
    def Col_Structure_Primary(self, data):
        Output_data = []
        updated_list = []
        
        #_,df=data_ingestion.secondary()
        for i,j,column in zip(data['URL_ID'],data['URL'],data['article_words']):
            # Returns A tokenized Words
            preprocessed_word = Analysis().text_corpus(column)
            
            # Existing Dictinary In text file
            positive_dictionary, negative_dictionary = Analysis().MasterDictionar_data()
            
            # 1.     POSITIVE SCORE
            positive_count = []
            for ps_words in preprocessed_word:
                if ps_words in positive_dictionary:
                    positive_count.append(ps_words)
            positive_score=len(positive_count)
            
            # 2.     NEGATIVE SCORE
            negative_count = []
            for ng_words in preprocessed_word:
                if ng_words in negative_dictionary:
                    negative_count.append(ng_words)
            negative_score=len(negative_count)
                    
            # 3.	POLARITY SCORE
            polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001 )
            
            # 4.	SUBJECTIVITY SCORE
            subjective_score = (positive_score + negative_score) / ((len(preprocessed_word)) + 0.000001 )
            
            # 5.	AVG SENTENCE LENGTH
            total_sentences =len(nltk.tokenize.sent_tokenize(column))
            avg_sentence_lenght = round(len(preprocessed_word)/total_sentences,0)
            
            # 6.	PERCENTAGE OF COMPLEX WORDS and 9.	COMPLEX WORD COUNT
            Percentage_of_Complex_words,total_num_of_complex_words_count=Analysis().calculate_complexity_percentage(preprocessed_word)
            
            # 7.	FOG INDEX
            FOG_Index = 0.4*(avg_sentence_lenght + Percentage_of_Complex_words)
            
            # 8.	AVG NUMBER OF WORDS PER SENTENCE
            Average_Number_of_Words_Per_Sentence=round(len(column.split())/total_sentences,0)
            
            # 9.	COMPLEX WORD COUNT
            total_num_of_complex_words_count
            
            # 10.	WORD COUNT
            Word_Count = len(preprocessed_word)
            
            # 11.	SYLLABLE PER WORD
            syllable_per_word = Analysis().count_syllables_per_word(preprocessed_word)
            
            # 12.	PERSONAL PRONOUNS
            personal_pronouns = Analysis().Personal_pronoun_count(preprocessed_word)
            
            # 13.	AVG WORD LENGTH
            word_length = Analysis().Average_Word_Length(preprocessed_word)
            avg_word_lenth=round(word_length/len(preprocessed_word),0)
            
            final_dict = {
                            'URL_ID'                            : i,
                            'URL'                               : j,
                            'article_words'                     : column,
                            'POSITIVE_SCORE'                    : positive_score,
                            'NEGATIVE_SCORE'                    : negative_score,
                            'POLARITY_SCORE'                    : polarity_score,
                            'SUBJECTIVITY_SCORE'                : subjective_score,
                            'AVG_SENTENCE_LENGTH'               : avg_sentence_lenght,
                            'PERCENTAGE_OF_COMPLEX_WORDS'       : Percentage_of_Complex_words,
                            'FOG_INDEX'                         : FOG_Index,
                            'AVG_NUMBER_OF_WORDS_PER_SENTENCE'  : Average_Number_of_Words_Per_Sentence,
                            'COMPLEX_WORD_COUNT'                : total_num_of_complex_words_count,
                            'WORD_COUNT'                        : Word_Count,
                            'SYLLABLE_PER_WORD'                 : syllable_per_word,
                            'PERSONAL_PRONOUNS'                 : personal_pronouns,
                            'AVG_WORD_LENGTH'                   : avg_word_lenth
                        }
            updated_list.append(final_dict)
            
            
        df = pd.DataFrame(updated_list)
        df.to_csv("E:\\For_Job\\Blackcoffer\\Code\\Notebook\\data\\Output.csv")
        
        return df
            
            
            
        