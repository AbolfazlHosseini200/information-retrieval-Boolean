from __future__ import unicode_literals
from hazm import *
import file_reader

address = "../../IR_data_news_12k.json"
json_file = file_reader.read_file(address)
f = open("./stop_words.txt", 'r')
stop_words = f.readlines()
f.close()
f = open("./punctuations.txt", 'r')
punctuations = f.readlines()
f.close()
normalizer = Normalizer()
lemmatizer = Lemmatizer()
for i in json_file:
    print("pending file number " + i)
    text = json_file[i]['content']
    text = normalizer.normalize(text)
    text = word_tokenize(text)
    text = list(set(text))
    final_tokens = []
    if "" in text:
        text.remove("")
    punctuations = "".join(punctuations).split("\n")
    stop_words = "".join(stop_words).split("\n")

    for j in range(len(text)):
        if text[j] in stop_words or text[j] in punctuations:
            continue
        final_tokens.append(text[j])
    saving = []
    for j in range(len(final_tokens)):
        final_tokens[j] = lemmatizer.lemmatize(final_tokens[j])
        new_tuple = (final_tokens[j], i)
        saving.append(new_tuple)
    with open('tokens.txt', 'a') as f:
        f.write(str(saving) + '\n')
