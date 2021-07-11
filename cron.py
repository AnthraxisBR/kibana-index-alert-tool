import getpass
import os
import sys
import argparse
from crontab import CronTab

from dotenv import load_dotenv
dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Setup cronjob')

parser.add_argument(
    '--username',
    dest='username',
    action='store',
    type=str,
    default=getpass.getuser(),
    help='Username to setup cronjob'
)

parser.add_argument(
    '--logfile',
    dest='logfile',
    action='store',
    type=str,
    default=None,
    help='Configure cron output logfile'
)

parser.add_argument(
    '--project_path',
    dest='project_path',
    action='store',
    type=str,
    required=True,
    help='Set project path'
)

args = parser.parse_args(sys.argv[1:])

cron = CronTab(user=args.username)

load_dotenv(f'/home/{args.username}/.kibana_index_alert_tool')

index: str = os.getenv('ES_KIBANA_INDEX')
python_path: str = os.getenv('PYTHON_PATH', '/usr/bin/python3')

command = f'{python_path} {dir_path}/run.py --command=scan_index'

if index is not None:
    command += f' --index={index}'

if args.project_path is not None:
    command += f' --project_path={args.project_path}'

if args.logfile is not None:
    command += f' >> {args.logfile}/`date +\%Y\%m\%d`-cron.log 2>&1'


job = cron.new(command=command)

##
# Change here to modify cron rule
##
job.minute.every(1)

##
#
##

cron.write()
