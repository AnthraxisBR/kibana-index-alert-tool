"""
    Start the application
"""
import os
import getpass
from kibana_index_alert_tool import main

from dotenv import load_dotenv


home = os.path.expanduser("~")
load_dotenv(f'/{home}/.kibana_index_alert_tool')

if __name__ == '__main__':
    main()
