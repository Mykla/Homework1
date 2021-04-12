import requests
import json
import yaml


from requests import HTTPError


def load_config(config_path):
    with open(config_path, 'r') as yaml_file:
        conf = yaml.safe_load(yaml_file)

    return conf


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

    r = requests.get(url, data=json.dumps(data), headers=headers)
    print(type(r.json()))
