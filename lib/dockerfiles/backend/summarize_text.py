import os

from collections import Counter
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords


def summarize(max_words, num_sents, url, user_text):
    # Use webscraping to obtain the text.
    if url:
        page = requests.get(url)
        page.raise_for_status()
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        p_elems = [element.text for element in soup.find_all('p')]

        text = ' '.join(p_elems)  # Make sure to join on a space!
    else:
        text = user_text

    # Fix typos, remove extra spaces, digits, and punctuation.
    text = text.replace(')mowing', 'knowing')
    text = re.sub('\s+', ' ', text) 
    text_edit = re.sub('[^a-zA-Z]', ' ', text)
    text_edit = re.sub('\s+', ' ', text_edit)

    # Request input.
    
    max_words = max_words
    num_sents = num_sents
                      
    # Run functions to generate sentence scores.
    speech_edit_no_stop = remove_stop_words(text_edit)
    word_freq = get_word_freq(speech_edit_no_stop)
    sent_scores = score_sentences(text, word_freq, max_words)

    # Print the top-ranked sentences.
    counts = Counter(sent_scores)
    summary = counts.most_common(int(num_sents))
    result_summary = ""
    print("\nSUMMARY:")
    for i in summary:
        # print(i[0])
        result_summary += '<br>' + i[0] +'</br>' 
    print(result_summary)
    return result_summary


def remove_stop_words(speech_edit):
    """Remove stop words from string and return string."""
    stop_words = set(stopwords.words('english'))
    speech_edit_no_stop = ''
    for word in nltk.word_tokenize(speech_edit):
        if word.lower() not in stop_words:
            speech_edit_no_stop += word + ' '  
    return speech_edit_no_stop

def get_word_freq(speech_edit_no_stop):
    """Return a dictionary of word frequency in a string."""
    word_freq = nltk.FreqDist(nltk.word_tokenize(speech_edit_no_stop.lower()))
    return word_freq

def score_sentences(speech, word_freq, max_words):
    """Return dictionary of sentence scores based on word frequency."""
    sent_scores = dict()
    sentences = nltk.sent_tokenize(speech)
    for sent in sentences:
        sent_scores[sent] = 0
        words = nltk.word_tokenize(sent.lower())
        sent_word_count = len(words)
        if sent_word_count <= int(max_words):
            for word in words:
                if word in word_freq.keys():
                    sent_scores[sent] += word_freq[word]
            sent_scores[sent] = sent_scores[sent] / sent_word_count
    return sent_scores
