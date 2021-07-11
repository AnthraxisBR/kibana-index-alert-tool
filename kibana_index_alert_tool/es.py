import logging
import os
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

from kibana_index_alert_tool.mail import SendMail
from kibana_index_alert_tool.index_templates import index_component, index_template

logging.basicConfig(filename='install-error-log.log', filemode='a', level=logging.DEBUG)


def get_hosts() -> list:
    hosts: str = os.getenv('ES_HOSTS')
    if hosts is not None:
        return hosts.split(',')
    raise Exception('Variable ES_HOSTS cannot be None, verify you .env file or set it in your environment variables')


def client(scheme: str = 'https'):
    es = Elasticsearch(
        get_hosts(),
        http_auth=(os.getenv('ES_USERNAME'), os.getenv('ES_PASSWORD')),
        scheme=scheme,
        port=os.getenv('ES_PORT', 9200),
    )
    return es


def get_data(index: str):
    res = client().search(index=index, body={
        "query": {
            "match": {
                "status": 0
            }
        }
    })
    return res


def set_as_sent(index: str, _id: str, unset: bool = False):
    if unset:
        return client().update(index=index,
                               id=_id,
                               body={"doc": {"status": 0}}
                               )
    return client().update(index=index,
                           id=_id,
                           body={"doc": {"status": 1}}
                           )


def send_email(data: dict, project_path: str) -> bool:
    return SendMail(project_path).send_ses(data)


def scan_index(args):
    index: str = args.index
    project_path: str = args.project_path
    print("Scanning index")
    data = get_data(index)
    mails_sent = 0
    if data['hits']['total']['value'] == 0:
        print('0 e-mails to send')
    for hit in data['hits']['hits']:
        _source = hit['_source']
        _id = hit['_id']
        print(f'Checking hit: {hit["_id"]}')
        if 'status' not in _source:
            print(f'Setting default e-mail status as not sent')
            set_as_sent('alerting-external', _id, unset=True)
            send_status = 0
        else:
            send_status = _source['status']

        if not send_status:
            print(f'Sending e-mail')
            if send_email(_source, project_path):
                mails_sent += 1
                print(f'Setting e-mail as sent')
                print(set_as_sent('alerting-external', _id))
        else:
            pass


def create_component(index_component_name: str):
    print('Creating component template')
    try:
        res = client().cluster.put_component_template(
            name=index_component_name,
            body=index_component
        )
        if res['acknowledged'] is True:
            print('Component defined')
    except TransportError as error:
        logging.error(error, )


def create_index_template():
    index_name = os.getenv('ES_KIBANA_INDEX').replace('*', '')
    index_component_name = f'component: {index_name}'.replace(' ', '').lower()
    index_template_name = f'index: {index_name}'.replace(' ', '').lower()

    create_component(index_component_name)

    index_template['index_patterns'] = [os.getenv('ES_KIBANA_INDEX')]
    index_template['composed_of'] = [index_component_name]

    print('Creating index template')
    try:
        res = client().indices.put_index_template(
            name=index_template_name,
            body=index_template
        )
    except TransportError as error:
        logging.error(error)
        raise Exception("Cannot create or update index, check ")
