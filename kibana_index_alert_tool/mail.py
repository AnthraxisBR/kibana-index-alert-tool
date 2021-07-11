import os
import boto3
from botocore.exceptions import ClientError

from jinja2 import Template

from kibana_index_alert_tool.helper import clear_html_tags


def get_recipients():
    return os.getenv('RECIPIENTS').strip().split(',')


class SendMail(object):
    driver: str
    sender: str
    recipients: list
    body_template: Template
    subject_template: Template

    def __init__(self, project_path: str):
        self.driver = os.getenv('EMAIL_DRIVE', 'ses')
        self.sender = os.getenv('SENDER')
        self.recipients = get_recipients()
        self.body_template: Template = Template(open(f'{project_path}/templates/email.jinja2').read())
        self.subject_template: Template = Template(open(f'{project_path}/templates/subject.jinja2').read())

    def send(self, *kwargs):
        _vars = None if len(kwargs) == 0 else kwargs[0]
        if _vars is None:
            raise Exception('Invalid args to send e-mail')
        if self.driver == 'ses':
            self.send_ses(_vars=_vars)

    def send_ses(self, _vars):
        AWS_REGION = "eu-west-1"
        SUBJECT = self.subject_template.render(_vars)
        BODY_HTML = self.body_template.render(_vars)
        BODY_TEXT = clear_html_tags(BODY_HTML)

        CHARSET = "UTF-8"
        session = boto3.Session(profile_name=os.getenv('AWS_PROFILE', 'default'))
        client = session.client('ses', region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': self.recipients
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=self.sender,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            return True
