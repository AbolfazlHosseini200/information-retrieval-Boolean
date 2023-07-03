from __future__ import unicode_literals
import file_reader
from hazm import *
# import stopwords_guilannlp

# stopwords = stopwords_guilannlp.stopwords_output("Persian", "nar")
# print(stopwords)
# address = "../IR_data_news_12k.json"
# json_file = file_reader.read_file(address)
# print(len(json_file))
normalizer = Normalizer()
print(normalizer.normalize("سلام ۱۲ امیدوارم خوب باشید مهربان ها"))
# tagger = POSTagger(model='resources/postagger.model')
# a = word_tokenize("را از به سلام درست غلط در .")
# print(a)
# a = tagger.tag(a)
# print(a)
# lemmatizer = Lemmatizer()
# print(lemmatizer.lemmatize('کتاب‌ها'))
# stemmer = Stemmer()
# print(stemmer.stem('از'))
# print()