"""
    Start the application
"""
import getpass
from kibana_index_alert_tool import main

from dotenv import load_dotenv

load_dotenv(f'/home/{getpass.getuser()}/.kibana_index_alert_tool')

if __name__ == '__main__':
    main()
