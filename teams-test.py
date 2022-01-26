import requests
import json

# for local test, use http://127.0.0.1:[ PORTA ]/webhook
# take Teams's channel webhook endpoint in 
# [ channel ] > MENU > Connectors > search "Incoming Webhook" > do what need > take url
webhook_url = 'WEBHOOK ENDPOINT LINK'
# https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cconnector-html#user-mention-in-incoming-webhook-with-adaptive-cards
data = {
    "type": "message",
    "attachments": [
        {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Large",
                    "weight": "Bolder",
                    "text": "Sample Adaptive Card with User Mention"
                },
                {
                    "type": "TextBlock",
                    "text": "Attention! <at>Adele AAD</at>"
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {
                        "$data": "${properties}",
                        "title": "${key}:",
                        "value": "${value}"
                        }
                    ]
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "msteams": {
                "entities": [
                      {
                        "type": "mention",
                        "text": "<at>Adele AAD</at>",
                        "mentioned": {
                          "id": "lucas@someone.com",
                          "name": "Lucas Test"
                        }
                      }
                ]
                }
            },
        }]
    }

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
