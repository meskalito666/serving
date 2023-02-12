from flask import Flask, request, jsonify
import requests
import numpy as np
import json
import os
import joblib

# передаем часть директории с поколением индексов в качестве пременной среды, 
# чтоб для обновления индектов можно было просто перезапустить сервис с новой переменной
VERSION = os.environ['VERSION']
# передаем индекс кластера в качестве пременной среды, 
# чтоб при запуске 4х сервисов, каждый взял на себя по индексу каждого из 4х кластеров
CLUSTER_ID = os.environ['CLUSTER_ID']
index = joblib.load(f'/idxs/{VERSION}/cluster{CLUSTER_ID}/index')

with open(f'/idxs/{VERSION}/cluster{CLUSTER_ID}/sentences.json') as f:
    sentences = json.load(f)

app = Flask(__name__)

# ищем самый похожий запрос 
@app.route('/get_sentence', methods=['POST'])
def get_sentence():
    emb = np.array(request.json['emb'], dtype='float32')
    _, doc = index.search(emb.reshape(1,-1),1)
    doc = doc.flatten()
    match = sentences[doc[0]]

    return jsonify(nearest_sentence=match)

if __name__ == "__main__":
    app.run()