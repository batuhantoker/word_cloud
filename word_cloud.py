# Python code to generate wordcloud from the PDF files in the directory

import os
import string
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
import PyPDF2
import textract
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def read_file(filepath):
    pdfFileObj = open(filepath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    text = ""
    # Read all the pages
    for pg in range(num_pages):
        page = pdfReader.getPage(pg)
        text += page.extractText()
    return text

def extract_keywords(text, ignore_words=[],
                     min_word_length=0,
                     ignore_numbers=True,
                     ignore_case=True):
    # Remove words with special characters
    filtered_text = ''.join(filter(lambda x: x in string.printable, text))

    # Create word tokens from the text string
    tokens = word_tokenize(filtered_text)

    # List of punctuations to be ignored
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', '--', '-', '#', '!', '*', '"', '%']

    # Get the stopwords list to be ignored
    stop_words = stopwords.words('english')

    # Convert ignore words from user to lower case
    ignore_words_lower = [x.lower() for x in ignore_words]

    # Combine all the words to be ignored
    all_ignored_words = punctuations + stop_words + ignore_words_lower

    # Get the keywords list
    keywords = [word for word in tokens \
                if word.lower() not in all_ignored_words
                and len(word) >= min_word_length]

    # Remove keywords with only digits
    if ignore_numbers:
        keywords = [keyword for keyword in keywords if not keyword.isdigit()]

    # Return all keywords in lower case if case is not of significance
    if ignore_case:
        keywords = [keyword.lower() for keyword in keywords]

    return keywords

def create_word_cloud(keywords, maximum_words=100, bg='white', cmap='Dark2',
                      maximum_font_size=256, width=3000, height=2000,
                      random_state=42, fig_w=15, fig_h=10, output_filepath=None):
    # Convert keywords to dictionary with values and its occurences
    word_could_dict = Counter(keywords)

    wordcloud = WordCloud(background_color=bg, max_words=maximum_words, colormap=cmap,
                          stopwords=STOPWORDS, max_font_size=maximum_font_size,
                          random_state=random_state,
                          width=width, height=height).generate_from_frequencies(word_could_dict)

    plt.figure(figsize=(fig_w, fig_h))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    if output_filepath:
        plt.savefig(output_filepath, bbox_inches='tight')
    plt.show()
    plt.close()


## Initialize parameters
docs_path = os.getcwd()
ignore_words = ['Fig', 'like', 'e.g.', 'i.e.', 'one'] # These words will be ignored
all_keywords = []

for filename in os.listdir(docs_path):
    filepath = os.path.join(docs_path, filename)
    if os.path.isfile(filepath) and filename.endswith('.pdf'):
        print(f'Parsing file: {filename}')
        try:
            file_text = read_file(filepath)
            keywords = extract_keywords(file_text, min_word_length=3, ignore_words=ignore_words)
            all_keywords.extend(keywords)
        except:
            print(f'ERROR!!! Unable to parse file: {filename}. Ignoring file!!')

print(f'Completed reading all pdf files in folder:{docs_path}')
print(all_keywords)
create_word_cloud(all_keywords, bg='black', cmap='Set2', random_state=100, width=1000, height=1000)
