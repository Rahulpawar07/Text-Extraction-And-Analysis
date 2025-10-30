import pandas as pd
import numpy as np
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


class data_ingestion:        
    
    def primary(self):
        """Load input data from Excel file"""
        try:
            # Use relative path from project root
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            input_path = os.path.join(base_path, "Notebook", "data", "Input.xlsx")
            data = pd.read_excel(input_path)
            return data
        except Exception as e:
            print(f'Error {e}')
            return None

            
    def secondary(self):
        """Ingesting data from a given directory and scrape those link by using beautifulsoup and returns a dataframe"""
        # Use relative path
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_path = os.path.join(base_path, "Notebook", "data", "Input.xlsx")
        data = pd.read_excel(input_path)
        
        df = data.copy()  # Create a copy to avoid modifying the original DataFrame
        updated_list = []
        No_Matching_Data = []
        
        # Use relative path for text files
        file_path = os.path.join(base_path, '..', 'Text_files')
        os.makedirs(file_path, exist_ok=True)
        
        for i, url in enumerate(df['URL']):
            try:
                response_code = requests.get(url, timeout=10)
                soup = bs(response_code.text, 'html.parser')
                
                # Safely get article title
                title_tag = soup.find('title')
                article_title = title_tag.text if title_tag else "No Title"
                
                all_text_element = soup.find("div", class_="td-post-content tagdiv-type")

                if all_text_element is not None:
                    all_text = all_text_element.get_text(strip=True, separator='\n')
                    firstdata = all_text.splitlines()
                else:
                    print(f"No matching element found in the HTML for URL: {url}")
                    firstdata = []        
                    Blank = {
                            'URL_ID': f"blackassign00{i+1}",
                            'URL': url 
                            }
                    No_Matching_Data.append(Blank)
                    
                new_dataframe = {
                        "URL_ID": df["URL_ID"][i],
                        'URL': url,
                        'article_words': f"{article_title}-{firstdata}"
                    }    
                
                updated_list.append(new_dataframe)           

                # Save to file
                filename = urllib.parse.quote_plus(url)
                filepath = os.path.join(file_path, f"{filename}.txt")
                
                with open(filepath, 'w+', encoding='utf-8') as file1:
                    file1.write(article_title)
                    file1.write(" ")
                    if firstdata:
                        file1.write("\n".join(firstdata))
                        
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                continue
                
        return pd.DataFrame(updated_list), No_Matching_Data
    
    def Handdle_Blank_link(self, blank_data):
        """Handle blank links with alternative scraping method"""
        updated_list = []
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, '..', 'Text_files')
        os.makedirs(file_path, exist_ok=True)
        
        for item in blank_data:
            i = item['URL_ID']
            j = item['URL']
            
            try:
                response_code = requests.get(j, timeout=10)
                soup = bs(response_code.text, 'html.parser')
                
                # Safely get article title
                title_tag = soup.find('title')
                article_title = title_tag.text if title_tag else "No Title"
                
                alldiv = soup.find("div", class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")

                if alldiv is not None:
                    firstdata = alldiv.text
                    
                    filename = urllib.parse.quote_plus(j)
                    filepath = os.path.join(file_path, f"{filename}.txt")
                    
                    with open(filepath, 'w+', encoding='utf-8') as file1:
                        file1.write(article_title)
                        file1.write(" ")
                        file1.write(firstdata)
                    
                    updated_dict = {
                        'URL_ID': i,
                        'URL': j,
                        'article_words': f"{article_title} - {firstdata}"
                    }
                    
                    updated_list.append(updated_dict)
                    
                else:
                    print(f"No data available for the link: {j}")
                    
            except Exception as e:
                print(f"Error processing blank link {j}: {e}")
                continue

        return pd.DataFrame(updated_list)

    
    def merged(self, df1, df2):
        """Merge dataframes and save output"""
        merged_df = pd.merge(df1, df2, on=['URL_ID', 'URL'], how='left')
        merged_df = merged_df.dropna()
        merged_df.reset_index(drop=True, inplace=True)
        
        # Use relative path for output
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_path, "Notebook", "data", "final.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        merged_df.to_csv(output_path, index=False)
        
        return merged_df

                
            
"""            
if __name__ == "__main__":
    obj = data_ingestion()
    obj1=obj.primary()
    df,remain_data=obj.secondary()
    update_df=obj.Handdle_Blank_link(remain_data)"""
    
