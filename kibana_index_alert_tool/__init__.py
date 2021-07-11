#!/usr/bin/python3
from kibana_index_alert_tool.es import scan_index, create_index_template
from kibana_index_alert_tool.kibana import create_connector

import argparse
import sys

__version__ = 'v0.0.1'


class KibanaIndexAlertTool(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='')

        parser.add_argument(
            '--command',
            dest='command',
            action='store',
            type=str,
            help='Available commands',
            choices=['scan-index', 'create-index-template', 'create-connector']
        )

        # Optional
        parser.add_argument('--version', '-v',
                            action='store_true',
                            help='The version of this package')

        args = parser.parse_args(sys.argv[1:2])

        if hasattr(args, 'version') and args.version is not False:
            self.version()
            exit(0)

        if hasattr(args, 'command') and args.command is None:
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        command = args.command.replace('-', '_')

        getattr(self, command)()

    @staticmethod
    def version():
        print(__version__)

    @staticmethod
    def scan_index():
        parser = argparse.ArgumentParser(
            description=''
        )

        parser.add_argument('--profile',
                            dest='profile',
                            action='store',
                            type=str,
                            default='default',
                            help='AWS Profile to authenticate, will use the \
                            profiles available on .aws/credentials. \
                            Default: default. \
                            Use with SES email driver'
                            )

        parser.add_argument('--index',
                            dest='index',
                            action='store',
                            type=str,
                            required=True,
                            help='Inform the index used on Kibana connector'
                            )

        parser.add_argument(
            '--project_path',
            dest='project_path',
            action='store',
            type=str,
            required=True,
            help='Set project path'
        )
        args = parser.parse_args(sys.argv[2:])

        scan_index(args)

    @staticmethod
    def create_index_template():
        create_index_template()

    @staticmethod
    def create_connector():
        create_connector()


def main():
    KibanaIndexAlertTool()


if __name__ == '__main__':
    main()
