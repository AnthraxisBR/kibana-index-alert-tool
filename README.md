# kibana-index-alert-tool

A small trick to send alert e-mails notifications using index connector on Kibana with Basic License

# Requirements

- python3
- boto3
- awscli


### Set up 

## Configure AWS CLI 

Configure a profile with permissions to send e-mail from SES (AWS) 

IMPORTANT: current only AWS SES e-mail drive available (feel free create or to ask for others driver).

## 2. Kibana

a. Create one "Index Connector" on Kibana

b. Set up your alerts to use this new connector.

c. Configure your documents inside alerts (this document will be used to create you e-mail content)


    {
      "alert_action_group": "{{alertActionGroup}}",
      "alert_group": "{{context.group}}",
      "alert_id": "{{alertId}}",
      "alert_event": "alert",
      "alert_reason": "{{context.reason}}",
      "alert_state": "{{context.alertState}}",
      "alert_name": "{{alertName}}",
      "alert_instance_id": "{{alertInstanceId}}",
      "alert_metric": "{{context.metric}}",
      "context_timestamp": "{{context.timestamp}}",
      "context_value": "{{context.value}}",
      "context_message": "{{context.message}}",
      "kibana_base_url": "{{kibanaBaseUrl}}",
      "date": "{{date}}",
      "tag": "{{tag}}",
      "status": 0
    }


### 3. Setup Code Source

a. Clone this repository where you prefer

b. Run ./install.sh script
    
    chmox +x install.sh
    ./install.sh


### Custom e-mail body

To customize e-mail template, just modify files inside `templates` folder.

1. Email HTML: email.jinja2
2. Email Subject: subject.jinja2

Obs.: All variables available in your index are available inside e-mail templates.


## TODO

1. SendGrid
2. Allow use Kibana users as recipients 
3. 
