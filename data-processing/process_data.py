import csv
import os
import json
from collections import defaultdict
from itertools import islice

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
spacy.prefer_gpu()

from spacy.lemmatizer import Lemmatizer
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_lg 

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

import nltk
from nltk.corpus import stopwords 
import pyLDAvis.gensim

nlp= spacy.load("en_core_web_lg")
stop_words = stopwords.words('english')
stop_words.extend(['sars','covid-19', 'cov-2','=','from', 'subject', 're', 'edu', 'use', 'not', 
                   'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 
                   'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 
                   'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 
                   'line', 'even', 'also', 'may', 'take', 'come'])

nlp.Defaults.stop_words.update(stop_words)

def lemmatize(doc):
    doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
    doc = u' '.join(doc)
    return nlp.make_doc(doc)
    
def clean_tokens(doc):
    doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True and (len(token)<=4)!=True]
    return doc


nlp.add_pipe(lemmatize,name='lemmatize',after='ner')
nlp.add_pipe(clean_tokens, name="cleanup", last=True)

fulltext_list = []
abstract_list = []
nlp.max_length = 2000000
dataset_limit = 100

with open('metadata.csv') as f_in:
    reader = csv.DictReader(f_in)
    for row in islice(reader, 0, dataset_limit):
        abstract = row['abstract']
        all_text = []
        if row['pdf_json_files']:
            for json_path in row['pdf_json_files'].split('; '):
                with open(json_path) as f_json:
                    full_text_dict = json.load(f_json)
                    for paragraph_dict in full_text_dict['body_text']:
                        paragraph_text = paragraph_dict['text']
                        section_name = paragraph_dict['section']
                        all_text.append(paragraph_text)
        nlp_abstract = nlp(abstract)
        abstract_list.append(nlp_abstract)
        nlp_fulltext = nlp(u' '.join(all_text))
        fulltext_list.append(nlp_fulltext)

def generate_corpus(doc_list):
    words=corpora.Dictionary(doc_list)
    corpus = [words.doc2bow(doc) for doc in doc_list]
    return [words,corpus]

def generate_lda_model(words,corpus):
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=words,
                                            num_topics=10, 
                                            random_state=2,
                                            update_every=1,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)  
    return lda_model

abstract_gen_corp = generate_corpus(abstract_list)
abstract_words=abstract_gen_corp[0]
abstract_corpus=abstract_gen_corp[1]
abstract_lda_model = generate_lda_model(abstract_words,abstract_corpus)

fulltext_gen_corp = generate_corpus(fulltext_list)
fulltext_words=fulltext_gen_corp[0]
fulltext_corpus=fulltext_gen_corp[1]
fulltext_lda_model = generate_lda_model(fulltext_words,fulltext_corpus)


def plotWordcloud(lda_model,stop_words):
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]

    cloud = WordCloud(stopwords=stop_words,
                      background_color='white',
                      width=2500,
                      height=1800,
                      max_words=10,
                      colormap='tab10',
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)

    topics = lda_model.show_topics(formatted=False)

    fig, axes = plt.subplots(2, 2, figsize=(10,10), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
        plt.gca().axis('off')


    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    return plt



