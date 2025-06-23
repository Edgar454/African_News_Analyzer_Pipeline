import re
import spacy
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import numpy as np

# Importing sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import pyLDAvis.lda_model

nlp = spacy.load("fr_core_news_sm")
en_nlp = spacy.load('en_core_web_sm')



french_regex_to_exclude = [
    r"africa presse",
    r'<a\s+href=["]{1,2}[^"]+["]{1,2}>?',
    r"<p>",
    r"</a>",
    r"</p>",
    r"https://\S+\.com",
    r"\n"
]
def exclude_regex(text):
    for regex in french_regex_to_exclude:
        text= re.sub(regex,"", text)
    return text
    
def lemmatize_token(token):
  return token.lemma_.strip()

def process_french_text(text):
    text = exclude_regex(text.lower())
    complete_doc  = nlp(text)

    words = [
         lemmatize_token(token)
         for token in complete_doc
         if not token.is_stop and not token.is_punct
     ]
    return words

def process_english_text(text):
    complete_doc  = en_nlp(text)
    words = [
         lemmatize_token(token)
         for token in complete_doc
         if not token.is_stop and not token.is_punct
     ]  
    return words

def process_text(text):
    try:
        lang = detect(text)
        if lang =="fr":
            clean_text = process_french_text(text)
        elif lang == "en":
            clean_text = process_english_text(text)
        return " ".join(clean_text)

    except LangDetectException:
        return " "

def create_dictionary_and_corpus(texts):
    """
    Create a dictionary and corpus for topic modeling from a list of texts.
    
    Args:
        texts (list): A list of preprocessed texts.
        
    Returns:
        tuple: A tuple containing the dictionary and corpus.
    """
    vectorizer = CountVectorizer()
    doc_term_matrix = vectorizer.fit_transform(texts)
    
    return vectorizer , doc_term_matrix

def extract_topics(texts, num_topics=5 , n_top_words=10):
    """
    Perform topic modeling on a list of texts using LDA.
    
    Args:
        texts (list): A list of preprocessed texts.
        num_topics (int): The number of topics to extract.
        
    Returns:
        list: A list of topics, each represented as a list of words.
    """
    # Create dictionary and corpus
    vectorizer , doc_term_matrix = create_dictionary_and_corpus(texts)
    
    # Train the LDA model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(doc_term_matrix)
    
    # Get the topics
    topics_data = []

    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        topic_terms = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topic_weights = [float(topic[i]) for i in topic.argsort()[:-n_top_words - 1:-1]]

        topics_data.append({
            "topic": f"Topic {topic_idx}",
            "terms": topic_terms,
            "weights": topic_weights
        })

    return topics_data , vectorizer, lda , doc_term_matrix

def visualize_topics(lda_model, vectorizer, doc_term_matrix , output_dir="output"):
    """
    Visualize the topics using pyLDAvis.
    
    Args:
        lda_model: The trained LDA model.
        vectorizer: The vectorizer used to create the document-term matrix.
        texts (list): The original texts used for training the model.
        
    Returns:
        None: The file is saved as an HTML file in output directory.
    """
    vis_data = pyLDAvis.lda_model.prepare(lda_model, doc_term_matrix, vectorizer)
    pyLDAvis.save_html(vis_data, f"{output_dir}/lda_visualization.html")