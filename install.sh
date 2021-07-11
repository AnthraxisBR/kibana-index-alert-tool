#!/bin/bash

echo "Installing Kibana Index Alert Tool"

! python --version &> /dev/null && { echo "You need to install python to run this program"; echo "Setup Failed!"; exit 1; }
! python --version 2>&1 | grep -q '^Python 3\.' && { echo "You cannot use python 2"; echo "Setup Failed!"; exit 1; }
! pip --version &> /dev/null && { echo "You need to install pip to run this program"; echo "Setup Failed!"; exit 1; }
! pip --version 2>&1 | grep -q '^pip 21\.' && { echo "Please upgrade your pip version"; echo "Setup Failed!"; exit 1; }

echo "Current dir: $(pwd)"
echo "Current user: $(whoami)"

echo "1 - Installing pip requirements"
pip install -r requirements.txt

echo "2 - cronjob from $(pwd)/cron.py file"
if python cron.py --username="$(whoami)" --logfile="$(pwd)" --project_path="$(pwd)" &> /dev/null
then
    echo "    Cronjob registered with success"
else
    echo "    Cannot define cronjob, check $(pwd)/cron.py file"
    echo "Failed! Check error log file : $(pwd)'install-error-log.log'"
    exit
fi

echo "3 - Elastic Search connection requirements"

echo ""
echo "######"
echo "### ATTENTION! MANUAL STEP!"
echo "######"
echo ""
echo "Create a .env file with your host and credentials in ~/.kibana_index_alert_tool"

echo "
AWS_PROFILE=default
EMAIL_DRIVE=ses
SENDER=REPLACE_WITH_YOUR_SENDER
RECIPIENTS=email1@example.examle,email2@example.examle
ES_KIBANA_INDEX=REPLACE_WITH_YOUR_CONNECTOR_INDEX
ES_HOSTS=https://host1.example.example,https://host2.example.example
ES_USERNAME=REPLACE_WITH_YOUR_ES_USERNAME
ES_PASSWORD=REPLACE_WITH_YOUR_ES_PASSWORD
"


echo "Confirm credentials location file: $(pwd)/.env (1,2)"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) break;;
        No ) echo "Failed!"; exit; break ;;
    esac
done


echo "Creating component and index template"
! python run.py --command=create-index-template &> /dev/null && { echo "Failed to create index template! Check error log file : $(pwd)/install-error-log.log"; }

echo "Create action connetor"
! python run.py --command=create-connector &> /dev/null && { echo "Failed to create connector! Check error log file : $(pwd)/install-error-log.log"; }
