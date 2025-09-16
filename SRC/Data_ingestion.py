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
lem = WordNetLemmatizer()


# Download NLTK data to user directory (portable)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')


class data_ingestion:        
    
    def primary(self):
        try:
            data = pd.read_excel(os.path.join("Notebook/data","Input.xlsx"))
            #print(data.head())
            return data
        except Exception as e:
            print(f'Error {e}')

            
    def secondary(self):
        """Ingesting data from a given directory and scrape those link by using beautifulsoup and returns a dataframe"""
        # Use portable path
        data = pd.read_excel(os.path.join("Notebook", "data", "Input.xlsx"))
        df = data.copy()  # Create a copy to avoid modifying the original DataFrame
        updated_list = []
        No_Matching_Data = []
        Blank_link = {}
        
        for i, url in enumerate(df['URL']):
            try:
                response_code = requests.get(url, timeout=10)
                soup = bs(response_code.text, 'html.parser')
                article_title = soup.find('title').text if soup.find('title') else "No Title"
                
                all_text_element = soup.find("div", class_="td-post-content tagdiv-type")

                if all_text_element is not None:
                    all_text = all_text_element.get_text(strip=True, separator='\n')
                    firstdata = all_text.splitlines()
                else:
                    print(f"No matching element found in the HTML for URL: {url}")
                    firstdata = []        
                    Blank_link[f"blackassign00{i+1}"] = url        
                    Blank = {
                            'URL_ID' : f"blackassign00{i+1}" ,
                            'URL'    : url 
                            }
                    No_Matching_Data.append(Blank)
                    
                 
                new_dataframe = {
                        "URL_ID": df["URL_ID"][i],
                        'URL' : url,
                        'article_words':f"{article_title}-{firstdata}"
                    }    
                
                updated_list.append(new_dataframe)           
                    

                filename = urllib.parse.quote_plus(url)
                # Use portable path and ensure directory exists
                file_path = 'Text_files'
                os.makedirs(file_path, exist_ok=True)
                space = " "
                    
                with open(os.path.join(file_path, f"{filename}.txt"), 'w+', encoding='utf-8') as file1:
                    file1.writelines(article_title)
                    file1.writelines(space)
                    if firstdata is None:
                        firstdata = 'No data found'
                    else:
                        file1.writelines(firstdata)
                        
            except requests.exceptions.RequestException as e:
                print(f"Error accessing URL {url}: {e}")
                # Add to blank list for manual handling if needed
                Blank_link[f"blackassign00{i+1}"] = url        
                Blank = {
                        'URL_ID' : f"blackassign00{i+1}" ,
                        'URL'    : url 
                        }
                No_Matching_Data.append(Blank)
                continue
        return pd.DataFrame(updated_list),No_Matching_Data
    
    
    def Handdle_Blank_link(self,blank_data):
        updated_list = []
        
        for item in blank_data:
            i = item['URL_ID']
            j = item['URL']
            try:
                response_code = requests.get(j, timeout=10)
                soup = bs(response_code.text, 'html.parser')
                article_title = soup.find('title').text if soup.find('title') else "No Title"
                
                alldiv = soup.find("div", class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")

                if alldiv is not None:
                    firstdata = alldiv.text
                    
                    filename = urllib.parse.quote_plus(j)
                    # Use portable path and ensure directory exists
                    file_path = 'Text_files'
                    os.makedirs(file_path, exist_ok=True)
                    space = " "
                        
                    with open(os.path.join(file_path, f"{filename}.txt"), 'w+') as file1:
                        file1.writelines(article_title)
                        file1.writelines(space)
                        file1.writelines(firstdata)
                    
                
                    updated_dict = {
                        'URL_ID': i,
                        'URL': j,
                        'article_words': f"{article_title} - {firstdata}"
                    }
                    
                    
                    updated_list.append(updated_dict)
                    
                else:
                    print(f"No data available for the link: {j}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Error accessing URL {j}: {e}")
                continue


        df = pd.DataFrame(updated_list)
        return df

    
    
    def merged(self,df1,df2):
        # Handle empty dataframes
        if df1.empty and df2.empty:
            print("No data available for analysis")
            return pd.DataFrame()
        elif df2.empty:
            merged_df = df1.copy()
        elif df1.empty:
            merged_df = df2.copy()
        else:
            # Ensure both dataframes have the required columns
            required_cols = ['URL_ID', 'URL']
            if all(col in df1.columns for col in required_cols) and all(col in df2.columns for col in required_cols):
                merged_df = pd.merge(df1, df2, on=['URL_ID', 'URL'], how='outer')
            else:
                # Fallback to concatenation if merge columns don't match
                merged_df = pd.concat([df1, df2], ignore_index=True)
        
        merged_df = merged_df.dropna()
        merged_df.reset_index(drop=True, inplace=True)
        
        # Use portable path and ensure directory exists
        output_dir = os.path.join("Notebook", "data")
        os.makedirs(output_dir, exist_ok=True)
        merged_df.to_csv(os.path.join(output_dir, "final.csv"), index=False)
        
        return merged_df

                
            
"""            
if __name__ == "__main__":
    obj = data_ingestion()
    obj1=obj.primary()
    df,remain_data=obj.secondary()
    update_df=obj.Handdle_Blank_link(remain_data)"""
    
