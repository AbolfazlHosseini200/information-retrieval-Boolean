class LinkedList:
    def __init__(self):
        self.next = None
        self.doc_id = -1
        self.positions = []

    def set_doc_id(self, doc_id, position):
        self.doc_id = int(doc_id)
        self.next = LinkedList()
        self.positions.append(int(position))


class Tokens:
    def __init__(self, word):
        self.word = word
        self.frq = 0
        self.first_doc = LinkedList()
        self.last_doc = self.first_doc

    def add_doc_id(self, doc_id, position):
        self.frq += 1
        cur = self.last_doc
        # print(cur.doc_id,doc_id)
        while True:
            if cur.doc_id == -1:
                cur.set_doc_id(doc_id, position)
                break
            elif cur.doc_id == int(doc_id):
                cur.positions.append(int(position))
                break
            cur = cur.next
            self.last_doc = cur

# '"سهمیه المپیک"'
class PostingLists:
    def __init__(self):
        self.posting_list = []
        self.tokens = []
        self.freq = []

    def add_doc(self, word, doc_id, position):
        added = False
        if not self.tokens:
            self.posting_list.append(Tokens(word))
            self.posting_list[-1].add_doc_id(doc_id, position)
            self.tokens.append(word)
            self.freq.append(1)
        elif word == self.tokens[-1]:
            self.posting_list[-1].add_doc_id(doc_id, position)
            self.freq[-1] += 1
        else:
            self.posting_list.append(Tokens(word))
            self.posting_list[-1].add_doc_id(doc_id, position)
            self.tokens.append(word)
            self.freq.append(1)
