import requests
import json
import yaml
import errno
import pandas as pd
import os

from requests import HTTPError


def load_config(config_path):
    with open(config_path, 'r') as yaml_file:
        conf = yaml.safe_load(yaml_file)

    return conf


def create_folder(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    config = load_config('./config.yaml')

    url = config["API"]["url"] + config["AUTH"]["endpoint"]
    headers = {'content-type': 'application/json'}
    data = config["AUTH"]["payload"]

    r = requests.post(url, data=json.dumps(data), headers=headers)

    rec = r.json()

    token = 'JWT ' + rec["access_token"]

    url = config["API"]["url"] + config["API"]["endpoint"]
    data = config["API"]["payload"]  # YYYY-MM-DD
    headers = {'content-type': 'application/json', 'Authorization': token}

    # Request data
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print(type(r.json()))

    for_store = r.json()

    # Store r json into folder
    for i in range(len(for_store)):
        my_dict = for_store[i]
        df = pd.DataFrame(list(my_dict.items()), columns=['product_id', 'date'])
        path = './data/' + for_store[i]['date']
        create_folder(path)
        csv_file_out = str(for_store[i]['product_id']) + '.csv'
        df.to_csv(os.path.join(path, csv_file_out))
