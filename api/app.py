import os, json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

@app.route('/coef_params/<dataset_name>', methods=['GET'])
def coef_params(dataset_name):

    with open(f'data/load/{dataset_name}_coef_params.json') as f:
        data = json.load(f)
    print(data)
    return data

@app.route('/dataset/<dataset_name>', methods=['GET'])
def dataset(dataset_name):

    with open(f'data/load/{dataset_name}_transformed.json') as f:
        data = json.load(f)
    print(data)
    return data


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=os.getenv('PORT'))