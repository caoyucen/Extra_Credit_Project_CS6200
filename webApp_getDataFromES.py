import urllib
import simplejson as json
from flask import Flask, render_template, request
from flask import request
from elasticsearch import Elasticsearch
from urllib.error import HTTPError

es = Elasticsearch(host="localhost", port=9200)
app = Flask(__name__)

@app.route('/')
def get_personalResult():
    return render_template('mainPage.html')


@app.route('/searchResult', methods=['GET', 'POST'])
def get_result():
    if request.method == 'POST':
        print("COME TO THE PAGE!!!!")
        _search_area = request.form.get("searchArea")
        _search_data = request.form.get("searchWord")
        print("searchWord =")
        print(_search_data)
        _index = "extra_credit0"
        res = es.search(index=_index, body={"query": {"match": {_search_area: _search_data}}})
        allDatas = res.get("hits").get("hits")
        dataList = []
        count = 0
        for data in allDatas:
            # print(data['_source'])
            try:
                newString2 = data['_source']['HEAD']
                print(newString2)
                if(len(newString2) > 0):
                    newString2 = str(newString2).replace(",", " ")
                    newString2 = str(newString2).replace("\"", " ")
                    newString2 = str(newString2).replace("\n", " ")
                    data['_source']['HEAD'] = str(newString2).replace("  ", " ")
                print(data['_source']['HEAD'])
            except:
                print("No HEAD")
            newString = data['_source']['TEXT']
            newString = str(newString).replace("\'", " ")
            newString = str(newString).replace("`", " ")
            newString = str(newString).replace(",", " ")
            newString = str(newString).replace("\n", " ")
            data['_source']['TEXT'] = str(newString).replace("\"", " ")
            dataList.append(data['_source'])
            count = count + 1
            print(count)
        jsonString = str(json.dumps(dataList)).replace("'", " ")
        # # print(jsonString)
        return render_template('searchResultPage.html', Datas=jsonString)


if __name__ == '__main__':
    app.run(debug=True)
