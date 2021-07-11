import json
import requests
import os
import logging

logging.basicConfig(filename='install-error-log.log', filemode='a', level=logging.DEBUG)

CONNECTOR_NAME = "kibana_index_alert_tool_connect"


def connector_exists():
    url: str = os.getenv('KIBANA_HOST') + '/api/actions'
    res = requests.get(url,
                       auth=(os.getenv("KIBANA_USERNAME"), os.getenv("KIBANA_PASSWORD")),
                       headers={
                           'kbn-xsrf': 'true',
                           'Content-Type': 'application/json'
                       })
    connectors = json.loads(res.content)
    for connector in connectors:
        if CONNECTOR_NAME == connector['name']:
            return True
    return False


def create_connector():
    if connector_exists():
        logging.error(f'Connector {CONNECTOR_NAME} already exists')
        raise Exception(f'Connector {CONNECTOR_NAME} already exists')
    connector: dict = {
        "name": CONNECTOR_NAME,
        "actionTypeId": ".index",
        "config": {
            "index": os.getenv('ES_KIBANA_INDEX')
        }
    }
    url: str = os.getenv('KIBANA_HOST') + '/api/actions/action'
    res = requests.post(url,
                        json=connector,
                        auth=(os.getenv("KIBANA_USERNAME"), os.getenv("KIBANA_PASSWORD")),
                        headers={
                            'kbn-xsrf': 'true',
                            'Content-Type': 'application/json'
                        })

    if res.status_code == 200:
        print('Connector created with success')
    else:
        print('Cannot create connector')
    return res
