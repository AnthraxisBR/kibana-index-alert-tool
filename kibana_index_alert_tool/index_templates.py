index_component: dict = {
    "template": {
        "mappings": {
            "properties": {
                "date": {
                    "index": True,
                    "ignore_malformed": False,
                    "store": False,
                    "type": "date",
                    "doc_values": True
                },
                "alert_action_group": {
                    "type": "text"
                },
                "alert_event": {
                    "type": "text"
                },
                "alert_group": {
                    "type": "text"
                },
                "alert_id": {
                    "type": "text"
                },
                "alert_instance": {
                    "type": "text"
                },
                "alert_metric": {
                    "type": "text"
                },
                "alert_name": {
                    "type": "text"
                },
                "alert_reason": {
                    "type": "text"
                },
                "alert_state": {
                    "type": "text"
                },
                "context_message": {
                    "type": "text"
                },
                "context_value": {
                    "type": "text"
                },
                "kibana_base_url": {
                    "type": "text"
                },
                "status": {
                    "type": "boolean"
                },
                "tags": {
                    "type": "text"
                }
            }
        }
    }
}

index_template: dict = {
    "index_patterns": [],
    "template": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "_source": {
                "enabled": True
            }
        }
    },
    "priority": 500,
    "composed_of": [],
    "version": 1
}
