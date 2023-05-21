import streamlit as st

import PyPDF2
import nltk
from nltk.corpus import stopwords   
import re

nltk.download('punkt')
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def read_pdf(path: str) -> str:
  """
  Function to process the PDF file
  ----------------------------------
  Parameters: 
  path: Path to the pdf file

  Returns: Processed PDF content as String
  """
  reader = PyPDF2.PdfReader(path)
  AllText = ""
  for page_no in range(len(reader.pages)):
    current_page = reader.pages[page_no].extract_text()
    current_page = current_page.replace(" ", "")
    current_page = current_page.replace("\n", " ")
    AllText += current_page
  return AllText


HEADINGS = ["Introduction",
          "Operations Management: Oil and Gas Report", 
          "History of Operations Management", 
          "Principles of Operations Management",
          "Functions of Operations Management",
          "Operations Management Strategies",
          "Objectives of Operations Management",
          "Operations Performance",
          "Operations Management in Oil and Gas Industry",
          "Advantages and Disadvantages of Operations Management"]

def clean_text(data: str) -> str:
  """
  Function to Clean the PDF file content
  ----------------------------------
  Parameters: 
  data: Contents of the pdf file

  Returns: Cleaned PDF content
  """
  for heading in HEADINGS:
    data = data.replace(heading, "", 1) # Remove the headings and subheadings
  data = data.lower() # Convert the text to all lowercase.
  data = re.sub(r'\([^)]*\)', '', data) # Remove paranthesis with text inside 
  data = re.sub('"','', data) # remove quotations
  data = re.sub("[^a-zA-Z.]", " ", data) # remove special characters other than '.' to mark end of a sentence
  return data




st.title("Text Analysis using NLP")
st.header('Text Summarization')
file = st.file_uploader('Upload a PDF')

submit = st.button("Submit")
if submit:
    filePath = file
    inputPDF = read_pdf(filePath)
    clean_inputPDF = clean_text(inputPDF)
    all_sentences = clean_inputPDF.split(".")
    all_sentences = [_.strip() for _ in all_sentences]
    frequency_dictionary = {}
    for word in nltk.word_tokenize(clean_inputPDF):
        if word not in STOPWORDS and word != ".":
            if word not in frequency_dictionary.keys():
                frequency_dictionary[word] = 1
            else:
                frequency_dictionary[word] += 1
    max_freq = max(frequency_dictionary.values())
    word_scores = {}
    for word in frequency_dictionary.keys():
        word_scores[word] = (frequency_dictionary[word]/max_freq)
    sentence_scores = {}
    curr = 0
    for sentence in all_sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in frequency_dictionary.keys():
                if sentence not in [_[0] for _ in sentence_scores.keys()]:
                    sentence_scores[(sentence, curr)] = frequency_dictionary[word]
                else:
                    sentence_scores[(sentence, curr)] += frequency_dictionary[word]
        curr += 1

    sentence_scores = sorted(sentence_scores.items(), key = lambda x: x[1])[::-1]
    best_sentences = []
    for i in range(10):
        curr_best = sentence_scores.pop(0)
        best_sentences.append(curr_best)
    best_sentences = sorted(best_sentences, key = lambda x: x[0][1])
    st.text("Summary")
    st.write(". ".join([_[0][0].capitalize() for _ in best_sentences])+ ".")
