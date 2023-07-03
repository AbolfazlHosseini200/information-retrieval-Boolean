import json


def read_file(url):
    f = open(url)
    data = json.load(f)
    return data
