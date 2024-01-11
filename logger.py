import logging
import os
from datetime import datetime

FILE_NAME = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
LOG_FILE = f"{FILE_NAME}.log"

LOG_PATH = os.path.join(os.getcwd(),"Logs",LOG_FILE)
os.makedirs(LOG_PATH,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_PATH,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def text_corpus(x):
    string_format = str(x).lower()
    lower_words=re.sub('[^a-zA-Z]+',' ',string_format).strip()
    #lower_words = lower_words.split()
    token = word_tokenize(lower_words)
    token_word = [t for t in token if t not in (stopword_auditor,StopWords_Currencies,StopWords_DatesandNumbers,StopWords_Generic,StopWords_GenericLong,StopWords_Geographic,StopWords_Names) ]
    lemantizzed = [lem.lemmatize(w) for w in token_word]
    return lemantizzed