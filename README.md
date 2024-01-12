# Text Analysis by using Python and machine learning Lib NLTK 

#   Objectie 
The objective of this assignment is to extract textual data articles from the given URL and perform text analysis to compute variables that are explained below. 

Here in this we need to extract the data from the given link and and save those data into the csv file we need to Proceed some analysis on top of the  extracted data like extraxt number of words , number of sentenses , postive count and negative count etc 

From a given link we need to extract the article text and title of the article, Those extracted text and title added into a textfile as well as output CSV file. All the extracted text file are saved in a Textfiles folder and Output.csv in

       > INPUT  > Input.xlsx

       > References > Output data structure.
       
       > Text Output > Final.csv

       > OUTPUT > Notebook/data/Output.csv

----- In this Project for Extracing the text by using Beautifulsoup

# Data set
#### Input.xlsx 
Input.xlsx
For each of the articles, given in the input.xlsx file, extract the article text and save the extracted article in a text file with URL_ID as its file name.
While extracting text,  make sure your program extracts only the article title and the article text. It should not extract the website header, footer, or anything other than the article text. 


# Output :-
#### Output.csv
    > 1.    URL_ID.

    > 2.    URL.

    > 3.    Article Words.

    > 4.    POSITIVE SCORE.

    > 5.  	NEGATIVE SCORE.
        	
    > 6.    POLARITY SCORE.

    > 7.    SUBJECTIVITY SCORE.

    > 8.    AVG SENTENCE LENGTH.

    > 9.    PERCENTAGE OF COMPLEX WORDS.

    > 10.   FOG INDEX.

    > 11.   AVG NUMBER OF WORDS PER SENTENCE.

    > 12.   COMPLEX WORD COUNT.

    > 13.   WORD COUNT.

    > 14.   SYLLABLE PER WORD.

    > 15.   PERSONAL PRONOUNS.

    > 16.   AVG WORD LENGTH.


#   Code Flow

Let's Me Explain The flow of Code :- 

    > 1. Install all the requirements file , use this code for install the neccessary packages and modules 
        pip install -r requirements.txt

    > 2. Create Module soo we need the create a setup file 
        python setup.py install

    > 3. In SRC there are 2 .py file :- 
        1. Data_Ingestion.py ---> Are used for Ingestining text link , Scrapping text  and returns a dataframe 
        2. Utils.py          ---> Are used for performing task like extracting words count , sentenses , positive score ,       negative score and fog index
        
    > 4. SRC/Components :- 
        1. Structure.py     ---> Strutural task are performed , there are multiple methods for reading text files , couting complex words , personal pronoun etc

    > 5. SRC/Pipeline :- 
        1. Training_Pipeline.py ---> As the name suggest inbuild __name__ method is used, and creating objects of the classes 

#   Steps For Terminal Run

For code run here are the few steps need to follow  try to create new terminal and run this commands on terminal :-

    > 1. pip install -r requirements.txt

    > 2. python setup.py install

    > 3. Python SRC/Pipeline/Training_pipeline.py

# Technology used 

    > 1. Python 

    > 2. Beautifulsoup

    > 3. NLTK Lib
