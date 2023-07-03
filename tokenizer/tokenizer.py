from __future__ import unicode_literals
from hazm import *


def normalizing_sentences(text, doc_id, normalizer, stemmer, lemmatizer):
    print("normalizing file number " + doc_id)
    return tokenizing_words(normalizer.normalize(text), doc_id, stemmer, lemmatizer)


def tokenizing_words(normalized_text, doc_id, stemmer, lemmatizer):
    print("tokenizing file number " + doc_id)
    tokens = word_tokenize(normalized_text)
    for i in range(len(tokens)):
        tokens[i] = [tokens[i], i]
    return stemming_words(tokens, doc_id, stemmer, lemmatizer)


def stemming_words(tokens, doc_id, stemmer, lemmatizer):
    print("stemming file number " + doc_id)

    for i in range(len(tokens)):
        tokens[i][0] = lemmatizer.lemmatize(tokens[i][0])
    return omit_stop_words(tokens, doc_id)


def omit_stop_words(processed_tokens, doc_id):
    f = open("./stop_words.txt", 'r')
    stop_words = f.readlines()
    f.close()
    f = open("./punctuations.txt", 'r')
    punctuations = f.readlines()
    f.close()
    print("eliminating stop words file number " + doc_id)
    final_tokens = []
    if "" in processed_tokens:
        processed_tokens.remove("")
    punctuations = "".join(punctuations).split("\n")
    stop_words = "".join(stop_words).split("\n")
    for i in range(len(processed_tokens)):
        if processed_tokens[i][0] in stop_words or processed_tokens[i][0] in punctuations:
            continue
        new_tuple = (processed_tokens[i][0], doc_id + "-" + str(processed_tokens[i][1]))
        final_tokens.append(new_tuple)
    return final_tokens
