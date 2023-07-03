import ast
import linked_list_classes
import pickle
import pandas as pd
import time


def persian_sort_key(t):
    return [ord(c) for c in list(t[0])]


def postings_lists_builder():
    f = open("../tokenizer/tokens.txt", "r")
    lines = f.readlines()
    posting_lists = linked_list_classes.PostingLists()
    all_tokens = []
    counter = 0
    for line in lines:
        if counter % 1000 == 0:
            print("pending doc number " + str(counter))
        counter += 1
        all_tokens += ast.literal_eval(line)
        # all_tokens = sorted(all_tokens, key=persian_sort_key)
    print("sort pending...")
    all_tokens = sorted(all_tokens, key=persian_sort_key)
    counter = 0
    tokens_length = str(len(all_tokens))
    start_time = time.time()
    last_counter = 0
    speed = 0
    for token in all_tokens:
        if counter % 100000 == 0:
            print("creating postings list step " + str(counter) + "/" + tokens_length, speed, "token per second")
        counter += 1
        if time.time() - start_time > 2:
            speed = (counter - last_counter) // (time.time() - start_time)
            start_time = time.time()
            last_counter = counter
        splitted = token[1].split("-")
        posting_lists.add_doc(token[0], splitted[0], splitted[1])
    # x = posting_lists.tokens.index("محمد")
    # print(posting_lists.freq[x])
    # print(posting_lists.tokens[0])
    print("docs:", posting_lists.tokens)
    return posting_lists
