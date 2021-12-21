import json
import re
from elasticsearch import Elasticsearch
import xmltodict
import os


def parsexmls(folderNames):
    allXmls = []
    for fname in folderNames:
        # print(fname)
        with open(fname, 'r') as fp:
            try:
                s = fp.read()
            except Exception as e:
                print("type error: " + str(e)+", fname: " + fname)
            sl = re.split(r'\<\/DOC\>\n', s)
            ssl = [x + '</DOC>' for x in sl[:-2]]
            for xml in ssl:
                xxml = {}
                try:
                    tempXml = xmltodict.parse(xml)
                    xxml = tempXml["DOC"]
                    # print(xxml)
                except Exception as e:
                    print("type error: " + str(e) +", fname: " + fname)
                    # print(xml)
                allXmls.append(xxml)
    return allXmls

def data_to_ES(datas):
    es = Elasticsearch(host="localhost", port=9200)
    _index = "extra_credit0"
    i = 0
    for data in datas:
        i = i + 1
        es.index(index=_index, document=json.dumps(data))
        print(i)

    # http://localhost:9200/extra_credit0/_search



if __name__ == '__main__':
    # FILE_DIR = "test/ap89_collection"
    FILE_DIR = "AP_DATA/ap89_collection"

    file_paths = [os.path.join(FILE_DIR, filename)
                  for filename in os.listdir(FILE_DIR) if filename.startswith('ap')]
    dic = parsexmls(file_paths)
    # print(dic[0])
    data_to_ES(dic)