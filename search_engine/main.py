import posting_lists_filler as plist_builder
import linked_list_classes as ll
import json
from hazm import *

lemmatizer = Lemmatizer()
stemmer = Stemmer()

linked_list = ll.LinkedList()
plist = plist_builder.postings_lists_builder()


# In[10]:
def read_file(url):
    f = open(url)
    data = json.load(f)
    return data


def print_array(doc_id, arr, topic):
    print("doc id:", doc_id,'title:',topic)
    for i in arr:
        print(i, end=" ")
    print()


def phrase_finder(string, plist):
    string = string.replace('"', '')
    arr = string.split(" ")
    word_nodes = []
    for i in range(len(arr)):
        if arr[i] in plist.tokens:
            word_nodes.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(arr[i]))])
        else:
            return None
    intersect_finder = []
    same_docs = []
    for i in range(13000):
        intersect_finder.append(0)
    for i in word_nodes:
        cur = i.first_doc
        while not cur.doc_id == -1:
            intersect_finder[cur.doc_id] += 1
            if intersect_finder[cur.doc_id] == len(word_nodes):
                same_docs.append(cur.doc_id)
            cur = cur.next
    phrase_positions = []
    cur1 = word_nodes[0].first_doc
    cur2 = word_nodes[1].first_doc
    while True:
        if cur1.doc_id == -1 or cur2.doc_id == -1:
            break
        if cur1.doc_id == cur2.doc_id and cur1.doc_id in same_docs:
            #             print(cur1.positions, cur2.positions)
            for i in cur1.positions:
                if i + 1 in cur2.positions:
                    new_tuple = (cur1.doc_id, i)
                    #                     print(new_tuple)
                    phrase_positions.append(new_tuple)
            cur1 = cur1.next
            cur2 = cur2.next
        elif cur1.doc_id > cur2.doc_id:
            cur2 = cur2.next
        else:
            cur1 = cur1.next
    #     print(phrase_positions, "test")
    for o in range(2, len(word_nodes)):
        cur1 = word_nodes[o].first_doc
        while True:
            if cur1.doc_id == -1:
                break
            if cur1.doc_id in same_docs:
                for k in phrase_positions[:]:
                    if cur1.doc_id == k[0]:
                        if not k[1] + o in cur1.positions:
                            phrase_positions.remove(k)
            cur1 = cur1.next
    return phrase_positions


def phrase_processor(phrases, plist):
    res = []
    for i in phrases:
        res.append(phrase_finder(i, plist))
    return res


def find_intersect(set1, set2):
    res = ll.Tokens(set1.word + "-" + set2.word)
    cur1 = set1.first_doc
    cur2 = set2.first_doc
    while True:
        if cur1.doc_id == -1 or cur2.doc_id == -1:
            return res
        if cur1.doc_id == cur2.doc_id:
            res.add_doc_id(cur1.doc_id, 0)
            cur1 = cur1.next
            cur2 = cur2.next
        elif cur1.doc_id > cur2.doc_id:
            cur2 = cur2.next
        else:
            cur1 = cur1.next


def find_nots(set1, set2):
    res = ll.Tokens(set1.word + "-!" + set2.word)
    cur1 = set1.first_doc
    cur2 = set2.first_doc
    #     print(set1.word)
    while True:
        #         print("cur1:",cur1.doc_id,"cur2:",cur2.doc_id)
        if cur1.doc_id == -1:
            return res
        if cur2.doc_id == -1:
            while not cur1.doc_id == -1:
                res.add_doc_id(cur1.doc_id, 0)
                cur1 = cur1.next
            return res
        if cur1.doc_id == cur2.doc_id:
            now = cur1.doc_id
            while now == cur1.doc_id:
                cur1 = cur1.next
            while now == cur2.doc_id:
                cur2 = cur2.next
            continue
        elif cur2.doc_id > cur1.doc_id:
            res.add_doc_id(cur1.doc_id, 0)
            cur1 = cur1.next
        else:
            cur2 = cur2.next


address = "../../IR_data_news_12k.json"
json_file = read_file(address)
normalizer = Normalizer()
print("welcome to abol's search engine:")
while True:
    inp = input("enter your search query:")
    print(inp)
    unprocessed = inp.split(" ")
    queries = []
    arr = []
    flag = False
    double_quotes = []
    doc_frq = []
    for i in range(20000):
        doc_frq.append(0)
    # find phrases
    for i in unprocessed:
        if '"' in i and not flag:
            flag = True
            double_quotes.append(i)
            continue
        if not flag:
            queries.append(i)
        else:
            double_quotes[-1] = double_quotes[-1] + " " + i
            if '"' in i:
                flag = False
    print(double_quotes)
    print(queries)
    # find not includes
    not_include = []
    for i in queries:
        if i.startswith("!"):
            not_include.append(i)
        else:
            arr.append(i)
    print(not_include)
    # find each words node in postings lists
    word_nodes = []
    for i in range(len(arr)):
        if arr[i] in plist.tokens:
            #             print(plist.posting_list[plist.tokens.index(arr[i])].first_doc.positions)
            word_nodes.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(stemmer.stem(arr[i])))])
        else:
            print("we couldn't find word " + arr[i] + " in our docs!!!")

    # find not include nodes in postings lists
    not_include_results = []
    for i in range(len(not_include)):
        the_word = not_include[i][1:]
        if the_word in plist.tokens:
            not_include_results.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(stemmer.stem(the_word)))])

    phrase_results = phrase_processor(double_quotes, plist)
    if len(word_nodes) > 0:
        linked_list = word_nodes[0]

    for i in word_nodes:
        cur = i.first_doc
        added_docs = []
        while not cur.doc_id == -1:
            if cur.doc_id not in added_docs:
                added_docs.append(cur.doc_id)
                doc_frq[cur.doc_id] += 1
            cur = cur.next
    #     print(phrase_results)
    for i in phrase_results:
        docs_added = []
        for j in i:
            if j[0] not in docs_added:
                docs_added.append(j[0])
                doc_frq[j[0]] += 1
    for i in not_include_results:
        cur = i.first_doc
        while not cur.doc_id == -1:
            doc_frq[cur.doc_id] = 0
            cur = cur.next
    counter = 0
    done = False
    #     print(doc_frq)

    for i in range(len(word_nodes) + len(double_quotes), 0, -1):
        for j in range(len(doc_frq)):
            if doc_frq[j] == i:
                content = word_tokenize(json_file[str(j)]['content'])
                topic = json_file[str(j)]['title']
                for k in word_nodes:
                    cur = k.first_doc
                    while True:
                        if cur.doc_id == -1:
                            break
                        if cur.doc_id == j:
                            for x in cur.positions:
                                print_array(j, content[x - 5:x + 5],topic)
                        cur = cur.next
                for k in phrase_results:
                    for x in k:
                        if x[0] == j:
                            print_array(j, content[x[1] - 10:x[1] + 10],topic)
                #                 print("doc_id:",j)
                counter += 1
                if counter == 5:
                    done = True
                    break
        if done:
            break

