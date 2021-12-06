import requests
import json

# for local test, use http://127.0.0.1:[ PORTA ]/webhook
# take Teams's channel webhook endpoint in 
# [ channel ] > MENU > Connectors > search "Incoming Webhook" > do what need > take url
webhook_url = 'https://somagrupo.webhook.office.com/webhookb2/01c2fc09-eddb-4589-b21a-2bf2651ba347@e48bd5e1-52cd-41f5-87b9-1d25c0d108b6/IncomingWebhook/085bebb9ebd74911ae11d3856ce2c199/a95b19eb-c74c-4d97-802e-6657ac288546'
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
                    "text": "Atenção! <at>Adele AAD</at>"
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
                          "id": "lucas.lopes@somagrupo.com.br",
                          "name": "Lucas Lopes"
                        }
                      }
                ]
                }
            },
        }]
    }

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})