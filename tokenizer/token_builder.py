from __future__ import unicode_literals
import file_reader
import tokenizer
from hazm import *

address = "../../IR_data_news_5k.json"
json_file = file_reader.read_file(address)
f = open("./stop_words.txt", 'r')
stop_words = f.readlines()
f.close()
f = open("./punctuations.txt", 'r')
punctuations = f.readlines()
f.close()
normalizer = Normalizer()
stemmer = Stemmer()
lemmatizer = Lemmatizer()
counter = 0
for i in json_file:
    print("pending file number " + i)
    tokens = tokenizer.normalizing_sentences(json_file[i]['content'], i, normalizer, stemmer, lemmatizer)
    counter += len(tokens)
    with open('tokens.txt', 'a') as f:
        f.write(str(tokens) + '\n')
print('token counts:',counter)
