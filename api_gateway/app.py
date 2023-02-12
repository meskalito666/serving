from flask import Flask, request, jsonify
import requests
import json
import numpy as np
import os

# передаем часть директории с поколением индексов в качестве пременной среды, 
# чтоб для обновления индекcов можно было просто перезапустить сервис с новой переменной
VERSION = os.environ['VERSION']
centers = np.load(f'/idxs/{VERSION}/centers.npy')

app = Flask(__name__)

@app.route('/send_query', methods=['POST'])
def get_data():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        val = request.json
        query = val['query']

        # передаем текстовый запрос в tf-serving, который трансформирует его в эмбеддинг
        rest_results = requests.post(
            'http://host.docker.internal:8501/v1/models/use_l:predict', 
            json={"instances":[query]}
            ).json()
        emb = rest_results['predictions'][0]
        emb = np.array(emb)

        # полученый эмббединг используем, чтоб найти ближайший кластер
        input_cluster = find_cluster(emb, centers)

        # отсылаем эмбеддинг ближайшему кластеру -> получаем наиболее близкий запрос 
        resp = json.loads(
            requests.post(
                f'http://host.docker.internal:60{input_cluster}0/get_sentence',
                json={'emb':emb.tolist()}
            ).text)

        return jsonify(nearest_sentence=resp['nearest_sentence'])
    else:
        return 'input error, use json'
        
# функция для поиска ближайшего кластера 
def find_cluster(emb, centers):
    u_v = np.sum(emb*centers, axis=1)
    abs_u = np.sqrt(np.sum(emb * emb))
    abs_v = np.sqrt(np.sum(centers * centers, axis=1))
    cos_sims = u_v / (abs_u * abs_v)
    return np.argmin(cos_sims)

if __name__ == "__main__":
    app.run()